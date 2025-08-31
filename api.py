# api.py — FastAPI backend for Hybrid Music Recommender (single-user)
# Endpoints:
#   GET  /songs                      → list all songs
#   POST /songs                      → add manual song
#   DELETE /songs/{song_id}          → delete song
#   POST /import-deezer              → import songs from Deezer (no API key)
#   POST /events                     → record {song_id, kind: like|play|skip}
#   GET  /recommendations            → top-N hybrid recs (CB + CF [+ MF later])
#   GET  /similar                    → top-N content-similar songs to a seed
#   GET  /stats                      → basic library stats
#   GET  /playlist                   → list playlist items (as songs)
#   POST /playlist/add               → add a song_id to playlist
#   POST /playlist/remove            → remove a song_id from playlist
#   GET  /playlist/export            → JSON export of current playlist
#
# How to run:
#   pip install fastapi uvicorn requests scikit-learn scipy numpy pydantic
#   uvicorn api:app --reload

from __future__ import annotations
from typing import List, Dict, Any, Optional
import torch, torch.nn as nn, torch.optim as optim
import json
import os
import hashlib

import numpy as np
from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# ---- local modules (you already have these) ---------------------------------
from song import Song                   # musiclib/song.py
from library import SongLibrary    # wrapper using BST keyed by song_id

# ----------------------------------------------------------------------------
# Storage setup
# ----------------------------------------------------------------------------
DATA_DIR = os.environ.get("MUSICLIB_DATA", ".")
LIB_PATH = os.path.join(DATA_DIR, "library.json")
INTERACTIONS_PATH = os.path.join(DATA_DIR, "interactions.json")  # {song_id: {likes, plays}}
PLAYLIST_PATH = os.path.join(DATA_DIR, "playlist.json")          # [song_id, ...]

os.makedirs(DATA_DIR, exist_ok=True)

# Small JSON helpers (robust to missing/corrupt files)
def _load_json(path: str, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def _save_json(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

# ----------------------------------------------------------------------------
# App & global state
# ----------------------------------------------------------------------------
app = FastAPI(title="Hybrid Music Recommender API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev-friendly; tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

library = SongLibrary(LIB_PATH)
interactions: Dict[str, Dict[str, int]] = _load_json(INTERACTIONS_PATH, {})  # {song_id: {likes, plays}}
playlist: List[str] = _load_json(PLAYLIST_PATH, [])

# ----------------------------------------------------------------------------
# Content features (TF-IDF)
# ----------------------------------------------------------------------------
_vectorizer: Optional[TfidfVectorizer] = None
_content_matrix: Optional[sparse.csr_matrix] = None
_id_to_idx: Dict[str, int] = {}
_idx_to_id: List[str] = []


def _song_text(s: Song) -> str:
    # simple concatenation of text features
    parts = [s.title, s.artist] + list(getattr(s, "genres", []) or [])
    return " ".join(str(x) for x in parts if x)


def rebuild_content() -> None:
    """Recompute TF-IDF features for the entire library."""
    global _vectorizer, _content_matrix, _id_to_idx, _idx_to_id
    songs = library.bst.inorder()  # List[Song]
    _idx_to_id = [s.song_id for s in songs]
    _id_to_idx = {sid: i for i, sid in enumerate(_idx_to_id)}
    corpus = [_song_text(s) for s in songs]
    if not corpus:
        _vectorizer = None
        _content_matrix = None
        return
    _vectorizer = TfidfVectorizer(min_df=1, stop_words="english")
    _content_matrix = _vectorizer.fit_transform(corpus)


def content_similar_ids(song_id: str, k: int = 10) -> List[str]:
    if _content_matrix is None or song_id not in _id_to_idx:
        return []
    i = _id_to_idx[song_id]
    sims = cosine_similarity(_content_matrix[i], _content_matrix).ravel()
    sims[i] = -1  # exclude self
    top = np.argsort(-sims)[:k]
    return [_idx_to_id[j] for j in top]


def content_scores_for_user() -> Dict[str, float]:
    # Build an average profile from interacted items (likes+plays)
    if _content_matrix is None or len(interactions) == 0:
        return {}
    idxs = [ _id_to_idx[sid] for sid in interactions.keys() if sid in _id_to_idx ]
    if not idxs:
        return {}
    prof = _content_matrix[idxs].mean(axis=0)     # (1, V) but type is numpy.matrix
    prof = np.asarray(prof).reshape(1, -1)        # convert to ndarray
    sims = cosine_similarity(prof, _content_matrix).ravel()  # fixes
    return { _idx_to_id[i]: float(sims[i]) for i in range(len(_idx_to_id)) }
# ----------------------------------------------------------------------------
# Collaborative (toy item-kNN reusing TF-IDF as item features)
# ----------------------------------------------------------------------------

def cf_item_scores() -> Dict[str, float]:
    if _content_matrix is None or len(_idx_to_id) == 0 or len(interactions) == 0:
        return {}
    # treat interacted items as neighbors; score other items by summed similarity
    scores = np.zeros(len(_idx_to_id), dtype=np.float32)
    weights = []
    seeds = []
    for sid, ev in interactions.items():
        j = _id_to_idx.get(sid)
        if j is None:
            continue
        w = (ev.get("likes", 0) * 3.0) + (ev.get("plays", 0) * 1.0)
        seeds.append(j)
        weights.append(w)
    if not seeds:
        return {}
    weights = np.array(weights, dtype=np.float32)
    for j, w in zip(seeds, weights):
        sims = cosine_similarity(_content_matrix[j], _content_matrix).ravel()
        scores += sims * w
    for j in seeds:
        scores[j] = -1e9  # hide seen
    # normalize to 0..1
    scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-8)
    return { _idx_to_id[i]: float(scores[i]) for i in range(len(scores)) }

# ----------------------------------------------------------------------------
# Hybrid blend (α CB + β CF + γ MF[placeholder] + tiny popularity)
# ----------------------------------------------------------------------------

def hybrid_recommend(k: int, alpha: float, beta: float, gamma: float) -> List[Song]:
    cb = content_scores_for_user()
    cf = cf_item_scores()
    pop = { s.song_id: (s.rank or 0) / 100000.0 for s in library.bst.inorder() }
    seen = set(interactions.keys())

    scores: Dict[str, float] = {}
    for s in library.bst.inorder():
        sid = s.song_id
        if sid in seen:
            continue
        score = alpha*cb.get(sid, 0.0) + beta*cf.get(sid, 0.0) + gamma*0.0 + pop.get(sid, 0.0)
        scores[sid] = score

    top = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:k]
    sid2song = { s.song_id: s for s in library.bst.inorder() }
    return [sid2song[sid] for sid, _ in top if sid in sid2song]

# ----------------------------------------------------------------------------
# Deezer helpers (inline client to avoid extra files)
# ----------------------------------------------------------------------------
DEEZER_BASE = "https://api.deezer.com"

def deezer_search_tracks(query: str, limit: int = 50) -> List[Song]:
    limit = max(1, min(int(limit), 200))
    url = f"{DEEZER_BASE}/search"
    r = requests.get(url, params={"q": query, "limit": limit}, timeout=10)
    r.raise_for_status()
    rows = r.json().get("data", [])
    out: List[Song] = []
    for row in rows:
        song_id = str(row.get("id"))
        title = row.get("title", "")
        artist = (row.get("artist") or {}).get("name", "")
        album = (row.get("album") or {}).get("title", "")
        duration = int(row.get("duration") or 0)
        rank = int(row.get("rank") or 0)
        out.append(Song(song_id=song_id, title=title, artist=artist, album=album, genres=[], duration=duration, rank=rank))
    return out

# ----------------------------------------------------------------------------
# Schemas
# ----------------------------------------------------------------------------
class SongIn(BaseModel):
    title: str
    artist: str
    album: Optional[str] = ""
    genres: Optional[List[str]] = []
    duration: Optional[int] = 0
    rank: Optional[int] = 0

class SongOut(BaseModel):
    song_id: str
    title: str
    artist: str
    album: str = ""
    genres: List[str] = []
    duration: int = 0
    plays: int = 0
    rank: int = 0

class EventIn(BaseModel):
    song_id: str
    kind: str  # like | play | skip

class PlaylistEdit(BaseModel):
    song_id: str

# ----------------------------------------------------------------------------
# Startup
# ----------------------------------------------------------------------------
@app.on_event("startup")
def _startup():
    # ensure JSONs exist
    _save_json(INTERACTIONS_PATH, interactions)
    _save_json(PLAYLIST_PATH, playlist)
    rebuild_content()

# ----------------------------------------------------------------------------
# Songs CRUD
# ----------------------------------------------------------------------------
@app.get("/songs", response_model=List[SongOut])
def list_songs():
    return [s.__dict__ for s in library.bst.inorder()]

@app.post("/songs", response_model=SongOut)
def add_song(payload: SongIn):
    # deterministic short id (so duplicates merge): hash of (title|artist|album)
    base = f"{payload.title}\u241f{payload.artist}\u241f{payload.album or ''}"
    sid = str(int(hashlib.sha256(base.encode()).hexdigest(), 16) % (10**12))
    s = Song(
        song_id=sid,
        title=payload.title,
        artist=payload.artist,
        album=payload.album or "",
        genres=list(payload.genres or []),
        duration=int(payload.duration or 0),
        rank=int(payload.rank or 0),
    )
    library.add_song(s)
    rebuild_content()
    return s.__dict__

@app.delete("/songs/{song_id}")
def delete_song(song_id: str):
    library.delete_song(song_id)
    interactions.pop(song_id, None)
    if song_id in playlist:
        playlist.remove(song_id)
    _save_json(INTERACTIONS_PATH, interactions)
    _save_json(PLAYLIST_PATH, playlist)
    rebuild_content()
    return {"ok": True}

# ----------------------------------------------------------------------------
# Deezer import
# ----------------------------------------------------------------------------
@app.post("/import-deezer", response_model=List[SongOut])
def import_deezer(q: str = Query(..., description="Deezer search query"), limit: int = 5):
    items = deezer_search_tracks(q, limit=limit)
    added: List[Song] = []
    for s in items:
        if library.search_song(s.song_id):
            continue  # skip duplicates by song_id
        library.add_song(s)
        added.append(s)
    rebuild_content()
    return [s.__dict__ for s in added]

# ----------------------------------------------------------------------------
# Events (implicit feedback)
# ----------------------------------------------------------------------------
@app.post("/events")
def add_event(evt: EventIn):
    if library.search_song(evt.song_id) is None:
        return {"ok": False, "error": "unknown song_id"}
    ev = interactions.get(evt.song_id, {"likes": 0, "plays": 0})
    if evt.kind == "like":
        ev["likes"] = int(ev.get("likes", 0)) + 1
    elif evt.kind == "play":
        ev["plays"] = int(ev.get("plays", 0)) + 1
    elif evt.kind == "skip":
        ev["plays"] = max(0, int(ev.get("plays", 0)) - 1)  # tiny negative signal
    interactions[evt.song_id] = ev
    _save_json(INTERACTIONS_PATH, interactions)
    return {"ok": True, "interactions": interactions}

# ----------------------------------------------------------------------------
# Recommendations & Similar
# ----------------------------------------------------------------------------
@app.get("/recommendations", response_model=List[SongOut])
def recommendations(k: int = 10, alpha: float = 0.6, beta: float = 0.3, gamma: float = 0.1):
    recs = hybrid_recommend(k, alpha, beta, gamma)
    return [s.__dict__ for s in recs]

@app.get("/similar", response_model=List[SongOut])
def similar(song_id: str, k: int = 10):
    ids = content_similar_ids(song_id, k=k)
    order = {sid: i for i, sid in enumerate(ids)}
    songs = [s for s in library.bst.inorder() if s.song_id in order]
    songs.sort(key=lambda s: order[s.song_id])
    return [s.__dict__ for s in songs]

# ----------------------------------------------------------------------------
# Stats
# ----------------------------------------------------------------------------
@app.get("/stats")
def stats():
    songs = library.bst.inorder()
    artists = {s.artist for s in songs}
    total_plays = sum(int(s.plays or 0) for s in songs)
    return {
        "songs": len(songs),
        "artists": len(artists),
        "plays": total_plays,
        "interacted": len(interactions),
        "playlist": len(playlist),
    }

# ----------------------------------------------------------------------------
# Playlist endpoints (backend-managed)
# ----------------------------------------------------------------------------
@app.get("/playlist", response_model=List[SongOut])
def get_playlist():
    idset = set(playlist)
    items = [s for s in library.bst.inorder() if s.song_id in idset]
    # preserve playlist order
    order = {sid: i for i, sid in enumerate(playlist)}
    items.sort(key=lambda s: order.get(s.song_id, 1_000_000))
    return [s.__dict__ for s in items]

@app.post("/playlist/add")
def playlist_add(item: PlaylistEdit):
    if library.search_song(item.song_id) is None:
        return {"ok": False, "error": "unknown song_id"}
    if item.song_id not in playlist:
        playlist.append(item.song_id)
        _save_json(PLAYLIST_PATH, playlist)
    return {"ok": True, "count": len(playlist)}

@app.post("/playlist/remove")
def playlist_remove(item: PlaylistEdit):
    if item.song_id in playlist:
        playlist.remove(item.song_id)
        _save_json(PLAYLIST_PATH, playlist)
    return {"ok": True, "count": len(playlist)}

@app.get("/playlist/export")
def playlist_export():
    payload = []
    idset = set(playlist)
    for s in library.bst.inorder():
        if s.song_id in idset:
            payload.append({"song_id": s.song_id, "title": s.title, "artist": s.artist})
    return payload

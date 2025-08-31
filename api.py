# api.py — FastAPI backend for the Hybrid Music Recommender
# Minimal but production-shaped. Uses:
# - your Song/SongBST/SongLibrary (keyed by song_id)
# - a tiny Interactions store (likes/plays)
# - content-based TF-IDF + cosine and a toy item-kNN CF
# - Deezer search (no API key needed)

from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---- your local modules (adjust paths if yours differ)
from song import Song                   # from musiclib/song.py you added earlier
from bst import SongBST                 # from your updated song_id-keyed BST
from song import SongLibrary    # wrapper that saves to library.json
from musiclib.deezer_client import DeezerClient  # our simple Deezer wrapper

# -------------------- App & CORS --------------------
app = FastAPI(title="Hybrid Music Recommender API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev-friendly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Storage --------------------
LIB_PATH = "library.json"
library = SongLibrary(LIB_PATH)
deezer = DeezerClient()

# Interactions: implicit feedback (single user or multi; you can extend easily)
# Here we handle a single "default" user to match your frontend (no auth).
# If you want multi-user later, key by user_id at the top level.
interactions: Dict[str, Dict[str, float]] = {}    # {song_id: weight}

WEIGHTS = {"like": 3.0, "play": 1.0, "skip": -1.0}  # simple scheme; keep non-negative later

def record_event(song_id: str, kind: str):
    w = WEIGHTS.get(kind, 0.0)
    cur = float(interactions.get(song_id, 0.0)) + w
    interactions[song_id] = max(0.0, cur)

# -------------------- Content model (TF-IDF) --------------------
_vectorizer: Optional[TfidfVectorizer] = None
_content_matrix: Optional[sparse.csr_matrix] = None
_id_to_idx: Dict[str, int] = {}
_idx_to_id: List[str] = []

def _song_text(s: Song) -> str:
    # simple text: title + artist + genres
    parts = [s.title, s.artist] + list(getattr(s, "genres", []) or [])
    return " ".join(str(x) for x in parts if x)

def rebuild_content():
    """Recompute TF-IDF vectors for all songs in the library."""
    global _vectorizer, _content_matrix, _id_to_idx, _idx_to_id
    songs = library.bst.inorder()  # List[Song]
    _idx_to_id = [s.song_id for s in songs]
    _id_to_idx = {sid: i for i, sid in enumerate(_idx_to_id)}
    corpus = [_song_text(s) for s in songs]
    if len(corpus) == 0:
        _vectorizer = None
        _content_matrix = None
        return
    _vectorizer = TfidfVectorizer(min_df=1, stop_words="english")
    _content_matrix = _vectorizer.fit_transform(corpus)  # (N, V)

def content_similar(song_id: str, k: int = 10) -> List[str]:
    """Return top-k similar song_ids by cosine on TF-IDF."""
    if _content_matrix is None or song_id not in _id_to_idx:
        return []
    i = _id_to_idx[song_id]
    sims = cosine_similarity(_content_matrix[i], _content_matrix).ravel()
    sims[i] = -1  # exclude self
    top = np.argsort(-sims)[:k]
    return [_idx_to_id[j] for j in top]

def content_scores_for_user() -> Dict[str, float]:
    """Score each item vs an average profile of interacted items."""
    if _content_matrix is None or len(interactions) == 0:
        return {}
    idxs = [ _id_to_idx[sid] for sid in interactions.keys() if sid in _id_to_idx ]
    if not idxs:
        return {}
    prof = _content_matrix[idxs].mean(axis=0)  # (1, V)
    sims = cosine_similarity(prof, _content_matrix).ravel()
    return { _idx_to_id[i]: float(sims[i]) for i in range(len(_idx_to_id)) }

# -------------------- Collaborative (item-kNN, toy) --------------------
def build_user_item() -> sparse.csr_matrix:
    # single-user implicit vector of weights → turn into (1 x N) matrix
    n = len(_idx_to_id)
    if n == 0:
        return sparse.csr_matrix((1, 0))
    data, cols = [], []
    for sid, w in interactions.items():
        j = _id_to_idx.get(sid)
        if j is not None and w > 0:
            cols.append(j); data.append(w)
    if not data:
        return sparse.csr_matrix((1, n))
    return sparse.csr_matrix((data, ([0]*len(cols), cols)), shape=(1, n))

def cf_item_scores() -> Dict[str, float]:
    """Very small item-item cosine recommender using the single user's row."""
    if _content_matrix is None or len(_idx_to_id) == 0:
        return {}
    UI = build_user_item()              # (1, N)
    if UI.nnz == 0:
        return {}
    # approximate: use content matrix columns as proxies for item features (fast path)
    # In a fuller version, you'd compute item-item similarity from UI.T @ UI.
    item_norms = np.sqrt((_content_matrix.power(2)).sum(axis=1)).A.ravel() + 1e-8
    user_vec = UI.toarray().ravel()  # length N
    # score = sum over interacted items of cosine(sim(item_j, item_i)) * weight_j
    scores = np.zeros(len(_idx_to_id), dtype=np.float32)
    interacted = [j for j, w in enumerate(user_vec) if w > 0]
    if not interacted:
        return {}
    # simple pairwise pass (kept small/clear)
    for j in interacted:
        # cosine with all items via TF-IDF similarity row (re-using content sims to stay tiny)
        sims = cosine_similarity(_content_matrix[j], _content_matrix).ravel()
        scores += sims * user_vec[j]
    # remove already seen
    for j in interacted:
        scores[j] = -1e9
    # normalize to 0..1 range
    scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-8)
    return { _idx_to_id[i]: float(scores[i]) for i in range(len(scores)) }

# -------------------- Hybrid --------------------
def hybrid_recommend(k: int, alpha: float, beta: float, gamma: float) -> List[Song]:
    # gamma reserved for MF later; currently unused (kept for API stability)
    cb = content_scores_for_user()
    cf = cf_item_scores()
    # small popularity boost
    pop = { s.song_id: (s.rank or 0) / 100000.0 for s in library.bst.inorder() }

    scores: Dict[str, float] = {}
    seen = set(interactions.keys())
    for s in library.bst.inorder():
        sid = s.song_id
        if sid in seen:
            continue
        score = alpha*cb.get(sid, 0.0) + beta*cf.get(sid, 0.0) + gamma*0.0 + pop.get(sid, 0.0)
        scores[sid] = score

    top = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:k]
    idset = {sid for sid, _ in top}
    # keep order:
    sid2song = { s.song_id: s for s in library.bst.inorder() }
    return [sid2song[sid] for sid, _ in top if sid in sid2song]

# -------------------- Schemas --------------------
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
    kind: str  # "like" | "play" | "skip"

# -------------------- Endpoints --------------------

@app.on_event("startup")
def _startup():
    rebuild_content()

@app.get("/songs", response_model=List[SongOut])
def list_songs():
    return [s.__dict__ for s in library.bst.inorder()]

@app.post("/songs", response_model=SongOut)
def add_song(payload: SongIn):
    # Make a lightweight unique id (in real app: use Deezer id or a UUID)
    sid = str(abs(hash((payload.title, payload.artist, payload.album))) % (10**12))
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
    interactions.pop(song_id, None)  # drop any feedback tied to it
    rebuild_content()
    return {"ok": True}

@app.post("/import-deezer", response_model=List[SongOut])
def import_deezer(q: str = Query(..., description="Deezer search query"), limit: int = 5):
    items = deezer.search_tracks(q, limit=limit)
    added: List[Song] = []
    for s in items:
        # if already present, skip adding duplicate
        if library.search_song(s.song_id):
            continue
        library.add_song(s)
        added.append(s)
    rebuild_content()
    return [s.__dict__ for s in added]

@app.post("/events")
def add_event(evt: EventIn):
    # Record like/play/skip for the (single) user
    if library.search_song(evt.song_id) is None:
        return {"ok": False, "error": "unknown song_id"}
    record_event(evt.song_id, evt.kind)
    return {"ok": True, "interactions": interactions}

@app.get("/recommendations", response_model=List[SongOut])
def recommendations(k: int = 10, alpha: float = 0.6, beta: float = 0.3, gamma: float = 0.1):
    recs = hybrid_recommend(k, alpha, beta, gamma)
    return [s.__dict__ for s in recs]

@app.get("/similar", response_model=List[SongOut])
def similar(song_id: str, k: int = 10):
    ids = content_similar(song_id, k=k)
    # preserve order
    idset = set(ids)
    songs = [s for s in library.bst.inorder() if s.song_id in idset]
    # sort by ids order
    order = {sid: i for i, sid in enumerate(ids)}
    songs.sort(key=lambda s: order.get(s.song_id, 1_000_000))
    return [s.__dict__ for s in songs]

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
    }

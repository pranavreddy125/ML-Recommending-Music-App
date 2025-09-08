# MelodyMatch: Hybrid ML Music Recommender

A hybrid recommender that blends content-based song embeddings with collaborative signals to generate ranked, personalized playlists.


---

## Features

### Hybrid Recommendation
- Content-based similarity using metadata + audio embeddings (title, artist, genre, acoustic features)  
- Collaborative filtering (matrix factorization / implicit feedback) for personalization  
- Weighted hybrid fusion with configurable blending for cold-start vs. personalization

### Playlist & Search
- Create personalized top-K playlists (`/recommend?user_id=...`)  
- Search by song metadata and return similar tracks (ANN fallback available)  
- Export playlist to JSON or local CSV

### Evaluation & Repro
- Offline metrics: Precision@K, Recall@K, NDCG@K (scripts included)  
- Train / eval pipelines with fixed random seed and checkpointing (see `configs/`)

### Lightweight Demo UI
- Static frontend showing search → recommendations → create playlist flow  
- Demo mode supports a sample user with preloaded listening history

---

## Technologies Used

**Backend / ML**
- Python 3.10+, PyTorch (models), scikit-learn (baseline transforms)  
- (Optional) FAISS for approximate nearest neighbors

**Frontend**
- HTML5, CSS3, JavaScript (simple demo UI)

**Serving**
- FastAPI / Flask (lightweight API endpoints for demo)

**Data**
- Local CSV / JSON dataset; optional Spotify enrichment script

---

## Using the application

1. **Open the demo UI**  
   - Open in browser: `http://127.0.0.1:5500`  
   - Or, for the static demo (no backend): open `frontend/index.html` directly.

2. **Search for a song or artist**  
   - Type into the **Search** box and press Enter.  
   - Results show matching tracks and a **Recommend** column/list with similar songs.

3. **Build a playlist**  
   - Click **Add → Playlist** on tracks you like to add them to the current playlist.  
   - The playlist panel shows current top-K items and total length.

4. **Tune hybrid behavior**  
   - Use the **Hybrid weight** slider to favor **Content** (metadata/embeddings) or **Collaborative** (user signals).  
   - After adjusting the slider, click **Refresh** (or **Re-rank**) to update results.

5. **Export or inspect results**  
   - Export the playlist via **Export → JSON/CSV** in the UI.  
   - Or run the CLI to get recommendations (prints JSON / writes to `./output/`):
   ```bash
   python src/recommend.py --user-id <id> --topk 10 --checkpoint models/best_checkpoint.pth

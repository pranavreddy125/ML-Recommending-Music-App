# MusicRecommender: Hybrid ML Music Recommender

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

## Setup Instructions

**Clone the repository**
```bash
git clone https://github.com/<your-username>/music-recommender.git
cd music-recommender

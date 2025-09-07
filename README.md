MusicRecommender: Hybrid ML Music Recommender (Demo)

A hybrid recommender that blends content-based song embeddings with collaborative signals to generate ranked, personalized playlists.

Example of the recommender in action will go here (replace with assets/demo.gif or a demo_video.mp4)

Features

Hybrid Recommendation

Content-based similarity using metadata + audio embeddings (title, artist, genre, acoustic features)

Collaborative filtering (matrix factorization / implicit feedback) for personalization

Weighted hybrid fusion with configurable blending for cold-start vs. personalization

Playlist & Search

Create personalized top-K playlists (/recommend?user_id=...)

Search by song metadata and return similar tracks (ANN fallback available)

Export playlist to JSON or local CSV

Evaluation & Repro

Offline metrics: Precision@K, Recall@K, NDCG@K (scripts included)

Train / eval pipelines with fixed random seed and checkpointing (see configs/)

Lightweight Demo UI

Static frontend showing search → recommendations → create playlist flow

Demo mode supports a sample user with preloaded listening history

Technologies Used

Backend / ML

Python 3.10+, PyTorch (models), scikit-learn (baseline transforms)

(Optional) FAISS for approximate nearest neighbors
Frontend

HTML5, CSS3, JavaScript (simple demo UI)
Serving

FastAPI / Flask (lightweight API endpoint for demo)
Data

Local CSV / JSON dataset; optional Spotify enrichment script



Using the application:

Open the demo UI: http://127.0.0.1:5500 (or open frontend/index.html for static demo mode).

Use the Search box to find a song or artist — results show similar tracks and a “Recommend” list.

Click Add → Playlist on tracks you like to build a top-K playlist.

Adjust the Hybrid weight slider to favor content vs. collaborative signals and hit Refresh to see changes.

Export the playlist with Export → JSON/CSV or run python src/recommend.py --user-id <id> --topk 10 for CLI output.

Demo mode: select Sample user in the top-right to load a preloaded listening history and see personalized recommendations without training.

# AI-Powered Multi-City Route Optimizer 🚛
**Team Name:** [Team_Parinde] | **Event:** Flipr Hackathon 30.2

## 🚀 Key Features
* **Hybrid AI Engine:** Combines *Cheapest Insertion Heuristic* (for speed) with a *Genetic Algorithm* (for global optimization).
* **Real-World Constraints:** Handles Time Windows, Priorities (1-3), and Unloading Service Times.
* **Scalable:** Tested successfully on 20+ cities with <8s response time.
* **Resilient:** Auto-fallbacks for Geocoding and Distance Matrix (ORS API -> Local Cache -> Haversine).

## 📊 Benchmark Results
| Dataset | Cities | Time (s) | Solver Selected |
| :--- | :--- | :--- | :--- |
| Small | 5 | 2.4s | Baseline |
| Medium | 10 | 4.7s | **AI Evolutionary** |
| Large | 20 | 7.2s | **AI Evolutionary** |

## 🛠️ Tech Stack
* **Backend:** FastAPI, Python 3.x, NumPy
* **Frontend:** Streamlit, Folium
* **Data:** OpenRouteService (Matrix API)

## 🏃‍♂️ How to Run
1.  **Backend:** `uvicorn main:app --reload`
2.  **Frontend:** `streamlit run frontend/app.py`# Flipr-AI-Powered-Route-Optimizer

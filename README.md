
# 🚚 Flipr — AI-Powered Multi-City Route Optimizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://flipr-ai-powered-route-optimizer-nmzsqnmbxdcav9chch6mrv.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue?logo=github)](https://github.com/unstoppable-satyam/Flipr-AI-Powered-Route-Optimizer)

**Live demo:** [https://flipr-ai-powered-route-optimizer-nmzsqnmbxdcav9chch6mrv.streamlit.app/](https://flipr-ai-powered-route-optimizer-nmzsqnmbxdcav9chch6mrv.streamlit.app/)

---

## 🔥 Project One-Liner
A hybrid route optimizer for Indian multi-city deliveries combining a **fast baseline heuristic** (cheapest insertion) with an **AI Genetic Algorithm**. Features include **dynamic recalculation**, **PDF reporting**, and an **interactive Streamlit + Folium dashboard**.

---

## 📋 Table of Contents
- [Why this project](#-why-this-project)
- [Quick Start (Run Locally)](#-quick-start-run-locally)
- [Environment Variables](#-environment-variables-env)
- [Frontend Usage](#-frontend-usage-user-flow)
- [Input File Formats](#-input-file-formats)
- [API Overview](#-api-overview)
- [Dynamic Recalculation Engine](#-dynamic-recalculation-engine)
- [Repository Structure](#-repository-structure--file-roles)
- [Testing & Benchmarking](#-testing--benchmarking)
- [Deployment Notes](#-deployment-notes)
- [Troubleshooting](#-troubleshooting)
- [Contributing & Contact](#-contributing--contact)

---

## 💡 Why This Project?
- **Real-world logistics constraints:** Handles priority levels, delivery deadlines, service times, and depot returns.
- **Hybrid optimization:** Instant results via baseline heuristic, improved quality via Genetic Algorithm.
- **Dynamic updates:** Handle live events (add/remove/update stops) while the vehicle is en route.
- **Professional outputs:** AI-generated summaries (Gemini with fallback) and downloadable PDF reports.
- **Clean visualization:** Interactive map, schedule table, and metrics dashboard.

---

## ⚡ Quick Start (Run Locally)

> **Note:** Use **Python 3.10 or 3.12**. Avoid Python 3.14 due to library incompatibilities.

### 1️⃣ Clone the repository
```bash
git clone [https://github.com/unstoppable-satyam/Flipr-AI-Powered-Route-Optimizer](https://github.com/unstoppable-satyam/Flipr-AI-Powered-Route-Optimizer)
cd Flipr-AI-Powered-Route-Optimizer

```

### 2️⃣ Create & activate a virtual environment

**macOS / Linux:**

```bash
python3.12 -m venv venv
source venv/bin/activate

```

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt

```

### 4️⃣ Start the backend

```bash
uvicorn main:app --reload

```

*API runs at: `http://127.0.0.1:8000*`

### 5️⃣ Start the frontend

```bash
streamlit run frontend/app.py

```

*Streamlit opens automatically in your browser.*

---

## 🔒 Environment Variables (.env)

Create a `.env` file in the project root:

```ini
ORS_API_KEY=your_openrouteservice_key_here
GEMINI_API_KEY_1=your_gemini_key_1
GEMINI_API_KEY_2=your_gemini_key_2

```

**Notes:**

* `ORS_API_KEY` is **required** for distance matrix and geocoding.
* Gemini keys are **optional**; if unavailable or quota-exhausted, the app falls back to deterministic summaries.

---

## compass Frontend Usage (User Flow)

1. **Source City:** Enter a valid Indian city (case-insensitive, alias-aware).
2. **Add Destinations:**
* Manual entry with priority (1–3) and deadline (hours).
* Upload CSV / JSON / Excel for bulk import.


3. **Review Destinations:** View, remove, or clear destinations in the sidebar list.
4. **Optimize Route:** Click `🚀 Optimize Route` to compute:
* Route sequence
* Schedule with arrival/departure times (hours)
* Total distance & time
* AI or fallback summary
* Interactive route map


5. **Download Report:** Generate a professional PDF report with summary and schedule.

---

## 📂 Input File Formats

### CSV / Excel

* **Required column:** `city`
* **Optional columns:** `priority`, `deadline_hours`

**Example:**

```csv
city,priority,deadline_hours
Jaipur,2,48
Indore,3,72
Hyderabad,1,36

```

### JSON

```json
[
  {"city": "Roorkee", "priority": 2, "deadline_hours": 1},
  {"city": "Jaipur"}
]

```

---

## 🔌 API Overview

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/optimize` | **Core optimization endpoint.** Returns route sequence, schedule, total stats, summary, and feasibility report. |
| `POST` | `/recalculate` | **Dynamic route recalculation.** Supports add/remove stops and priority updates using fast repair + GA refinement. |
| `POST` | `/generate-report` | Generates and returns a downloadable PDF report. |

---

## 🔁 Dynamic Recalculation Engine

The system uses a two-stage design for live updates:

1. **Stage 1 — Fast Baseline Repair:** Cheapest insertion on remaining stops (milliseconds).
2. **Stage 2 — Bounded Genetic Algorithm (Optional):** Short, time-limited GA seeded with baseline output.

> **Note:** Visited stops remain frozen; only the future route is recalculated.

---

## 🗂 Repository Structure & File Roles

```text
main/
├── main.py                 # FastAPI app & API endpoints
├── models.py               # Pydantic request/response models
└── distance_matrix.py      # ORS matrix + haversine fallback

frontend/
└── app.py                  # Streamlit UI, validation, map & schedule rendering

solver/
├── baseline.py             # Cheapest insertion heuristic
└── genetic.py              # Genetic Algorithm optimizer

utils/
├── index_map.py            # ID ↔ index mapping
├── feasibility.py          # Feasibility checks
├── summary_generator.py    # Gemini-based summary with fallback
└── pdf_generator.py        # PDF report creation

tests/
├── benchmark.py            # Performance benchmarking (5/10/20+ cities)
└── edge_cases.py           # Edge case testing

```

---

## 🧪 Testing & Benchmarking

Use `tests/benchmark.py` to:

* Measure response time.
* Test scalability (5, 10, 20+ cities).
* Identify bottlenecks (ORS calls, solver time).

*Results are output as a CSV for reporting.*

---

## ☁️ Deployment Notes

* **Backend:** Can be deployed on Render / Railway.
* **Frontend:** Can be deployed on Streamlit Cloud.
* **Configuration:**
* Ensure frontend `API_URL` points to the deployed backend `/optimize`.
* Set environment variables directly in the hosting platform dashboard.



---

## 🛠 Troubleshooting

* **City not accepted?** Try `City, State, India` format.
* **Gemini quota exceeded?** Summary falls back automatically to deterministic text.
* **Slow performance?** ORS matrix calls dominate execution time; caching is enabled to mitigate this.
* **404 / detail not found?** Check the frontend API endpoint URL configuration.

---

## 🤝 Contributing & Contact

Contributions are welcome via PRs and issues.

**Authors:** Satyam Kumar, Lavisha Kapoor, Pushpendra Singh, Priyanshu 
**Contact Email:** satyamsks999000@gmail.com

*Made with ❤️ for Flipr Hackathon 30.2*

🚚 Flipr Hackathon 30.2: AI-Powered Multi-City Route Optimization System

GitHub Repository: https://github.com/unstoppable-satyam/Flipr-AI-Powered-Route-Optimizer

📌 Project Overview

This project is an intelligent logistics system designed to optimize delivery routes for multi-city transport operations. Unlike basic GPS, this system accounts for priority orders, strict delivery deadlines, and service times. It features a Hybrid Solver (Baseline Heuristic + Genetic Algorithm) to ensure the most efficient route is found.

Key Features

🧠 AI-Powered Routing: Uses Genetic Algorithms to beat standard heuristics.

⚡ Dynamic Recalculation: Handle real-time events like new orders or cancellations while the truck is en route.

📝 PDF Reporting: Auto-generates professional reports with AI summaries.

🗺️ Interactive Dashboard: Visualizes routes on a map using Streamlit & Folium.

⚙️ Setup & Installation

⚠️ Important: Python Version Warning

Do NOT use Python 3.14.
This project relies on libraries (like numpy and pandas) that may have compatibility issues with Python 3.14.
✅ Recommended Versions: Python 3.10 or 3.12.

1. Create a Virtual Environment

It is highly recommended to run this project in a virtual environment to avoid conflicts.

<details>
<summary><b>🍎 For Mac / Linux Users (Click to Expand)</b></summary>

Open Terminal and navigate to the project folder.

Create the environment:

python3.12 -m venv venv


Activate it:

source venv/bin/activate


</details>

<details>
<summary><b>🪟 For Windows Users (Click to Expand)</b></summary>

Open Command Prompt (cmd) or PowerShell.

Create the environment:

python -m venv venv


Activate it:

venv\Scripts\activate


</details>

2. Install Dependencies

Once your virtual environment is active, install the required packages:

pip install -r requirements.txt


3. Set Up Environment Variables

Create a .env file in the root directory and add your API keys:

ORS_API_KEY=your_openrouteservice_key_here
GEMINI_API_KEY=your_google_gemini_key_here


ORS_API_KEY: Get it free from OpenRouteService.

GEMINI_API_KEY: Get it free from Google AI Studio.

🚀 How to Run the Application

You need to run the Backend and Frontend in two separate terminals.

Terminal 1: Start the Backend API

uvicorn main:app --reload


The API will start at http://127.0.0.1:8000

Terminal 2: Start the Frontend Dashboard

streamlit run frontend/app.py


The dashboard will open in your browser automatically.

📚 API Documentation (Deep Dive)

The backend exposes three main endpoints. Click the toggles below to see detailed specifications.

<details>
<summary><b>🔹 POST /optimize (Core Route Calculation)</b></summary>

Description: Calculates the optimal route sequence, total time, and distance for a given set of destinations.

URL: /optimize

Method: POST

Request Body Example:

{
  "source": { "id": "delhi", "name": "Delhi" },
  "destinations": [
    {
      "id": "jaipur",
      "name": "Jaipur",
      "priority": 1,
      "deadline_hours": 6.0,
      "service_time_minutes": 45
    },
    { "id": "agra", "name": "Agra", "priority": 2 }
  ],
  "vehicle_speed_kmh": 65.0
}


Key Response Fields:

route_sequence: Ordered list of city IDs.

schedule: Detailed timeline with arrival/departure times.

summary: AI-generated explanation of the route.

solver_used: Indicates if "Baseline" or "AI Evolutionary" was used.

</details>

<details>
<summary><b>🔹 POST /recalculate (Dynamic Updates)</b></summary>

Description: Handles real-time updates (like adding a stop) while the vehicle is already moving. It ensures the truck continues from its current location but eventually returns to the original depot.

URL: /recalculate

Method: POST

Request Body Example:

{
  "source": { "id": "delhi", "name": "Delhi" },
  "visited_stop_ids": ["delhi", "agra"],
  "current_time_hours": 3.5,
  "remaining_destinations": [
    { "id": "jaipur", "name": "Jaipur" }
  ],
  "event": {
    "type": "ADD_DESTINATION",
    "payload": {
      "name": "Mathura",
      "priority": 1,
      "deadline_hours": 6.0
    }
  }
}


How it Works:

Identifies Current Location from visited_stop_ids.

Applies the event (Add/Remove stops).

Re-optimizes the remaining route.

Stitches the history + new path + return leg.

</details>

<details>
<summary><b>🔹 POST /generate-report (PDF Export)</b></summary>

Description: Generates a downloadable PDF report with the route summary and schedule table.

URL: /generate-report

Method: POST

Request Body:

{
  "title": "Route Plan",
  "summary": "AI Generated summary text...",
  "schedule": [ ...list of stop objects... ]
}


Response: Binary PDF file stream.

</details>

📂 Project Structure

├── frontend/
│   └── app.py              # Streamlit Dashboard
├── solver/
│   ├── baseline.py         # Heuristic Solver (Cheapest Insertion)
│   ├── genetic.py          # AI Solver (Genetic Algorithm)
│   └── recalculation.py    # Dynamic Update Logic
├── utils/
│   ├── distance_matrix.py  # Map API Integration
│   ├── summary_generator.py# LLM Text Generation
│   └── pdf_generator.py    # ReportLab PDF Creator
├── main.py                 # FastAPI Backend
├── requirements.txt        # Dependencies
└── README.md               # Documentation


🔮 Future Improvements

Real-time Traffic: Integrate Google Maps Traffic API for live delays.

Multi-Vehicle Support: Scale the Genetic Algorithm to handle fleets (VRP).

Driver Mobile App: A React Native app for drivers to view live routes.

Made with ❤️ for Flipr Hackathon 30.2

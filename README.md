# OrbitGuard

OrbitGuard is a full-stack web application designed for satellite collision risk prediction and 3D visualization. It simulates and predicts potential collision risks between two satellites using TLE (Two-Line Element) data and displays the results in an interactive 3D Earth visualization powered by CesiumJS.

## Problem Statement
With the increasing number of satellites and debris in low Earth orbit (LEO), the risk of collisions between objects is constantly rising. Anticipating close approaches (conjunctions) is crucial for satellite operators to maneuver their assets to safety. This tool provides an accessible approach to predicting the closest point of approach between two objects and visualizing the potential risk based on publicly available tracking data.

## Technical Approach

### Backend (Python / FastAPI)
- **TLE Fetching**: Connects to the Celestrak API to pull the most recent TLE records for requested NORAD IDs.
- **Orbital Mechanics**: Utilizes the `skyfield` Python library to calculate satellite ephemerides (positions in a geocentric framework).
- **Collision Risk Logic**: Evaluates the Euclidean distance between two objects at 1-minute intervals over a 24-hour simulation window. Computes risk severity and scores dynamically.

### Frontend (React / Vite)
- **CesiumJS 3D Visualization**: Renders an interactive 3D globe with precise visualizations of orbital paths.
- **Dynamic Risk Display**: Presents the generated data (minimum approach distance, UTC time, risk classification) in an aesthetic cyberpunk-style control panel.
- **Modern UI**: Dark futuristic design using vanilla CSS variables, glassmorphism, and smooth animations.

## Local Setup Instructions

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)

### Running the Backend
1. Open a terminal and navigate to the `backend` directory.
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be running at `http://localhost:8000`.

### Running the Frontend
1. Open a new terminal and navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Open the displayed URL (typically `http://localhost:5173`) in your browser to view the application.

## Future Improvements
- **Real-time Push Updates**: Subscribe to TLE updates via websockets for continuously evolving collision data without refreshing.
- **Many-to-Many Collision Checking**: Efficiently evaluate an entire constellation against known space debris fragments instead of just binary satellite checks.
- **Maneuver Suggestions**: Offer predictive delta-V algorithms to suggest minimal maneuvers to avoid high-risk collisions.

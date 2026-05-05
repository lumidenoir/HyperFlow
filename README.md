# Hypertrophy Planner

A smart, fatigue-based workout tracker designed to optimize recovery and maximize hypertrophic gains. This application tracks your muscle fatigue using exponential decay models, ensuring you never overtrain a "red-zoned" muscle group.

## Features

- **Dynamic Fatigue Tracking**: Automatically calculates muscle fatigue based on volume, RPE, and exercise intensity.
- **Exponential Recovery**: Fatigue decays naturally over time, providing real-time readiness status for every muscle group.
- **Smart Recommendations**: Suggests exercises and set targets based on your current recovery state.
- **Dual Backend Support**: Comes with both a Python (FastAPI) and a Rust (Axum) implementation.
- **Modern UI**: A sleek, responsive dashboard built with Svelte and TailwindCSS.

## Visual Walkthrough

<p align="center">
  <img src="assets/dashboard.png" width="45%" alt="Dashboard" />
  <img src="assets/active_session.png" width="45%" alt="Active Session" />
</p>
<p align="center">
  <img src="assets/history.png" width="45%" alt="History" />
  <img src="assets/exercises.png" width="45%" alt="Exercises" />
</p>
<p align="center">
  <img src="assets/draft.png" width="45%" alt="Drafting" />
</p>


## Tech Stack

### Frontend
- **Framework**: Svelte / Vite
- **Styling**: TailwindCSS
- **State Management**: Svelte Stores

### Backend (Python - Default)
- **Framework**: FastAPI
- **Database**: SQLModel / SQLite
- **Environment**: Python 3.10+

### Backend (Rust - Performance)
- **Framework**: Axum
- **Database**: SQLx / SQLite
- **Performance**: High-concurrency ready

## Getting Started

### Prerequisites
- Node.js & npm
- Python 3.10+ (for Python backend)
- Rust (for Rust backend)

### Quick Start (Python Backend)
1. Ensure you have the dependencies installed.
2. Run the startup script:
   ```bash
   ./run.sh
   ```
3. Open [http://localhost:5173](http://localhost:5173) in your browser.

### Using the Rust Backend
To use the Rust backend, switch to the `rust-backend` branch:
```bash
git checkout rust-backend
```

## API Documentation
Once the backend is running, you can access the interactive Swagger docs at:
- **Python**: [http://localhost:5100/docs](http://localhost:5100/docs)
- **Rust**: [http://localhost:5100/swagger-ui](http://localhost:5100/swagger-ui) (if configured)

---
*Built for lifters, by nerds.*

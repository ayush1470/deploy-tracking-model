# Check-Deviation Model

This repository contains the **Check-Deviation Model**, which uses **DBSCAN clustering** to detect anomalies in GPS location data. It helps identify whether a given GPS coordinate significantly deviates from a user's usual path.

## Table of Contents

- Overview
- Features
- Tech Stack
- Installation
- Usage
- API Endpoint
- Environment Variables
- Contributing
- License

## Overview

The Check-Deviation Model is designed to:

- Fetch GPS location data from a **PostgreSQL database**  
- Train a **DBSCAN clustering model** to detect the normal movement pattern  
- Use **Nearest Neighbors** to check if a new GPS coordinate deviates from the learned path  
- Provide an API endpoint (`/check-deviation`) to determine if a location is an anomaly  

## Features

- **Machine Learning-Based Route Deviation Detection** using **DBSCAN**  
- **Flask API** to handle real-time location deviation checks  
- **PostgreSQL Integration** to store and retrieve GPS data  
- **CORS Enabled** for cross-origin API requests  
- **Environment Variable Support** for secure database credentials  

## Tech Stack

- **Backend:** Flask (Python)  
- **Machine Learning:** Scikit-learn (DBSCAN, Nearest Neighbors)  
- **Database:** PostgreSQL  
- **Cloud Deployment:** Render (or any other cloud provider)  

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ayush1470/deploy-tracking-model.git
cd check-deviation

# Route Deviation Detection API

## 1. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv 
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

## 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## 3. Set Up Environment Variables
Create a `.env` file or set the `POSTGRES_URL` environment variable:

```bash
export POSTGRES_URL="your_postgresql_connection_url"
```

The database URL should follow this format:

```bash
postgresql://user:password@host:port/database_name
```

## 4. Run the Flask API
```bash
python app.py
```

## Usage
Once the server is running, you can send `POST` requests to the `/check-deviation` endpoint to check if a GPS coordinate is an anomaly.

### Example Request (Using cURL)
```bash
curl -X POST http://localhost:5000/check-deviation \
     -H "Content-Type: application/json" \
     -d '{"latitude": 12.9716, "longitude": 77.5946}'
```

### Response Example
```json
{
    "anomaly": 1
}
```
- `1` → Anomalous (Deviation Detected)
- `0` → Normal (No Deviation)

## API Endpoint
| Method | Endpoint         | Description                                        |
|--------|-----------------|----------------------------------------------------|
| POST   | `/check-deviation` | Checks if a given GPS coordinate deviates from the usual path |

### Request Body
```json
{
    "latitude": float,
    "longitude": float
}
```

### Response
```json
{
    "anomaly": 1 or 0
}
```

## Environment Variables
| Variable Name | Description |
|--------------|-------------|
| `POSTGRES_URL` | PostgreSQL connection URL |

**Best Practice:** Store your credentials in a `.env` file or system environment variables instead of hardcoding them.

## Contributing
Contributions are welcome! If you’d like to improve this project, feel free to fork the repo and submit a pull request.

import os
import psycopg2
from flask import Flask, request, jsonify
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from flask_cors import CORS
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

# Use the correct PostgreSQL URL format
POSTGRES_URL = os.getenv("POSTGRES_URL")
if not POSTGRES_URL:
    raise ValueError("POSTGRES_URL is not set. Please add it to environment variables.")

# Parse URL
parsed_url = urlparse(POSTGRES_URL)
DB_HOST = parsed_url.hostname
DB_USER = parsed_url.username
DB_PASSWORD = parsed_url.password
DB_NAME = parsed_url.path.lstrip("/")
DB_PORT = parsed_url.port

# Function to fetch GPS data
def get_gps_data():
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude FROM gps_data")
    gps_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return np.array(gps_data, dtype=float)

# Train DBSCAN model
gps_array = get_gps_data()
dbscan = DBSCAN(eps=0.0028, min_samples=4)
labels = dbscan.fit_predict(gps_array)

# Find core points
core_samples_mask = labels != -1  # Core and border points are non-negative
core_points = gps_array[core_samples_mask]

# Nearest Neighbors model
nn = NearestNeighbors(n_neighbors=1)
nn.fit(core_points)

# Function to check if a point is an anomaly
def is_anomaly(new_point):
    new_point = np.array(new_point).reshape(1, -1)
    distance, _ = nn.kneighbors(new_point)
    return 1 if distance[0][0] > dbscan.eps else 0  # 1 for anomaly, 0 for normal

@app.route('/check-deviation', methods=['POST'])
def check_deviation():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude is None or longitude is None:
        return jsonify({"error": "Invalid input"}), 400

    new_gps_point = (latitude, longitude)
    anomaly = is_anomaly(new_gps_point)

    return jsonify({"anomaly": anomaly})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


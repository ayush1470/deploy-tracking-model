from flask import Flask, request, jsonify
import mysql.connector
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to MySQL
def get_gps_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abcd1234",
        database="women_safety"
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
core_samples_mask = np.zeros_like(labels, dtype=bool)
core_samples_mask[dbscan.core_sample_indices_] = True
core_points = gps_array[core_samples_mask]

# Nearest Neighbors model
nn = NearestNeighbors(n_neighbors=1)
nn.fit(core_points)

# Function to check if a point is an anomaly
def is_anomaly(new_point):
    new_point = np.array(new_point).reshape(1, -1)
    distance, _ = nn.kneighbors(new_point)
    return 1 if distance[0][0] > dbscan.eps else 0  # Return 1 for anomaly, 0 for normal

# API Route: Check if a location is an anomaly
@app.route('/check-deviation', methods=['POST'])
def check_deviation():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude is None or longitude is None:
        return jsonify({"error": "Invalid input"}), 400

    new_gps_point = (latitude, longitude)
    anomaly = is_anomaly(new_gps_point)

    return jsonify({"anomaly": anomaly})  # Just return the boolean 0 or 1

if __name__ == '__main__':
    app.run(debug=True)  # Run locally

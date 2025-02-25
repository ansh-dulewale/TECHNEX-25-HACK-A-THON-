from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from yolov4 import detect_cars
from algo import optimize_traffic
from datetime import datetime

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return "Backend is live!"

@app.route('/api/traffic')  # Example endpoint for traffic data
def get_traffic():
    # Your traffic logic here (e.g., using YOLO)
    return {"status": "traffic data"}

# Ensure the uploads directory exists
os.makedirs('uploads', exist_ok=True)

def store_traffic_data(intersection_id, vehicle_count):
    # Placeholder function to store traffic data
    # Implement the actual database storage logic here
    pass

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('videos')
    if len(files) != 4:
        return jsonify({'error': 'Please upload exactly 4 videos'}), 400

    video_paths = []
    for i, file in enumerate(files):
        video_path = os.path.join('uploads', f'video_{i}.mp4')
        file.save(video_path)
        video_paths.append(video_path)

    num_cars_list = []
    emergency_vehicle_detected = False
    for video_file in video_paths:
        num_cars, emergency_detected = detect_cars(video_file)
        num_cars_list.append(num_cars)
        if emergency_detected:
            emergency_vehicle_detected = True
        store_traffic_data(intersection_id=1, vehicle_count=num_cars)

    result = optimize_traffic(num_cars_list, emergency_vehicle_detected)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

# filepath: AI-Based-Traffic-Management-System/backend/algo.py
import pandas as pd
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('traffic_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def analyze_historical_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM traffic_data")
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows, columns=['id', 'timestamp', 'intersection_id', 'vehicle_count'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Perform analysis (e.g., calculate average vehicle count per hour)
    df['hour'] = df['timestamp'].dt.hour
    avg_vehicle_count = df.groupby('hour')['vehicle_count'].mean()
    return avg_vehicle_count.to_dict()



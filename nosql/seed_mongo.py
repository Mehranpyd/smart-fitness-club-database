import os
import time
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING, DESCENDING

URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('MONGO_DATABASE', 'fitness_club_nosql')

for attempt in range(20):
    try:
        client = MongoClient(URI, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        break
    except Exception:
        if attempt == 19:
            raise
        time.sleep(2)

db = client[DB_NAME]

workouts = db['workout_logs']
activity = db['member_activity']
equipment_logs = db['equipment_logs']

# Reset only the practice database collections.
for c in (workouts, activity, equipment_logs):
    c.delete_many({})

workout_types = ['Strength', 'Cardio', 'Yoga', 'HIIT', 'Pilates']
for i in range(1, 121):
    workouts.insert_one({
        'member_id': i,
        'date': datetime(2026, 1, 1) + timedelta(days=i),
        'workout_type': workout_types[i % len(workout_types)],
        'duration_minutes': 30 + (i % 6) * 10,
        'calories': 180 + (i % 8) * 50,
        'exercises': [
            {'name': 'Exercise A', 'sets': 3, 'reps': 10 + i % 5},
            {'name': 'Exercise B', 'sets': 3, 'reps': 8 + i % 4}
        ]
    })

for i in range(1, 121):
    activity.insert_one({
        'member_id': i,
        'week': (i % 12) + 1,
        'steps': 4000 + (i % 10) * 700,
        'heart_rate_avg': 65 + (i % 12),
        'goals': ['strength', 'fitness'] if i % 2 else ['weight_loss'],
        'notes': 'Regular activity' if i % 3 else 'Increased intensity',
        'optional_metric': {'sleep_hours': 6 + (i % 4)} if i % 4 == 0 else None
    })

conditions = ['Normal', 'Check Soon', 'Maintenance Required']
for i in range(1, 121):
    equipment_logs.insert_one({
        'equipment_id': i,
        'timestamp': datetime(2026, 2, 1) + timedelta(hours=i),
        'usage_minutes': 20 + (i % 10) * 5,
        'temperature': 20 + (i % 7),
        'vibration': round(0.2 + (i % 6) * 0.1, 2),
        'status': conditions[i % 3]
    })

# Indexes: simple, aligned with query examples.
workouts.create_index([('member_id', ASCENDING)])
workouts.create_index([('workout_type', ASCENDING)])
activity.create_index([('member_id', ASCENDING)])
equipment_logs.create_index([('equipment_id', ASCENDING), ('timestamp', DESCENDING)])

print('MongoDB seed complete: 120 documents in each collection.')

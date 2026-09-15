use('fitness_club_nosql');

// CREATE / READ / UPDATE / DELETE
// db.workout_logs.insertOne({member_id: 999, workout_type: 'Strength', duration_minutes: 45});
// db.workout_logs.find({member_id: 10});
// db.workout_logs.updateOne({member_id: 10}, {$set: {duration_minutes: 60}});
// db.workout_logs.deleteOne({member_id: 999});

// Comparison + logical operators
db.workout_logs.find({duration_minutes: {$gte: 50, $lte: 80}});
db.workout_logs.find({$or: [{workout_type: 'HIIT'}, {calories: {$gt: 400}}]});

// Projection + sort + limit
db.workout_logs.find({}, {member_id: 1, workout_type: 1, duration_minutes: 1, _id: 0})
  .sort({duration_minutes: -1}).limit(10);

// Array query
db.workout_logs.find({exercises: {$elemMatch: {sets: 3, reps: {$gte: 12}}}});

// Aggregation
db.workout_logs.aggregate([
  {$group: {_id: '$workout_type', total_minutes: {$sum: '$duration_minutes'}, avg_calories: {$avg: '$calories'}}},
  {$sort: {total_minutes: -1}}
]);

// Semi-structured document query: optional_metric may not exist in every document.
db.member_activity.find({'optional_metric.sleep_hours': {$gte: 8}});

# Design Notes

## Why SQL for the core data?
Members, memberships, classes, trainers, bookings and payments have clear relationships and require data integrity. Primary keys, foreign keys, UNIQUE constraints and CHECK constraints are therefore used.

## Why MongoDB?
Workout logs, activity information and equipment logs can contain flexible fields, arrays and optional values. MongoDB is used to demonstrate document-oriented, schema-flexible storage.

## Level control
This project intentionally avoids a web framework, authentication, cloud deployment, microservices, advanced ORM usage, message queues, or other topics not needed for the brief. The application layer is a small Python script whose job is simply to connect to both databases and demonstrate queries.


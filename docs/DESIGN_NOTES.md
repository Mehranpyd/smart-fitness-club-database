# Design Notes — Student Learning Version

## Why MySQL?
The lectures use MySQL examples for SQL, so this practice project uses MySQL rather than introducing a different relational database engine.

## Why SQL for the core data?
Members, memberships, classes, trainers, bookings and payments have clear relationships and require data integrity. Primary keys, foreign keys, UNIQUE constraints and CHECK constraints are therefore used.

## Why MongoDB?
Workout logs, activity information and equipment logs can contain flexible fields, arrays and optional values. MongoDB is used to demonstrate document-oriented, schema-flexible storage.

## Level control
This project intentionally avoids a web framework, authentication, cloud deployment, microservices, advanced ORM usage, message queues, or other topics not needed for the brief. The application layer is a small Python script whose job is simply to connect to both databases and demonstrate queries.

## Learning order
1. Open the ER diagram.
2. Read `01_schema.sql` and identify PK/FK/constraints.
3. Read `02_seed.sql` and see how 120 records are generated.
4. Run and modify one query at a time in `04_queries.sql`.
5. Open `nosql/queries.js` and compare MongoDB CRUD with SQL CRUD.
6. Change one MongoDB document field and write a new query for it.
7. Read `app/main.py` last and identify where the application connects to each database.

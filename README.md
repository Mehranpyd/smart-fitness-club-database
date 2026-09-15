# Smart Fitness Club — Hybrid Database System

A hybrid database system for managing fitness club data using relational SQL and document-oriented NoSQL technologies.

## Technologies

- MySQL 8 — relational and structured data
- MongoDB — document-oriented NoSQL data
- Python — application integration layer
- Docker Compose — containerized database and application environment

## System Overview

The system uses MySQL for structured data with clear relationships and integrity requirements, while MongoDB is used for flexible and semi-structured data.

The SQL database manages:

- Members
- Trainers
- Memberships
- Fitness classes
- Class bookings
- Payments
- Payment audit records

MongoDB manages:

- Workout logs
- Member activity
- Equipment logs

The Python application layer connects to both database systems and demonstrates data retrieval from the hybrid architecture.

## Database Design

The relational database includes:

- Primary keys
- Foreign keys
- UNIQUE constraints
- NOT NULL constraints
- CHECK constraints
- Normalized relational tables
- Indexes for frequently queried columns

The database also includes a stored procedure, trigger, and transaction example.

MongoDB uses document-oriented structures with:

- Nested documents
- Arrays
- Optional fields
- Referencing through member and equipment identifiers
- Aggregation queries

## SQL Query Coverage

The SQL implementation demonstrates:

- SELECT
- INSERT
- UPDATE
- DELETE
- WHERE
- AND / OR / NOT
- LIKE
- BETWEEN
- IN
- ORDER BY
- COUNT
- SUM
- AVG
- MIN / MAX
- GROUP BY
- HAVING
- INNER JOIN
- LEFT JOIN
- RIGHT JOIN
- Indexes
- EXPLAIN
- Stored procedures
- Triggers
- Transactions with COMMIT / ROLLBACK

## MongoDB Query Coverage

The MongoDB implementation demonstrates:

- Document insertion
- Document retrieval
- Document updates
- Document deletion
- Comparison filters
- Logical filters
- Array queries
- Projection
- Sorting
- Limiting results
- Aggregation

## Data

The main SQL tables contain the following sample data volumes:

- Members — 120 records
- Trainers — 10 records
- Fitness classes — 120 records
- Memberships — 120 records
- Class bookings — 120 records
- Payments — 120 records

Each main MongoDB collection contains 120 documents.

## Project Structure

    Smart_Fitness_Club_Practice_Project_MySQL/
    │
    ├── README.md
    ├── docker-compose.yml
    ├── .gitignore
    ├── verify_project.py
    │
    ├── sql/
    │   ├── 01_schema.sql
    │   ├── 02_seed.sql
    │   ├── 03_indexes.sql
    │   └── 04_queries.sql
    │
    ├── nosql/
    │   ├── seed_mongo.py
    │   └── queries.js
    │
    ├── app/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── main.py
    │
    └── docs/
        ├── ER-diagram.md
        └── DESIGN_NOTES.md

## Running the System

From the project directory:

    docker compose up --build

The Docker environment starts:

- MySQL
- MongoDB
- Python application components

The Python application connects to both databases and executes a small set of integration queries.

To stop the system:

    docker compose down

To remove the database volumes and rebuild the databases from the initialization scripts:

    docker compose down -v
    docker compose up --build

## Main Files

| File | Description |
|---|---|
| `sql/01_schema.sql` | SQL tables, constraints, stored procedure and trigger |
| `sql/02_seed.sql` | SQL sample data |
| `sql/03_indexes.sql` | Database indexes |
| `sql/04_queries.sql` | SQL queries, CRUD and business queries |
| `nosql/seed_mongo.py` | MongoDB sample data |
| `nosql/queries.js` | MongoDB queries and aggregations |
| `app/main.py` | Application layer connecting to MySQL and MongoDB |
| `docs/ER-diagram.md` | SQL ER diagram and MongoDB document structures |
| `docs/DESIGN_NOTES.md` | Database design decisions |
| `verify_project.py` | Project verification utility |

## Architecture

    Smart Fitness Club
             │
      Python Application
             │
       ┌─────┴─────┐
       │           │
      MySQL      MongoDB
       │           │
    Structured   Flexible
       Data       Documents
       │           │
    Members      Workout Logs
    Trainers     Member Activity
    Memberships  Equipment Logs
    Classes
    Bookings
    Payments

## Design Approach

MySQL is used where relationships, constraints and transactional consistency are important.

MongoDB is used where document structures can contain nested data, arrays and optional attributes.

The hybrid approach allows each database technology to be used according to the characteristics of the data it stores.
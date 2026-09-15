import os
import time

import mysql.connector
from pymongo import MongoClient


MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "database": os.getenv("MYSQL_DATABASE", "fitness_club"),
    "user": os.getenv("MYSQL_USER", "fitness_user"),
    "password": os.getenv("MYSQL_PASSWORD", "fitness_pass"),
}

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

MONGO_DB = os.getenv(
    "MONGO_DATABASE",
    "fitness_club_nosql"
)


def mysql_connection():
    """Connect to MySQL with a few retry attempts."""

    for _ in range(20):
        try:
            return mysql.connector.connect(**MYSQL_CONFIG)

        except mysql.connector.Error:
            time.sleep(2)

    raise RuntimeError("Could not connect to MySQL")


def mongo_connection():
    """Connect to MongoDB with a few retry attempts."""

    for _ in range(20):
        try:
            client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=2000
            )

            client.admin.command("ping")

            return client

        except Exception:
            time.sleep(2)

    raise RuntimeError("Could not connect to MongoDB")


def run_mysql_demo():
    """Run a simple MySQL demonstration."""

    conn = mysql_connection()

    cur = conn.cursor(dictionary=True)

    print("\n=== MySQL DEMO ===")

    # ---------------------------------------------------------
    # 1. WHERE, AND, ORDER BY and LIMIT
    # ---------------------------------------------------------

    cur.execute(
        """
        SELECT
            member_id,
            first_name,
            last_name,
            city
        FROM members
        WHERE status = 'Active'
          AND city = 'Berlin'
        ORDER BY last_name
        LIMIT 5
        """
    )

    print(
        "Active Berlin members:",
        cur.fetchall()
    )

    # ---------------------------------------------------------
    # 2. GROUP BY, COUNT, AVG, HAVING and ORDER BY
    # ---------------------------------------------------------

    cur.execute(
        """
        SELECT
            membership_type,
            COUNT(*) AS members,
            AVG(monthly_fee) AS average_fee
        FROM memberships
        GROUP BY membership_type
        HAVING COUNT(*) >= 10
        ORDER BY members DESC
        """
    )

    print(
        "Membership aggregation:",
        cur.fetchall()
    )

    # ---------------------------------------------------------
    # 3. LEFT JOIN and COUNT
    # ---------------------------------------------------------

    cur.execute(
        """
        SELECT
            fc.class_name,
            COUNT(cb.booking_id) AS bookings
        FROM fitness_classes fc
        LEFT JOIN class_bookings cb
            ON fc.class_id = cb.class_id
        GROUP BY
            fc.class_id,
            fc.class_name
        ORDER BY bookings DESC
        LIMIT 5
        """
    )

    print(
        "Popular classes:",
        cur.fetchall()
    )

    # ---------------------------------------------------------
    # 4. Stored Procedure
    # ---------------------------------------------------------

    cur.execute(
        "CALL GetMemberSummary(%s)",
        (1,)
    )

    while True:

        rows = cur.fetchall()

        if rows:
            print(
                "Stored procedure result:",
                rows
            )

        if not cur.nextset():
            break

    # ---------------------------------------------------------
    # 5. CRUD demonstration
    # ---------------------------------------------------------

    # CREATE / INSERT
    cur.execute(
        """
        INSERT INTO members
        (
            first_name,
            last_name,
            email,
            phone,
            city,
            join_date,
            status
        )
        VALUES
        (
            'App',
            'Demo',
            'app.demo@example.com',
            '000',
            'Berlin',
            '2026-09-01',
            'Active'
        )
        """
    )

    new_id = cur.lastrowid

    # UPDATE
    cur.execute(
        """
        UPDATE members
        SET city = 'Potsdam'
        WHERE member_id = %s
        """,
        (new_id,)
    )

    # READ / SELECT
    cur.execute(
        """
        SELECT
            member_id,
            first_name,
            city
        FROM members
        WHERE member_id = %s
        """,
        (new_id,)
    )

    print(
        "CRUD demo:",
        cur.fetchone()
    )

    # DELETE
    cur.execute(
        """
        DELETE FROM members
        WHERE member_id = %s
        """,
        (new_id,)
    )

    conn.commit()

    cur.close()
    conn.close()


def run_mongo_demo():
    """Run a simple MongoDB demonstration."""

    client = mongo_connection()

    db = client[MONGO_DB]

    workouts = db["workout_logs"]

    print("\n=== MongoDB DEMO ===")

    # ---------------------------------------------------------
    # 1. Find one document
    # ---------------------------------------------------------

    print(
        "Workout for member 10:",
        workouts.find_one(
            {"member_id": 10},
            {"_id": 0}
        )
    )

    # ---------------------------------------------------------
    # 2. Comparison operator: $gte
    # ---------------------------------------------------------

    print(
        "Long workouts:",
        list(
            workouts.find(
                {
                    "duration_minutes": {
                        "$gte": 70
                    }
                },
                {
                    "_id": 0,
                    "member_id": 1,
                    "duration_minutes": 1
                }
            ).limit(5)
        )
    )

    # ---------------------------------------------------------
    # 3. Aggregation
    # ---------------------------------------------------------

    pipeline = [
        {
            "$group": {
                "_id": "$workout_type",
                "total_minutes": {
                    "$sum": "$duration_minutes"
                },
                "average_calories": {
                    "$avg": "$calories"
                }
            }
        },
        {
            "$sort": {
                "total_minutes": -1
            }
        }
    ]

    print(
        "Workout aggregation:",
        list(
            workouts.aggregate(pipeline)
        )
    )

    # ---------------------------------------------------------
    # 4. Flexible schema example
    # ---------------------------------------------------------

    print(
        "Documents with optional sleep metric:",
        db["member_activity"].count_documents(
            {
                "optional_metric.sleep_hours": {
                    "$exists": True
                }
            }
        )
    )

    client.close()


if __name__ == "__main__":

    run_mysql_demo()

    run_mongo_demo()

    print(
        "\nHybrid application demo finished successfully."
    )
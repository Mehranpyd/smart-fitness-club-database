# SQL ER Diagram

```mermaid
erDiagram
    MEMBERS ||--o{ MEMBERSHIPS : has
    MEMBERS ||--o{ CLASS_BOOKINGS : makes
    FITNESS_CLASSES ||--o{ CLASS_BOOKINGS : receives
    TRAINERS ||--o{ FITNESS_CLASSES : teaches
    MEMBERS ||--o{ PAYMENTS : makes
    PAYMENTS ||--o{ PAYMENT_AUDIT : creates

    MEMBERS {
      int member_id PK
      varchar first_name
      varchar last_name
      varchar email UK
      varchar phone
      varchar city
      date join_date
      enum status
    }
    TRAINERS {
      int trainer_id PK
      varchar first_name
      varchar last_name
      varchar specialty
      varchar email UK
      decimal hourly_rate
    }
    MEMBERSHIPS {
      int membership_id PK
      int member_id FK
      varchar membership_type
      date start_date
      date end_date
      decimal monthly_fee
      enum status
    }
    FITNESS_CLASSES {
      int class_id PK
      int trainer_id FK
      varchar class_name
      date class_date
      time start_time
      int capacity
      varchar room
    }
    CLASS_BOOKINGS {
      int booking_id PK
      int member_id FK
      int class_id FK
      date booking_date
      enum attendance_status
    }
    PAYMENTS {
      int payment_id PK
      int member_id FK
      date payment_date
      decimal amount
      enum payment_method
      enum payment_status
    }
    PAYMENT_AUDIT {
      int audit_id PK
      int payment_id
      int member_id
      varchar message
      timestamp created_at
    }
```

## MongoDB document structures

- `workout_logs`: member ID, date, workout type, duration, calories, and an **array** of exercise objects. The array demonstrates semi-structured data and nested documents.
- `member_activity`: member ID, weekly activity measures, goals array, notes, and an **optional** sleep metric. Not every document has the optional field.
- `equipment_logs`: equipment ID, timestamp, usage, temperature, vibration, and status. This represents flexible log/sensor-style records.

### Embedding vs Referencing decision

Exercises are embedded inside `workout_logs` because they belong directly to one workout record and are naturally read together. The SQL side keeps core member/class/payment relationships normalized and connected with foreign keys. MongoDB uses `member_id` as a reference value rather than duplicating the full member record.

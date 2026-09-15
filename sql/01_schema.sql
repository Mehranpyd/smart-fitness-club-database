CREATE DATABASE IF NOT EXISTS fitness_club;
USE fitness_club;

DROP TRIGGER IF EXISTS trg_payment_after_insert;
DROP PROCEDURE IF EXISTS GetMemberSummary;

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS class_bookings;
DROP TABLE IF EXISTS fitness_classes;
DROP TABLE IF EXISTS memberships;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS trainers;
DROP TABLE IF EXISTS members;

CREATE TABLE members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(30),
    city VARCHAR(60) NOT NULL,
    join_date DATE NOT NULL,
    status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active'
);

CREATE TABLE trainers (
    trainer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialty VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    hourly_rate DECIMAL(8,2) NOT NULL CHECK (hourly_rate > 0)
);

CREATE TABLE memberships (
    membership_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    membership_type VARCHAR(30) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    monthly_fee DECIMAL(8,2) NOT NULL CHECK (monthly_fee > 0),
    status ENUM('Active','Expired','Cancelled') NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

CREATE TABLE fitness_classes (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    trainer_id INT NOT NULL,
    class_name VARCHAR(80) NOT NULL,
    class_date DATE NOT NULL,
    start_time TIME NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0),
    room VARCHAR(40) NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id)
);

CREATE TABLE class_bookings (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    class_id INT NOT NULL,
    booking_date DATE NOT NULL,
    attendance_status ENUM('Booked','Attended','Cancelled') NOT NULL,
    UNIQUE (member_id, class_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (class_id) REFERENCES fitness_classes(class_id)
);

CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(8,2) NOT NULL CHECK (amount > 0),
    payment_method ENUM('Card','Cash','Bank Transfer') NOT NULL,
    payment_status ENUM('Paid','Pending','Refunded') NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

CREATE TABLE equipment (
    equipment_id INT PRIMARY KEY AUTO_INCREMENT,
    equipment_name VARCHAR(80) NOT NULL,
    category VARCHAR(50) NOT NULL,
    purchase_date DATE NOT NULL,
    condition_status ENUM('Good','Maintenance','Out of Service') NOT NULL,
    location VARCHAR(60) NOT NULL
);

-- Stored procedure: basic taught-style multi-table retrieval.
DELIMITER $$
CREATE PROCEDURE GetMemberSummary(IN p_member_id INT)
BEGIN
    SELECT m.member_id, m.first_name, m.last_name, m.email,
           ms.membership_type, ms.status AS membership_status,
           ms.start_date, ms.end_date
    FROM members m
    LEFT JOIN memberships ms ON m.member_id = ms.member_id
    WHERE m.member_id = p_member_id;
END$$
DELIMITER ;

-- Trigger: simple business rule / automatic audit-style message.
CREATE TABLE IF NOT EXISTS payment_audit (
    audit_id INT PRIMARY KEY AUTO_INCREMENT,
    payment_id INT NOT NULL,
    member_id INT NOT NULL,
    message VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$
CREATE TRIGGER trg_payment_after_insert
AFTER INSERT ON payments
FOR EACH ROW
BEGIN
    INSERT INTO payment_audit(payment_id, member_id, message)
    VALUES (NEW.payment_id, NEW.member_id, CONCAT('Payment recorded: ', NEW.amount));
END$$
DELIMITER ;

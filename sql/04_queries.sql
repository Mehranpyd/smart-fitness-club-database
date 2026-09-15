USE fitness_club;

-- 1. Basic SELECT
SELECT * FROM members LIMIT 10;
SELECT first_name, last_name, city FROM members ORDER BY last_name ASC LIMIT 10;

-- 2. WHERE + comparison + logical operators
SELECT * FROM members WHERE status = 'Active' AND city = 'Berlin';
SELECT * FROM payments WHERE amount > 40 OR payment_status = 'Pending';

-- 3. LIKE, BETWEEN, IN
SELECT * FROM members WHERE email LIKE '%@yahoo.com' LIMIT 10;
SELECT * FROM payments WHERE amount BETWEEN 30 AND 50;
SELECT * FROM members WHERE status IN ('Active','Inactive');

-- 4. Aggregation
SELECT COUNT(*) AS total_members FROM members;
SELECT SUM(amount) AS total_payments FROM payments WHERE payment_status = 'Paid';
SELECT AVG(amount) AS average_payment FROM payments;
SELECT MIN(amount) AS minimum_payment, MAX(amount) AS maximum_payment FROM payments;

-- 5. GROUP BY + HAVING
SELECT city, COUNT(*) AS member_count
FROM members
GROUP BY city
HAVING COUNT(*) >= 10
ORDER BY member_count DESC;

SELECT payment_method, SUM(amount) AS total_amount
FROM payments
GROUP BY payment_method
HAVING SUM(amount) > 1000;

-- 6. INNER JOIN
SELECT m.member_id, m.first_name, m.last_name, ms.membership_type, ms.status
FROM members m
INNER JOIN memberships ms ON m.member_id = ms.member_id;

-- 7. LEFT JOIN: include members without matching records
SELECT m.member_id, m.first_name, m.last_name, cb.booking_id
FROM members m
LEFT JOIN class_bookings cb ON m.member_id = cb.member_id
ORDER BY m.member_id;

-- 8. RIGHT JOIN: include all classes even if no booking exists
SELECT cb.booking_id, fc.class_id, fc.class_name
FROM class_bookings cb
RIGHT JOIN fitness_classes fc ON cb.class_id = fc.class_id
ORDER BY fc.class_id;

-- 9. Business query: class popularity
SELECT fc.class_name, COUNT(cb.booking_id) AS bookings
FROM fitness_classes fc
LEFT JOIN class_bookings cb ON fc.class_id = cb.class_id
GROUP BY fc.class_id, fc.class_name
ORDER BY bookings DESC;

-- 10. CRUD demonstration
INSERT INTO members (first_name,last_name,email,phone,city,join_date,status)
VALUES ('Test','Member','test.member@yahoo.com','+49-170-999999','Berlin','2026-09-01','Active');

UPDATE members
SET phone = '+49-170-888888'
WHERE email = 'test.member@yahoo.com';

SELECT * FROM members WHERE email = 'test.member@yahoo.com';

DELETE FROM members WHERE email = 'test.member@yahoo.com';

-- 11. Stored procedure
CALL GetMemberSummary(1);

-- 12. Trigger result
SELECT * FROM payment_audit ORDER BY audit_id DESC LIMIT 10;

-- 13. Transaction: taught-style COMMIT / ROLLBACK
START TRANSACTION;
UPDATE members SET status = 'Inactive' WHERE member_id = 120;
-- ROLLBACK;  -- use this instead of COMMIT to undo the change
COMMIT;

-- 14. Index / optimization demonstration
EXPLAIN SELECT * FROM members WHERE city = 'Berlin';
EXPLAIN SELECT * FROM payments WHERE member_id = 50;

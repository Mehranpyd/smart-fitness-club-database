USE fitness_club;

CREATE INDEX idx_members_city ON members(city);
CREATE INDEX idx_members_status ON members(status);
CREATE INDEX idx_memberships_member ON memberships(member_id);
CREATE INDEX idx_memberships_status ON memberships(status);
CREATE INDEX idx_classes_date ON fitness_classes(class_date);
CREATE INDEX idx_classes_trainer ON fitness_classes(trainer_id);
CREATE INDEX idx_bookings_member ON class_bookings(member_id);
CREATE INDEX idx_bookings_class ON class_bookings(class_id);
CREATE INDEX idx_payments_member ON payments(member_id);
CREATE INDEX idx_payments_date ON payments(payment_date);
CREATE INDEX idx_equipment_condition ON equipment(condition_status);

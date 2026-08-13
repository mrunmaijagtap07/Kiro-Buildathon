-- ============================================================
-- CampusArchive Seed Data
-- Run AFTER schema.sql
-- ============================================================
-- Admin account: credentials come from environment variables.
-- See init_db.py for the seeding script that reads .env.
-- This file seeds non-sensitive reference data only.
-- ============================================================

USE campus_repository;

-- ─────────────────────────────────────────────────────────────
-- DEPARTMENTS
-- Update dept_code and dept_name to match your college.
-- ─────────────────────────────────────────────────────────────
INSERT IGNORE INTO departments (dept_code, dept_name) VALUES
  ('IT',   'Information Technology'),
  ('CS',   'Computer Science'),
  ('EC',   'Electronics & Communication'),
  ('ME',   'Mechanical Engineering'),
  ('CE',   'Civil Engineering'),
  ('EE',   'Electrical Engineering'),
  ('AIDS', 'AI & Data Science'),
  ('CSBS', 'Computer Science & Business Systems');

-- ─────────────────────────────────────────────────────────────
-- TECHNOLOGY TAGS
-- ─────────────────────────────────────────────────────────────
INSERT IGNORE INTO tags (tag_name) VALUES
  ('Python'),
  ('Flask'),
  ('Django'),
  ('FastAPI'),
  ('Java'),
  ('Spring Boot'),
  ('C'),
  ('C++'),
  ('JavaScript'),
  ('TypeScript'),
  ('React'),
  ('Vue.js'),
  ('Angular'),
  ('Node.js'),
  ('Express.js'),
  ('PHP'),
  ('Laravel'),
  ('HTML/CSS'),
  ('MySQL'),
  ('PostgreSQL'),
  ('MongoDB'),
  ('SQLite'),
  ('Redis'),
  ('Machine Learning'),
  ('Deep Learning'),
  ('Computer Vision'),
  ('NLP'),
  ('IoT'),
  ('Arduino'),
  ('Raspberry Pi'),
  ('Android'),
  ('iOS'),
  ('Flutter'),
  ('React Native'),
  ('Docker'),
  ('AWS'),
  ('Azure'),
  ('Firebase'),
  ('REST API'),
  ('GraphQL'),
  ('Blockchain'),
  ('Cybersecurity'),
  ('Data Science'),
  ('Power BI'),
  ('Tableau'),
  ('OpenCV'),
  ('TensorFlow'),
  ('PyTorch'),
  ('Scikit-learn'),
  ('Pandas');

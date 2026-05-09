# MySQL Schema

Database: `ai_study_recommendation`

## 1) users

- `id` INT PRIMARY KEY AUTO_INCREMENT
- `name` VARCHAR(120) NOT NULL
- `email` VARCHAR(255) NOT NULL UNIQUE
- `standard` INT NOT NULL
- `password` TEXT NOT NULL (bcrypt hash)
- `created_at` DATETIME NOT NULL

## 2) student_profiles

- `id` INT PRIMARY KEY AUTO_INCREMENT
- `user_id` INT NOT NULL UNIQUE (FK -> users.id)
- `student_details` JSON NOT NULL
- `subjects` JSON NOT NULL
- `marks` JSON NOT NULL
- `subject_levels` JSON NOT NULL
- `skills` JSON NOT NULL
- `interests` JSON NOT NULL
- `updated_at` DATETIME NOT NULL

## 3) progress

- `id` INT PRIMARY KEY AUTO_INCREMENT
- `user_id` INT NOT NULL (FK -> users.id)
- `task` TEXT NULL
- `task_type` VARCHAR(20) NOT NULL (`daily` or `weekly`)
- `status` VARCHAR(20) NOT NULL (`pending` or `completed`)
- `score` FLOAT NULL
- `date` VARCHAR(20) NULL
- `created_at` DATETIME NOT NULL
- `completed_at` DATETIME NULL

Suggested index:
- composite index on (`user_id`, `date`)

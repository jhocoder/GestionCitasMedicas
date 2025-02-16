CREATE DATABASE citasmedicas;
USE citasmedicas;

    -- CREATE TABLE users (
    --  id int unsigned auto_increment primary key,
    --  email VARCHAR(200) NOT NULL,
    --  password VARCHAR(255) NOT NULL,
    --  phone VARCHAR(14) NOT NULL
    -- );

    -- CREATE TABLE doctor (
    --  id int unsigned auto_increment primary key,
    --  nombre varchar(200) NOT NULL,
    --  especialidad VARCHAR(20) NOT NULL
    -- );

    -- CREATE TABLE appoinment (
    --     id int unsigned auto_increment primary key,
    --     user_id INT unsigned NOT NULL,
    --     doctor_id INT unsigned NOT NULL,
        
    --     FOREIGN KEY (user_id) REFERENCES users(id),
    --     FOREIGN KEY (doctor_id) REFERENCES doctor(id)
    -- )
    INSERT INTO doctor (nombre, especialidad) VALUES 
    ('Dr. Juan Perez', 'Cardiologia'),
    ('Dra. Maria Lopez', 'Pediatria'),
    ('Dr. Carlos Sanchez', 'Dermatologia');



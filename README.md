# University Grade Management System API

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contact](#contact)

## Introduction
This project is a backend system for managing university grades using Django Rest Framework. The API supports both student, professor roles and administrator roles with features for course registration, grade tracking, and performance monitoring.

## Database Schema


## Features
List the main features of your project:
- JWT Authentication: Secure access using token-based authentication, with support for user registration and login, role-based permissions and access/refresh tokens.
- Student and Professor Management: Professors can manage courses, assign grades and enroll students to courses they manage. Admins can manage all users, subjects, and courses.
- Comprehensive API Documentation: Clear descriptions of database structure, endpoints, and usage examples to simplify integration and testing.

## Installation
Provide step-by-step instructions on how to set up the project locally.

1. Clone the repository:
    ```bash
    git clone git@github.com:Odzen/university-grades.git
    ```
2. Navigate to the project directory:
    ```bash
    cd unversity-grades
    ```
3. Create a virtual environment:
    ```bash
    python3 -m venv env
    ```
4. Activate the virtual environment:
    ```bash
    source env/bin/activate
    ```
5. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Make and apply the migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
7. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage
If you use the production server and want to try the API, sign in with the following credentials (/auth/login/):
- Admin: jsebastian.va@gmail.com - Admin12345.
- Teacher: teacher@gmail.com - Teacher12345.
- Student: student@gmail.com - Student12345.

## Documentation
The API documentation is available at `/docst/` at the root of the project. https://university-grades-460c6e848672.herokuapp.com/docs/ 

## Contact
Email: jsebastian.va@gmail.com
[LinkedIn](https://www.linkedin.com/in/juanvelasquezacevedo/)


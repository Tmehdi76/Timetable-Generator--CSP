# University Timetable Generator (CSP-based)

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![Render](https://img.shields.io/badge/deployed%20on-render-5C4EE5.svg)

An intelligent university timetable scheduling system using Constraint Satisfaction Problem (CSP) algorithms with Flask backend and interactive web interface.

## Features

- 🎯 Automated scheduling with 100% constraint satisfaction
- 🏫 Supports lectures, TDs (tutorials), and TPs (practical sessions)
- 👨‍🏫 Teacher workload balancing (max 3 days/week)
- 🕒 No more than 3 consecutive sessions per group
- 📊 Interactive visualization with group filtering

## Live Demo

Access the deployed application:  
https://timetable-generator-csp-26um.onrender.com/

## How It Works

  **Constraint Modeling**:
   - Teacher availability
   - Group-specific sessions
   - Consecutive session limits

  
Visualization:

Color-coded by course type

Responsive design for all devices

Real-time filtering by student groups

Installation
Local Development
Clone the repository:

bash
git clone https://github.com/yourusername/timetable-generator-csp.git

cd timetable-generator-csp

Set up virtual environment:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install dependencies:

bash
pip install -r requirements.txt
Run the development server:

bash
python app.py

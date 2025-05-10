# 🗓️ University Timetable Generator (CSP-based)

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![Render](https://img.shields.io/badge/deployed%20on-render-5C4EE5.svg)

An intelligent university timetable scheduling system powered by **Constraint Satisfaction Problem (CSP)** algorithms. Built with Flask for the backend and a responsive, interactive web interface.

---

## 🚀 Live Demo

👉 [Try it on Render](https://timetable-generator-csp-26um.onrender.com/)

---

## ✨ Features

- 🎯 Fully automated scheduling with strict constraint satisfaction  
- 🏫 Handles lectures, TDs (tutorials), and TPs (practical sessions)  
- 👨‍🏫 Teacher workload balancing (e.g., max 3 days/week)  
- ⏳ Prevents more than 3 consecutive sessions per group  
- 📊 Interactive and responsive visualization with group-based filtering  

---

## 🧠 How It Works

### ✅ Constraint Modeling

- Teacher availability  
- Group-specific course load  
- Session sequence and spacing rules (e.g., no long blocks)  

### 📈 Visualization

- Color-coded by session type (Lecture, TD, TP)  
- Responsive UI for mobile and desktop  
- Real-time filtering by student groups  

---

## 🛠️ Local Development

### 🔄 Clone the repository

```bash
git clone https://github.com/yourusername/timetable-generator-csp.git
cd timetable-generator-csp
```

## 🐍 Set Up Virtual Environment

```bash
python -m venv venv
```

# For Linux/macOS:

```bash
source venv/bin/activate
```
# For Windows:
```bash

venv\Scripts\activate
```

## 📦 Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the development server

```bash
python app.py
```

## 📄 License
MIT License © Taleb Mehdi

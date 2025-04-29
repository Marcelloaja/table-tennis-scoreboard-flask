# 🏓 Table Tennis Tournament Scoreboard App (Flask)

A lightweight, dynamic web-based scoreboard application for managing and displaying table tennis (ping pong) match scores. Built with Python and Flask, this app supports both **3-set** and **5-set** match formats, complete with real-time score tracking, serve switching, leaderboards, and recent match history.

---

## ✨ Features

- ✅ Choose match format: **Best of 3** or **Best of 5** sets
- ✅ Real-time scoring with **+1 buttons** for each player
- ✅ **Serve indicator** that switches every 2 points
- ✅ Auto set win detection (11 points with minimum 2-point lead, or deuce rules if tied)
- ✅ Automatic match winner declaration (2 of 3 / 3 of 5)
- ✅ Display **per-set score history** (e.g., Set 1: 11–7, Set 2: 9–11, ...)
- ✅ **Leaderboard** tracking top 3–5 players based on total wins
- ✅ **Recent Matches** list with full result details
- ✅ **Reset button** to clear all data (scores, leaderboard, recent matches)

---

## 🖥️ App Screens (Suggestion)
> 📌 You can add screenshots later in this section:
> - Form Input
> - Scoreboard
> - Leaderboard
> - Recent Matches

---

## 📁 Project Structure

├── app.py
├── templates/
│   ├── index.html
│   ├── scoreboard.html
│   ├── leaderboard.html
│   └── recent.html
├── static/
│   └── style.css
└── data/
    ├── players.json
    └── matches.json
    
---

## 🛠️ Tech Stack

- Python 3.x
- Flask
- HTML5 & CSS3
- JSON (local storage)

---

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/table-tennis-scoreboard-flask.git
   cd table-tennis-scoreboard-flask

2. **Install dependencies**
   ```bash
   pip install flask

3. **Run the application**
   ```bash
   python app.py

4. **Open in browser**
   ```bash
    http://localhost:5000

## 🔄 Resetting the App
To reset all data (score, leaderboard, match history), use the Reset button from the scoreboard page.
It will clear both players.json and matches.json.

# 🧗 Climbing Tracker

A CLI-based climbing tracker that logs your boulder sessions, calculates consistency scores, and visualizes your progress through charts and an expedition system with unlockable difficulty levels.

---

## Features

- **Session logging** — register every route you attempt during a session, including the grade and whether you completed it
- **Score system** — each grade (V0–V9) has a point value; completing a route scores full points, failing scores half
- **Daily limit** — a cap per day prevents score manipulation and keeps progress honest
- **Expedition system** — set a difficulty goal (Easy, Medium, Hard, Impossible, Legendary) and track your climb to the top
- **Level unlocking** — complete an expedition to unlock harder difficulty tiers
- **Progress charts** — visualize your completed routes by grade, score over time, and current expedition progress

---

## How It Works

Your climber starts at the bottom of a mountain. Every session you log pushes them higher. Reach the top and a new, harder mountain awaits.

```
🧗 Mountain: [████████░░] 80.0%
```

---

## Getting Started

**Requirements**
- Python 3.10+
- matplotlib

**Install dependencies**
```bash
pip install matplotlib
```

**Run the app**
```bash
python cli.py
```

On first launch, you'll be asked for your name and your first expedition difficulty.

---

## Project Structure

```
climbing-tracker/
├── models.py      # Core data classes (User, Expedition, Session, Attempt)
├── storage.py     # JSON-based data persistence
├── graphics.py    # Chart generation with Matplotlib
├── cli.py         # Command-line interface
```

---

## Grade Score Table

| Grade | Points (completed) | Points (failed) |
|-------|--------------------|-----------------|
| V0    | 1                  | 0               |
| V1    | 2                  | 1               |
| V2    | 3                  | 1               |
| V3    | 4                  | 2               |
| V4    | 5                  | 2               |
| V5    | 6                  | 3               |
| V6    | 7                  | 3               |
| V7    | 8                  | 4               |
| V8    | 9                  | 4               |
| V9    | 10                 | 5               |

---

## Expedition Difficulty Levels

| Level      | Points Required | Unlocked by default |
|------------|-----------------|---------------------|
| Easy       | 100             | ✅                  |
| Medium     | 300             | ✅                  |
| Hard       | 500             | ✅                  |
| Impossible | 800             | 🔒                  |
| Legendary  | 1200            | 🔒                  |

---

## Roadmap

- [ ] GUI interface with Tkinter
- [ ] Mountain animation with character progression
- [ ] Outdoor climbing mode
- [ ] Multi-user support

---

Made with Python 🐍 by [gabrielpenov](https://github.com/gabrielpenov)

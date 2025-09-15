# Google Play Store Analytics Internship Project

## Overview
This repository contains the completed internship tasks for the *Build Real-time Google Play Store Data Analytics (Python)* project. The project analyzes Google Play Store app data using Python and visualizations, including time-restricted charts and interactive graphs. All tasks have been implemented as per the internship guidelines.

---

## Tasks Completed

### *Task 1: Grouped Bar Chart*
- Compares *average rating* and *total review count* for the *top 10 app categories by installs*.
- Filters:
  - Average rating ≥ 4.0
  - App size ≥ 10MB
  - Last update in *January*
- Time-restricted: *3 PM – 5 PM IST*
- Libraries used: pandas, matplotlib, numpy

---

### *Task 2: Interactive Choropleth Map*
- Visualizes *global installs by category* using Plotly.
- Filters:
  - Top 5 categories by installs
  - Categories not starting with A, C, G, S
  - Highlight categories with installs > 1M
- Time-restricted: *6 PM – 8 PM IST*
- Libraries used: pandas, plotly

---

### *Task 3: Dual-axis Chart*
- Compares *average installs* and *revenue* for *free vs. paid apps* within top 3 categories.
- Filters:
  - Installs ≥ 10,000
  - Revenue ≥ $10,000
  - Android version > 4.0
  - Size ≥ 15MB
  - Content rating = Everyone
  - App name ≤ 30 characters
- Time-restricted: *1 PM – 2 PM IST*
- Libraries used: pandas, matplotlib, numpy

---

### *Task 4: Time Series Line Chart*
- Shows trend of *total installs over time* segmented by category.
- Highlights periods of *>20% month-over-month growth*.
- Filters:
  - App name not starting with X, Y, Z
  - Category starts with E, C, B
  - Reviews > 500
  - App name does not contain “S”
  - Category translations:
    - Beauty → Hindi (सौंदर्य)
    - Business → Tamil (வணிகம்)
    - Dating → German (Dating)
- Time-restricted: *6 PM – 9 PM IST*
- Libraries used: pandas, plotly, pytz

---

### *Task 5: Bubble Chart*
- Analyzes *relationship between app size (MB) and average rating*, bubble size = installs.
- Filters:
  - Rating > 3.5
  - Valid categories: Game, Beauty, Business, Comics, Communication, Dating, Entertainment, Social, Event
  - Reviews > 500
  - App name does not contain “S”
  - Sentiment subjectivity > 0.5
  - Installs > 50k
  - Category translations (same as Task 4)
  - Game category highlighted in *pink*
- Time-restricted: *5 PM – 7 PM IST*
- Libraries used: pandas, matplotlib, seaborn, pytz

---

## Repository Structure

PlayStore_Analytics_Internship/

├── play_store_task1.py

├── play_store_task2.py

├── play_store_task3.py

├── play_store_task4.py

├── play_store_task5.py

├── requirements.txt

├── README.md
├── data/
│   ├── google_play_store_data.csv
│   └── user_reviews.csv

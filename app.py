from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta, date
import json
import os


app = Flask(__name__)

# Data structure to store notes
calendar_data = {}

fi_days = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]
fi_months = [
    "tammikuu", "helmikuu", "maaliskuu", "huhtikuu",
    "toukokuu", "kesäkuu", "heinäkuu", "elokuu",
    "syyskuu", "lokakuu", "marraskuu", "joulukuu"
]

DATA_FILE = "calendar_data.json"

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

calendar_data = load_data()

def format_date_box(date_obj):
    weekday = fi_days[date_obj.weekday()]
    month = fi_months[date_obj.month - 1]
    return f"{weekday} {date_obj.day}.{month}"

def get_week_dates(start_date):
    """Generate a list of dates for the current week and next week."""
    days = []
    for i in range(14):  # Two weeks (current + next)
        days.append(start_date + timedelta(days=i))
    return days

@app.route('/')
def calendar():
    today = date.today()
    week_dates = get_week_dates(today)

    # Prepare filtered data with only active days
    filtered_data = {
        d: calendar_data.get(d.strftime('%Y-%m-%d'), [])
        for d in week_dates if d.strftime('%Y-%m-%d') in calendar_data
    }

    # Find the day with the most participants
    max_day = None
    max_count = 0
    for day, people in filtered_data.items():
        if len(people) > max_count:
            max_count = len(people)
            max_day = day

    return render_template(
        "calendar.html",
        filtered_data=filtered_data,
        format_date_box=format_date_box,
        max_day=max_day
    )

@app.route('/add_note', methods=['POST'])
def add_note():
    date = request.form['date']
    name = request.form['name']

    if not name.isalpha():
        return redirect(url_for('calendar'))

    if date in calendar_data:
        if name not in calendar_data[date]:
            calendar_data[date].append(name)
    else:
        calendar_data[date] = [name]
    
    save_data(calendar_data)
    return redirect(url_for('calendar'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

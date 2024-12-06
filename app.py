from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta, date
import locale

# Set locale to Finnish
locale.setlocale(locale.LC_TIME, 'fi_FI.UTF-8')

app = Flask(__name__)

# Data structure to store notes
calendar_data = {}

def format_date_box(date_obj):
    """Format a date object as a short Finnish date (e.g., 'Ma 22.11')."""
    return date_obj.strftime('%a %d.%m').capitalize()

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

    # Validate that the name contains only letters
    if not name.isalpha():
        return redirect(url_for('calendar'))

    if date in calendar_data:
        if name not in calendar_data[date]:
            calendar_data[date].append(name)
    else:
        calendar_data[date] = [name]
    return redirect(url_for('calendar'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

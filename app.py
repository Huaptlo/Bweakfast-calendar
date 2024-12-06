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
    filtered_data = {
        d: calendar_data.get(d.strftime('%Y-%m-%d'), [])
        for d in week_dates
    }
    return render_template(
        "calendar.html",
        week_dates=week_dates,
        filtered_data=filtered_data,
        format_date_box=format_date_box
    )

@app.route('/add_note', methods=['POST'])
def add_note():
    date = request.form['date']
    name = request.form['name']
    if date in calendar_data:
        if name not in calendar_data[date]:
            calendar_data[date].append(name)
    else:
        calendar_data[date] = [name]
    return redirect(url_for('calendar'))

if __name__ == "__main__":
    app.run(debug=True)

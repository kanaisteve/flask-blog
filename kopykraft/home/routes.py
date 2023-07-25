from flask import render_template
from flask_login import current_user
from kopykraft.home import home
from datetime import date

# home page
@home.route('/')
@home.route('/home')
def index():
    return render_template('index.html', current_user=current_user)

# about page
@home.route('/about')
def about():
    return render_template('about.html', current_user=current_user)

# services page
@home.route('/services')
def services():
    return render_template('services.html', current_user=current_user)

# return json data
@home.route('/date')
def get_current_date():
    return {"Date": date.today()}

# return json data
@home.route('/engineers')
def get_engineers():
    engineers = {
        "Kanai": "Frontend Engineer",
        "Peter": "Backend Engineer",
        "Katumbi": "Software Engineer",
        "Victor": "Cybersecurity",
    }

    return engineers

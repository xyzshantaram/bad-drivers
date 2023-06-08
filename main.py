import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for
import itertools

def create_app():
    app = Flask(__name__)
    
    # Create a connection to the SQLite database
    conn = sqlite3.connect('drivers.db')
    c = conn.cursor()

    # Create the drivers table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS drivers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_plate TEXT,
                    place TEXT,
                    time INTEGER,
                    description TEXT,
                    video TEXT,
                    city TEXT
                )''')
    conn.commit()
    c.close()
    conn.close()

    # Load the cities list from the provided JSON file
    cities_url = 'https://cdn.jsdelivr.net/gh/nshntarora/Indian-Cities-JSON/cities.json'
    cities_response = requests.get(cities_url).json()
    key = lambda x:x['state']
    grouped = itertools.groupby(sorted(cities_response, key=key), key=key)

    cities_names = []
    for _, c in grouped:
        s = list(sorted(c, key=lambda x: x['name']))
        for city in s:
            cities_names.append(f"{city['name']}, {city['state']}")

    # Helper function to validate if a city is in the cities list
    def validate_city(city):
        return city in cities_names

    # Index route - show form to add a driver
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.j2', cities=cities_names)

    # Add a driver route - handle form submission
    @app.route('/drivers', methods=['POST'])
    def add_driver():
        conn = sqlite3.connect('drivers.db')
        c = conn.cursor()
        license_plate = request.form['license_plate']
        place = request.form['place']
        time = request.form['time']
        description = request.form['description']
        video = request.form['video']
        city = request.form['city']

        if not validate_city(city):
            return render_template('error.j2', error='Invalid city')

        # Insert the driver details into the database
        c.execute("INSERT INTO drivers (license_plate, place, time, description, video, city) VALUES (?, ?, ?, ?, ?, ?)",
                (license_plate, place, time, description, video, city))
        conn.commit()
        c.close()
        conn.close()
        return redirect(url_for('index'))

    # List all drivers for a particular city
    @app.route('/drivers', methods=['GET'])
    def drivers():
        conn = sqlite3.connect('drivers.db')
        c = conn.cursor()
        city = request.args.get('city')

        if not validate_city(city):
            return render_template('error.j2', error='Invalid city')

        c.execute("SELECT license_plate, city, description, video, place, time FROM drivers WHERE city=?", (city,))
        drivers_list = c.fetchall()
        c.close()
        conn.close()
        return render_template('drivers.j2', drivers=drivers_list, city=city)

    # Show a random driver from a city
    @app.route('/drivers/random', methods=['GET'])
    def random_driver():
        conn = sqlite3.connect('drivers.db')
        c = conn.cursor()
        city = request.args.get('city')
        if not validate_city(city):
            return render_template('error.j2', error='Invalid city')

        c.execute("SELECT license_plate, city, description, video, place, time FROM drivers WHERE city=? order by random() limit 1;", (city,))
        driver = c.fetchone()
        c.close()
        conn.close()
        return render_template('random.j2', driver=driver, city=city)

    return app
# Calendar Mood App

This app tracks your daily moods on a colorized calendar.

Deployed Link: https://calendar-mood.herokuapp.com/


## Getting Started
Instructions on how to get running on your local machine:

### Installation and Set Up
1. Fork and clone this repository.
2. Create a virtual environment. In terminal: `virtualenv calendar-app` (or whatever you want to call "calendar-app") Install virtualenvwrapper before  this step if you do not already have it (https://pypi.python.org/pypi/virtualenvwrapper).
3. Install requirements with: `pip install -r requirements.txt` in terminal.
4. Create your calendar-app database in terminal using: `createdb calendar-db` and run `python manage.py db upgrade`. Install Postgres before this step if you do not already have it (https://www.postgresql.org/download/).   
5. Set your local environment variables for a secret key for the CSRF token protection in the forms. While in your virtualenv, run `[subl,atom,code] $VIRTUAL_ENV/bin/postactivate` in terminal, depending on your text editor preferences/setup. Example: `code $VIRTUAL_ENV/bin/postactivate` to open up the file in VSCode. Add `export SECRET_KEY='YOUR_SECRET_KEY'` to the file and save.
6. Start the server using `python app.py` in terminal.
7. View the page in your browser at `localhost:5000`


## Built With  
* Python Flask, Postgres
  * Logins use flask-login
  * Forms use WTForms
  * Password hashing uses bcrypt
  * ORM for Python used SQLAlchemy via flask-sqlalchemy  

**Calendar:**  

* FullCalendar (https://fullcalendar.io/)  
* Moment.js (http://momentjs.com/)


**Styling:**  

* SemanticUI (https://semantic-ui.com/)
* Color - Python color representations manipulation (https://github.com/vaab/colour)
* JQuery Palette Color Picker (https://github.com/carloscabo/jquery-palette-color-picker)
* Photos from Unsplash (https://unsplash.com/)
	* Home Page Image (https://unsplash.com/photos/Cy4jIcJ7w0Y)
	* About Page Image (https://unsplash.com/photos/P3VNWILRbzw)


**Data Visualization:**  

* D3 Data-Driven Documents (https://d3js.org/)


## Features
* Authentication for users; users can change their passwords later.
* Ability to add or modify dates and view a particular date's info. Modifying a date also updates the timestamp to the current UTC time.


## Possible items to add or work on
* Writing and implementing tests
* D3 visualizations with user/group data
* Ability to customize colors based on moods (not just picking a color for the day, as it currently is). 
* Adding optional user info fields, calls to an API/location integration for weather for that day.
* Sharing your personal calendar with permissions.
* Modify timestamps to be saved in local time and not UTC.
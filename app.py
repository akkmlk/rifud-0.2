import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mysql
from dotenv import load_dotenv
from routes.api_food_waste import food_waste_api
from routes.ui_pages import pages
load_dotenv()

app = Flask(os.environ.get("APP_NAME"))
app.secret_key = os.environ.get("SECRET_KEY")
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_PORT'] = int(os.environ.get("MYSQL_PORT"))
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] =  os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_UNIX_SOCKET"] = None
mysql.init_app(app)

app.register_blueprint(food_waste_api)
app.register_blueprint(pages)

if __name__ == "__main__":
    app.run(debug=True)
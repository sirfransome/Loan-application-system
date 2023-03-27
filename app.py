import os
from flask import Flask
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('database_url')
app.config['API_TITLE'] = "Loan Application System"
app.config['API_VERSION'] = "v1"

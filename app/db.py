from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables
load_dotenv()

# Database configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def close_db_connection(db):
    db.close()

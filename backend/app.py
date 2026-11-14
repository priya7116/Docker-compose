from flask import Flask, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "root123"),
        database=os.environ.get("DB_NAME", "studentdb")
    )

def initialize_database():
    for i in range(10):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS studentdb")
            cursor.execute("USE studentdb")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    course VARCHAR(100)
                )
            """)
            cursor.execute("SELECT COUNT(*) FROM students")
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.execute("INSERT INTO students (name, course) VALUES ('Asha', 'Docker'), ('Rahul', 'Python')")
            connection.commit()
            cursor.close()
            connection.close()
            print("Database ready!")
            return
        except Exception as error:
            print("Waiting for MySQL:", error)
            time.sleep(5)
    raise Exception("Database initialization failed")

@app.route("/")
def home():
    return jsonify({"message": "Student Backend is running"})

@app.route("/students")
def students():
    connection = get_connection()
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM students")
            result = cursor.fetchall()
        return jsonify(result)
    finally:
        connection.close()

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
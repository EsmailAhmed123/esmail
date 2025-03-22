import sqlite3
import random

DB_FILE = "timetable.db"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = ["08:00 - 10:00", "11:00 - 13:00", "14:00 - 17:00"]

def init_db():
    # Create database tables
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lecturers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lecturer_id INTEGER,
        lesson_name TEXT NOT NULL,
        FOREIGN KEY (lecturer_id) REFERENCES lecturers(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lecturer_id INTEGER,
        lesson_name TEXT NOT NULL,
        day TEXT NOT NULL,
        time_slot TEXT NOT NULL,
        FOREIGN KEY (lecturer_id) REFERENCES lecturers(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lecturer_name TEXT UNIQUE NOT NULL
    )""")

    connection.commit()
    connection.close()

def request_lecturer_addition(name):
    # A function to facilitate lecture addition to the system request
    connection = sqlite3.connect(DB_FILE) # Connect to the database
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO requests (lecturer_name) VALUES (?)", (name,))
        connection.commit()
        print(f"Request for {name} to be added has been submitted.")
    except sqlite3.IntegrityError:
        print("Request already exists.")
    connection.close()

def approve_lecturer(name):
    # Requests for a lecturer to be approved
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Check if lecturer is already approved
    cursor.execute("SELECT id FROM lecturers WHERE name = ?", (name,))
    if cursor.fetchone():
        print(f"Lecturer '{name}' is already approved.")
        connection.close()
        return  # Exit early if already approved

    # Check if lecturer has a pending request
    cursor.execute("SELECT lecturer_name FROM requests WHERE lecturer_name = ?", (name,))
    result = cursor.fetchone()

    if not result:
        print(f"No pending request found for lecturer '{name}'.")
    else:
        cursor.execute("INSERT INTO lecturers (name) VALUES (?)", (name,))
        cursor.execute("DELETE FROM requests WHERE lecturer_name = ?", (name,))
        connection.commit()
        print(f"Lecturer '{name}' has been approved and added to the system.")

    connection.close()

def add_lesson(lecturer_name, lessons):
    # Add lessons to the lecturer's slot, according to time of the day
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM lecturers WHERE name = ?", (lecturer_name,))
    result = cursor.fetchone()
    if not result:
        print("Error: Lecturer not found. Request approval first!")
        return

    lecturer_id = result[0]
    for lesson in lessons:
        cursor.execute("INSERT INTO lessons (lecturer_id, lesson_name) VALUES (?, ?)", (lecturer_id, lesson))

    connection.commit()
    connection.close()
    print("Lessons added successfully.")

def make_timetable(lecturer_name):
    # Generate a timetable for the system to be used
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM lecturers WHERE name = ?", (lecturer_name,))
    result = cursor.fetchone()
    if not result:
        print("Error: Lecturer not found")
        return
    lecturer_id = result[0]

    cursor.execute("SELECT lesson_name FROM lessons WHERE lecturer_id = ?", (lecturer_id,))
    lessons = [row[0] for row in cursor.fetchall()]
    if not lessons:
        print("No lessons found for this lecturer.")
        return

    assigned = []
    available_slots = [(day, time) for day in DAYS for time in TIME_SLOTS]
    random.shuffle(available_slots)

    for lesson in lessons:
        if not available_slots:
            print("Error: Not enough time slots for all lessons!")
            break
        day, time_slot = available_slots.pop()
        cursor.execute("INSERT INTO timetable (lecturer_id, lesson_name, day, time_slot) VALUES (?, ?, ?, ?)", (lecturer_id, lesson, day, time_slot))
        assigned.append((day, time_slot, lesson))

    connection.commit()
    connection.close()
    print("Timetable generated successfully.")
    display_timetable(lecturer_name)

def display_timetable(lecturer_name):
    # This function will display the made timetable
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM lecturers WHERE name = ?", (lecturer_name,))
    result = cursor.fetchone()
    if not result:
        print("Lecturer not found.")
        return

    lecturer_id = result[0]
    cursor.execute("SELECT day, time_slot, lesson_name FROM timetable WHERE lecturer_id = ? ORDER BY day", (lecturer_id,))
    timetable = cursor.fetchall()
    if not timetable:
        print("No timetable found for this lecturer.")
        return

    print(f"\nTimetable for {lecturer_name}:")
    for day, time, lesson in timetable:
        print(f"{day} ({time}): {lesson}")

    connection.close()

if __name__ == "__main__":
    init_db()
    print("Timetable System")
    action = input("Do you want to (1) Request to be added, (2) Approve Lecturer, (3) Add Lessons, (4) Generate Timetable, (5) View Timetable? ")
    name = input("Enter lecturer Name: ")
    
    if action == "1":
        request_lecturer_addition(name)
    elif action == "2":
        approve_lecturer(name)
    elif action == "3":
        lessons = input("Enter lessons (comma-separated): ").split(", ")
        add_lesson(name, lessons)
    elif action == "4":
        make_timetable(name)
    elif action == "5":
        display_timetable(name)
    else:
        print("Invalid option. Choose 1, 2, 3, 4, or 5")
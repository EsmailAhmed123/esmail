# Esmail
A simple timetable system developed using a Python script.
A lecturer is supposed to ask the timetabler to add the number of students, allocate a class, and then lessons.

## **How to Clone the App**

- **Via HTTPS:**  
  ```bash
  git clone https://github.com/EsmailAhmed123/esmail.git
  ```
- **Via SSH:**  
  ```bash
  git clone git@github.com:EsmailAhmed123/esmail.git
  ```

## **Setup Instructions**

### **Navigate to Your Project Directory**
```bash
cd path/to/project
```

### **Set Up a Virtual Environment**

- **On Linux/MacOS:**  
  ```bash
  python3 -m venv venv
  ```
- **On Windows:**  
  ```bash
  python -m venv venv
  ```

### **Activate the Virtual Environment**

- **On Linux/MacOS:**  
  ```bash
  source venv/bin/activate
  ```
- **On Windows:**  
  ```bash
  venv\Scripts\activate
  ```

### **Install Dependencies**
```bash
pip install Flask Flask-SQLAlchemy
```

---

## **Manually Adding Lecturers (Interactive Python)**
To manually add a lecturer, open a Python interactive shell:

```bash
python
```

Then, run the following commands:
```python
from app import db, Lecturer

db.create_all()  # Ensures database tables exist

new_lecturer = Lecturer(name="John Doe", email="johndoe@example.com")
db.session.add(new_lecturer)
db.session.commit()

print("Lecturer added successfully!")
```

---

## **API Endpoints & cURL Commands**

### **1️⃣ Create a Timetable Request**
```bash
curl -X POST http://127.0.0.1:5000/request/create \
     -H "Content-Type: application/json" \
     -d '{"lecturer_id": 1, "unit_name": "Software Engineering", "student_count": 30, "room_available": true}'
```

### **2️⃣ List All Requests**
```bash
curl -X GET http://127.0.0.1:5000/request/list
```

### **3️⃣ Approve a Request**
```bash
curl -X PATCH http://127.0.0.1:5000/request/approve/1
```

### **4️⃣ Reject a Request**
```bash
curl -X PATCH http://127.0.0.1:5000/request/reject/1
```

---

## **Run the Flask App**
```bash
python app.py
```

Now, your timetable system is up and running! 🚀


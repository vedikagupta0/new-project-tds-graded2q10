from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# Enable CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CSV data on startup
students_data = []

with open("students.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row["studentId"] = int(row["studentId"])  # Convert ID to int
        students_data.append(row)

@app.get("/api")
def get_students(request: Request):
    class_filters = request.query_params.getlist("class")
    
    if not class_filters:
        return {"students": students_data}
    
    filtered_students = [student for student in students_data if student["class"] in class_filters]
    return {"students": filtered_students}

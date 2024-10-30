# main.py

from bson import ObjectId
from fastapi import FastAPI, HTTPException
from .models import Student
from .schema import StudentCreate, StudentResponse
from .database import init_database

app = FastAPI()

@app.on_event("startup")
async def startup():
    init_database()
    print("Bunnet and MongoDB connection established")

# @app.post("/students/", response_model=StudentResponse)
# async def create_student(student: StudentCreate):
#     result = await Student.create(**student.dict())
#     return StudentResponse(id=str(result.id), **result.dict())
@app.post("/students/", response_model=StudentResponse)
async def create_student(student: StudentCreate):
    # Create a new Student document
    new_student = Student(**student.dict())
    # Save the new Student document to the database
    new_student.save()
    return StudentResponse(id=str(new_student.id), **student.dict())

@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str):
    student =   Student.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student_data = student.dict()
    student_data["id"] = str(student_data.pop("_id"))  # Convert ObjectId to string
    return StudentResponse(**student_data)



# async def get_student(student_id: str):
#     student = await Student.find_by_id(student_id)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return StudentResponse(id=str(student.id), **student.dict())

@app.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(student_id: str, student_data: StudentCreate):
    student = await Student.find_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await student.update(**student_data.dict())
    return StudentResponse(id=student_id, **student_data.dict())

@app.delete("/students/{student_id}")
async def delete_student(student_id: str):
    student =   Student.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.delete()
    return {"message": "Student deleted successfully"}

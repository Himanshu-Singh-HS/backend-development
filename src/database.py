# database.py

from pymongo import MongoClient
from bunnet import init_bunnet
from .config import MONGODB_URI, DB_NAME
from .models import  Student 

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

def init_database():
    init_bunnet(database=db, document_models=[Student])

 





# from fastapi import FastAPI, HTTPException
# from bunnet import Document, init_bunnet
# from pymongo import MongoClient
# from pydantic import BaseModel
# from bson import ObjectId

# app = FastAPI()

# # MongoDB connection URI and settings
# MONGODB_URI = "mongodb://localhost:27017"
# DB_NAME = "himanshu"

# # Define Bunnet document model
# class Student(Document):
#     name: str
#     age: int
#     grade: str

# class StudentCreate(BaseModel):
#     name: str
#     age: int
#     grade: str

# class StudentResponse(BaseModel):
#     id: str
#     name: str
#     age: int
#     grade: str

# @app.on_event("startup")
# async def startup():
#     # Initialize MongoDB client
#     client = MongoClient(MONGODB_URI)
#     db = client[DB_NAME]
    
#     # Initialize Bunnet with the database object and document models
#     init_bunnet(database=db, document_models=[Student])
#     print("Bunnet and MongoDB connection established")

# @app.post("/students/", response_model=StudentResponse)
# async def create_student(student: StudentCreate):
#     result = await Student.create(**student.dict())
#     return StudentResponse(id=str(result.id), **result.dict())

# @app.get("/students/{student_id}", response_model=StudentResponse)
# async def get_student(student_id: str):
#     student = await Student.find_by_id(student_id)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return StudentResponse(id=str(student.id), **student.dict())

# @app.put("/students/{student_id}", response_model=StudentResponse)
# async def update_student(student_id: str, student_data: StudentCreate):
#     student = await Student.find_by_id(student_id)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#     await student.update(**student_data.dict())
#     return StudentResponse(id=student_id, **student_data.dict())

# @app.delete("/students/{student_id}")
# async def delete_student(student_id: str):
#     student = await Student.find_by_id(student_id)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#     await student.delete()
#     return {"message": "Student deleted successfully"}

from fastapi import APIRouter, HTTPException
from models import Student
from schema import StudentCreate, StudentResponse
from bson import ObjectId

student_router = APIRouter()

@student_router.post("/", response_model=StudentResponse)
async def create_student(student: StudentCreate):
    new_student = Student(**student.dict())
    await new_student.save()
    return StudentResponse(id=str(new_student.id), **student.dict())

@student_router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str):
    student = await Student.find_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentResponse(id=str(student.id), **student.dict())

@student_router.put("/{student_id}", response_model=StudentResponse)
async def update_student(student_id: str, student_data: StudentCreate):
    student = await Student.find_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await student.update(**student_data.dict())
    return StudentResponse(id=student_id, **student_data.dict())

@student_router.delete("/{student_id}")
async def delete_student(student_id: str):
    student = await Student.get(student_id)   
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await student.delete()
    return {"message": "Student deleted successfully"}







# from fastapi import APIRouter, HTTPException
# from .schemas import StudentCreate, StudentResponse
# from .services import create_student, get_student, update_student, delete_student

# router = APIRouter()

# @router.post("/students/", response_model=StudentResponse)
# async def create_student_endpoint(student: StudentCreate):
#     student = await create_student(student)
#     return StudentResponse(id=str(student.id), **student.dict())

# @router.get("/students/{student_id}", response_model=StudentResponse)
# async def get_student_endpoint(student_id: str):
#     student = await get_student(student_id)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return StudentResponse(id=str(student.id), **student.dict())

# @router.put("/students/{student_id}", response_model=StudentResponse)
# async def update_student_endpoint(student_id: str, student_data: StudentCreate):
#     student = await update_student(student_id, student_data)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return StudentResponse(id=str(student.id), **student.dict())

# @router.delete("/students/{student_id}")
# async def delete_student_endpoint(student_id: str):
#     student = await delete_student(student_id)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return {"message": "Student deleted successfully"}



# from fastapi import APIRouter
# from services import create_student, get_student, update_student, delete_student
# from schemas import StudentCreate, StudentResponse

# student_router = APIRouter()

# @student_router.post("/", response_model=StudentResponse)
# async def create(student: StudentCreate):
#     new_student = await create_student(student)
#     return StudentResponse(id=str(new_student.id), **student.dict())

# @student_router.get("/{student_id}", response_model=StudentResponse)
# async def read(student_id: str):
#     student = await get_student(student_id)
#     return StudentResponse(id=str(student.id), **student.dict())

# @student_router.put("/{student_id}", response_model=StudentResponse)
# async def update(student_id: str, student_data: StudentCreate):
#     updated_student = await update_student(student_id, student_data)
#     return StudentResponse(id=str(updated_student.id), **student_data.dict())

# @student_router.delete("/{student_id}")
# async def delete(student_id: str):
#     return await delete_student(student_id)

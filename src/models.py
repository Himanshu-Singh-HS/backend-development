from bunnet import Document
from pydantic import BaseModel

class Student(Document):
    name: str
    age: int
    grade: str
    class Settings:
        name: str = "drafting_report_registry"
        use_state_management = True
        state_management_save_previous = True
        
    pass

 

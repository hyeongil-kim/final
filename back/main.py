import json
from fastapi import FastAPI, HTTPException, status
import uvicorn
from model import Course

app = FastAPI()

data_file = "courses.json" 


@app.get("/courses")
def get_courses() -> dict | list:
    try:
        with open("courses.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"message": str(e)}

@app.post("/courses")
def add_course(course: Course) -> dict:
    try:
        with open("courses.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        data.append(course.model_dump())
        
        with open("courses.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        return {"message": "201 Created", "course": course.model_dump()}
    except Exception as e:
        return {"message": str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''
1. Endpoint to get a list of all available courses. This endpoint needs to support 3 modes of
sorting: Alphabetical (based on course title, ascending), date (descending) and total course
 rating (descending). Additionaly, this endpoint needs to support optional filtering of courses
based on domain.

2. Endpoint to get the course overview.

3. Endpoint to get specific chapter information.

4. Endpoint to allow users to rate each chapter (positive/negative), while aggregating all ratings
for each course.
'''


from fastapi import FastAPI
from pydantic import BaseModel

from app import db_manager

app = FastAPI()
db_ref = db_manager.mongo_db()

@app.get("/courses")
def read_all_courses():
    courses = db_ref.find_all_courses()
    return courses

@app.get("/course/overview/{course_name}")
def read_course_overview(course_name:str):
    course_overview = db_ref.get_course_overview(course_name)
    return course_overview

@app.get("/chapter/information/{chapter_name}")
def read_chapter_information(chapter_name:str):
    chapter_info = db_ref.get_chapter_information(chapter_name)
    return chapter_info


class chapter_rate_request(BaseModel):
    user_id : str
    chapter_name: str
    rating : str

@app.post("/chapter/rate")
def rate_chapter(rate_request: chapter_rate_request):
    return db_ref.update_chapter_rating(rate_request.chapter_name, rating=rate_request.rating, user_id=rate_request.user_id)
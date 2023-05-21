'''
author: Ujjal Das
github: ujjaldas132
date: May, 2023
<p>

'''
from fastapi.testclient import TestClient
from app.app_driver import app


client = TestClient(app)

def test_courses():
    response = client.get("/courses")
    assert response.status_code == 200
    course_list = response.json()
    expected_course_list = ["Computer Vision Course", "Highlights of Calculus", "Introduction to Deep Learning", "Introduction to Programming"]
    course_list_from_response = []
    for doc in course_list:
        print(type(doc), doc["name"])
        course_list_from_response.append(doc["name"])
    for i in range(4) :
        assert expected_course_list[i] == course_list_from_response[i]


def test_course_overview():
    response = client.get("/course/overview/Introduction to Deep Learning")
    assert response.status_code == 200
    course_overview = response.json()
    print(course_overview)
    assert course_overview["overview"] == "Course lectures for MIT Introduction to Deep Learning."


def test_chapter_info():
    response = client.get("/chapter/information/Image Classification")
    assert response.status_code == 200
    course_overview = response.json()
    assert course_overview["info"] == "Computer Vision Course"

def test_rating():
    chapter_name = "Image Classification"
    rating_payload = {
        "user_id" : "kimo",
        "rating" : "positive",
        "chapter_name": chapter_name
    }
    response = client.post("/chapter/rate", json=rating_payload)
    assert response.json()["rating"] != None
    response = client.get("/courses")
    correspnding_course = response.json()[0]
    course_rating_list = correspnding_course["ratings"]
    found_rating_against_the_course = False
    total_rating_of_course = 0
    for doc in course_rating_list:
        if doc["name"] == chapter_name:
            found_rating_against_the_course = True
        total_rating_of_course += doc["rating"]
    assert found_rating_against_the_course
    assert total_rating_of_course == correspnding_course["rating"]
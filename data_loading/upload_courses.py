'''
author: Ujjal Das
github: ujjaldas132
date: May, 2023
<p>

'''

import json
import pymongo

import app.helper

f = open('courses.json')
data = json.load(f)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
course_db = myclient["kimo"]

for course in data:
    course_collection = course_db["courses"]
    course_name = course['name']
    date_of_course = course['date']
    description_of_course = course['description']
    domain_of_course = course['domain']

    couse_doc = {'name' : course_name,
                 'date' : date_of_course,
                 'description' : description_of_course,
                 'domain' : domain_of_course,
                 'ratings' : [],
                 'rating' : 0
                 }
    course_collection.insert_one(couse_doc)
    for chapter in course['chapters']:
        chapter_name = chapter['name']
        chapter_info = chapter['text']
        print(course_name, chapter_name, chapter_info)
        chapter_doc = {
            "name" : chapter_name,
            "info" : chapter_info,
            'ratings': [],
            'rating': 0,
            "course" : course_name
        }
        chapter_collection_split_name = app.helper.get_chapter_collection_name(chapter_name)
        chapter_collection = course_db[chapter_collection_split_name]
        chapter_collection.insert_one(chapter_doc)

# Closing file
f.close()
myclient.close()
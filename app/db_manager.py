'''
author: Ujjal Das
github: ujjaldas132
date: May, 2023
<p>

'''
from datetime import datetime
import json
import pymongo
from pymongo.operations import UpdateOne
from app import helper

class mongo_db:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.myclient["kimo"]
        self.course_collection = self.database["courses"]

    def find_all_courses(self):
        # all courses
        all_courses = self.course_collection.find().sort([("name", pymongo.ASCENDING), ('date', pymongo.DESCENDING), ("rating", pymongo.DESCENDING)])
        l = []
        for doc in all_courses:
            doc.pop("_id")
            doc["date"] = str(datetime.fromtimestamp(doc["date"]).date())
            l.append(doc)
        json_string = json.dumps(l)
        return json.loads(json_string)

    def get_course_overview(self, course_name):
        #overView of a course
        course_doc = self.course_collection.find_one({"name": course_name})
        json_str = {
            "overview" :course_doc["description"],
            "rating" : helper.get_rating_from_Number( course_doc["rating"]),
            "starting_date" : str(datetime.fromtimestamp(course_doc["date"]).date()),
            "domain" : course_doc["domain"]
        }
        return json.loads(json.dumps(json_str))

    def get_chapter_information(self, chapter_name):
        #specific chapter information
        collection_name = helper.get_chapter_collection_name(chapter_name)
        chapter = self.database.get_collection(collection_name).find_one({"name":chapter_name})
        chapter.pop("_id")
        chapter.pop("ratings")
        chapter["rating"] = helper.get_rating_from_Number(chapter["rating"])
        return json.loads(json.dumps(chapter))

    def update_chapter_rating(self,chapter_name, user_id, rating:str):

        collection_name = helper.get_chapter_collection_name(chapter_name)
        num_rating = helper.get_numeric_rating(rating)

        bulk_operations = []
        # Remove existing rating if it exists
        remove_operation = UpdateOne(
            {"name": chapter_name},
            {"$pull": {"ratings": {"_id": user_id}}},
        )
        bulk_operations.append(remove_operation)
        # If the rating doesn't exist, create a new document
        update_operation = UpdateOne(
            {"name": chapter_name},
            {"$addToSet": {"ratings": {"_id": user_id, "rating": num_rating}}},
            upsert=True
        )
        bulk_operations.append(update_operation)
        # now recalculate the aggregated chapter rating
        reset_chapter_rating = UpdateOne(
            {"name": chapter_name},
            [
                {
                    "$set": {
                        "rating": {"$sum": "$ratings.rating"}
                    }
                }
            ]
        )
        bulk_operations.append(reset_chapter_rating)
        self.database[collection_name].bulk_write(bulk_operations)

        #Now we have to calculate the course rating
        # first update the pointer for chapter rating then calculate the aggregated rating
        chapter_doc = self.database[collection_name].find_one({"name":chapter_name})
        course_name = chapter_doc["course"]
        new_rating = chapter_doc["rating"]

        bulk_operations = []
        # remove if exists
        remove_operation = UpdateOne(
            {"name": course_name},
            {"$pull": {"ratings": {"name": chapter_name}}},
        )
        bulk_operations.append(remove_operation)
        # If the rating doesn't exist, create a new document
        update_operation = UpdateOne(
            {"name": course_name},
            {"$addToSet": {"ratings": {"name": chapter_name, "rating": new_rating}}},
            upsert=True
        )
        bulk_operations.append(update_operation)
        # calculate aggregated rating
        reset_course_rating = UpdateOne(
            {"name": course_name},
            [
                {
                    "$set": {
                        "rating": {"$sum": "$ratings.rating"}
                    }
                }
            ]
        )
        bulk_operations.append(reset_course_rating)
        self.course_collection.bulk_write(bulk_operations)
        return json.loads(json.dumps({
            "status" : "done",
            "rating": helper.get_rating_from_Number(new_rating)}))

if __name__ == '__main__':
    db = mongo_db()
    db.find_all_courses()
    db.update_chapter_rating("CNN Architectures", "user1", "negative")
    db.update_chapter_rating("CNN Architectures", "user2", "positive")
    db.update_chapter_rating("CNN Architectures", "user3", "negative")
    db.update_chapter_rating("CS50 2021 in HDR - Cybersecurity", "user3", "positive")
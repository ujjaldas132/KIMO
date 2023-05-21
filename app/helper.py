'''
author: Ujjal Das
github: ujjaldas132
date: May, 2023
<p>

'''

def get_numeric_rating(rating:str):
    rating = rating.lower()
    return 1 if rating=="positive" else -1

def get_rating_from_Number(rating:int) :
    if rating == 0:
        return "Neutral"
    elif rating == -1:
        return "Negative"
    return "Positive"

def get_chapter_collection_name(chapter_name:str):
    return "chapter_" + chapter_name[0:1].lower()
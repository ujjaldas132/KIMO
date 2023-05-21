##### Table of Contents  
- [Data Loading](#dataLoading)  
- [FastApi](#fastapi)  
- [Testing](#testing)  
   



<a name="dataLoading"/>

# Data Loading

- code you can find inside `data_loading` package.

To store the data in mongodb, I have created 27 collections(Assuming I have atleast one course starting with each alphabet)
- 1 for Course
- 26 for chapter, eg. chapter_a, chapter_b, chapter_c
  - This is an automated process. It creates the collection if it doesnot exist, and require to store next chapter information.
  - As we have a huge number of chapters . So instead of storing them in same collection I splited them into multiple collections.
  - The partition is based on the starting letter of the chapter, let say if the course name is "Image Processing", then it will part of collection "chapter_i"


### Schema
#### sample Schema for course
```
{
    _id: ObjectId("646a19d2abdd7fe4e1601759"),
    name: 'Introduction to Programming',
    date: 1659906000,
    description: `An introduction to programming using .......`,
    ratings: [ { name: 'CS50 2021 in HDR - Cybersecurity', rating: 1 } ],
    rating: 1,
    domain:['programming'],
  }
```
in the `ratings` array we store the overall rating of each chapter comes under the course.
and `rating` is for the aggregated rating for the course.<br>
for rating we are store numbers instead of text just for calculation. the conversion is
<br>`positive` : 1<br>
`negative` : -1 <br>
`neutral` : 0 <br>


#### Sample Schema for Chapter
```
{
    _id: ObjectId("646a544fb4ce63f7734a664a"),
    name: 'CNN Architectures',
    info: 'Computer Vision Course. CS231n L10 Recurrent neural networks',
    ratings: [ { _id: '4', rating: 1 } ],
    rating: 1,
    course: 'Computer Vision Course'
  }
```

Here in `ratings` we are storing ratings against each users.<br>
`_id` is the `user_id`, so that a user cant make duplicate rating.




<a name="fastapi"/>

# FASTAPI codes
  Code is present inside `app` package.<br>
- `app_driver` is the main file.
- `db_manager` is the class to handle all the db connections
- `helper` is for util functions

`python -m uvicorn app.app_driver:app --reload` is the command to run the server

#### Sample urls
##### Get Request for problem No 1
- ```http://127.0.0.1:8000/courses```

```commandline
[
  {
    "name": "Computer Vision Course",
    "date": "2017-08-11",
    "description": "Computer Vision has become ubiquitous in our society,............",
    "domain": [
        "computer vision",
        "artificial intelligence"
    ],
    "ratings": [
      {
        "name": "Image Classification",
        "rating": 1
      }
    ],
    "rating": 1
  },
  {
    "name": "Highlights of Calculus",
    "date": "2018-06-28",
    "description": "Highlights of Calculus is a series of short videos...............................",
    "domain": [
        "mathematics"
    ],
    "ratings": [],
    "rating": 0
  },
  {
    "name": "Introduction to Deep Learning",
    "date": "2022-05-26",
    "description": "Course lectures for MIT Introduction to Deep Learning.",
    "domain": [
        "artificial intelligence"
    ],
    "ratings": [],
    "rating": 0
  },
  {
    "name": "Introduction to Programming",
    "date": "2022-08-08",
    "description": "An introduction to programming using a language called Python................................",
    "domain": [
        "programming"
    ],
    "ratings": [],
    "rating": 0
  }
]

```

##### Get Request and response for problem No 2
- ```http://127.0.0.1:8000/course/overview/Introduction%20to%20Programming```
 
 ```
{
"overview": "An introduction to how to read an ....",
"rating": "Positive",
"starting_date": "2022-08-08",
"domain": [
"programming"
]
}
```
##### Get Request and response for problem No 3
- ```http://127.0.0.1:8000/chapter/information/Big%20Picture%20of%20Calculus```
```
{
"name": "Big Picture of Calculus",
"info": "Highlights of Calculus",
"rating": "Neutral",
"course": "Highlights of Calculus"
}
```
##### Post request for problem no 4
`url` : ```http://127.0.0.1:8000/chapter/rate```
<br>`payload` : 
```
{
	"chapter_name": "CNN Architectures",
	"rating" : "positive",
	"user_id": "4"
}
```

 `response` <br>
```
{
    "status": "done",
    "rating": "Positive"
}
```


<a name="testing"/>

## Testing

All test code you can find inside `test` package.
Automated tests are done using `pytest`
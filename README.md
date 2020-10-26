# Full Stack API Final Project

## Introduction

This Trivia project is designed to test the knowledge of the user. Additionally you everyone is allowed to create new Trivia questions. You can train with questions, answer them and see immidiadly the correct answer. If you have enough knowledge you can play a quiz and gain score. In this project an API was created with following functionality:

1) Display either all questions or only for a specific category. Question, answer, difficulty level and category are shown. The results are paginated.
2) Delete questions.
3) Create new questions.
4) Search for a string/substring in questions and get a paginated output.
5) Play a quiz game.


## Getting started
### Installation
Python3, pip, node and npm must be installed.


#### Frontend
The NPM uses package.json in `/frontend` to manage software dependencies. Open terminal an run:

    npm install



#### Backend
Go to `/backend` and run in terminal:

    pip install -r requirements.txt


## Running Frontend
The frontend app was build. Then open terminal and run:

    npm start

The browser should automatically load [http://localhost:3000](http://localhost:3000). Otherwise use the url in the browser manually.


## Running Backend

Make sure you are using the virtual environment in the `/backend`. Run the server with following lines in the terminal:

    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run

## Testing
For testing, run

    createdb trivia_test
    psql trivia_test < trivia.psql
    python test_flaskr.py


## API Documentation
### URLs and ports
Base URL: The application is hosted locally.

Frontend: `http://localhost:3000`

Backend: `http://localhost:5000`


### Error handling

Errors are returned as JSON having the format as shown below:

    {
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
    }


The following three types of errors are available for the API:

* 404 : Ressource Not Found
* 422 : Unprocessable Entity
* 400 : Bad Request


### Ressource Endpoint Library

#### GET /categories

* Returns a list of categories.
* Sample: `curl http://127.0.0.1:5000/categories` 

JSON return:

    {
        'success': true,
        'categories': {
            '1': 'Science',
            '2': 'Art',
            '3': 'Geography',
            '4': 'History',
            '5': 'Entertainment',
            '6': 'Sports'
        }
    }

#### GET /questions

* Returns a list of questions. The number is limited to the pagination size. Additionally it returns a list of categories and total number of questions.
* Sample: `curl http://127.0.0.1:5000/questions` 

JSON return:

    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "current_category": null,
        "questions": [
            {
                "answer": "Tom Cruise",
                "category": "5",
                "difficulty": 4,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            },
            {
                "answer": "Maya Angelou",
                "category": "4",
                "difficulty": 2,
                "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
                "answer": "Edward Scissorhands",
                "category": "5",
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            },
            {
                "answer": "Muhammad Ali",
                "category": "4",
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
            },
            {
                "answer": "Brazil",
                "category": "6",
                "difficulty": 3,
                "id": 10,
                "question": "Which is the only team to play in every soccer World Cup tournament?"
            },
            {
                "answer": "Uruguay",
                "category": "6",
                "difficulty": 4,
                "id": 11,
                "question": "Which country won the first ever soccer World Cup in 1930?"
            },
            {
                "answer": "George Washington Carver",
                "category": "4",
                "difficulty": 2,
                "id": 12,
                "question": "Who invented Peanut Butter?"
            },
            {
                "answer": "Lake Victoria",
                "category": "3",
                "difficulty": 2,
                "id": 13,
                "question": "What is the largest lake in Africa?"
            },
            {
                "answer": "The Palace of Versailles",
                "category": "3",
                "difficulty": 3,
                "id": 14,
                "question": "In which royal palace would you find the Hall of Mirrors?"
            },
            {
                "answer": "Agra",
                "category": "3",
                "difficulty": 2,
                "id": 15,
                "question": "The Taj Mahal is located in which Indian city?"
            }
        ],
        "success": true,
        "total_questions": 18
    }

#### DELETE /questions/\<int:id\>

* Deletes a question and returns the if of it.
* Sample: `curl http://127.0.0.1:5000/questions/4 -X DELETE` 

JSON return:

    {
        'success': true,
        'deleted': 4
    }


#### POST /questions

* Creates a new question with question, answer, category and difficulty level values.
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            "question": "What is the HTTP method to create new objects?",
            "answer": "POST",
            "difficulty': 1,
            "category": "1"
        }'` 

JSON return:

    {
        'success': true,
        'created': 55
    }


#### POST /questions

* Searches for substring in questions using a search term in JSON request parameters. The resulats are paginated if there are more than 10 found questions.
* Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "boxer"}'` 

JSON return:

    {
    "currentCategory": null, 
    "questions": [
        {
        "answer": "Muhammad Ali", 
        "category": "4", 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
        }
    ], 
    "success": true, 
    "totalQuestions": 1
    }


#### GET /categories/\<int:category_id\>/questions

* Get questions by <strong>category id</strong> in url. The result is a JSON witgh paginated questions.
* Sample: `curl http://127.0.0.1:5000/categories/6/questions` 

JSON return:

    {
    "currentCategory": 6, 
    "questions": [
        {
        "answer": "Brazil", 
        "category": "6", 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
        }, 
        {
        "answer": "Uruguay", 
        "category": "6", 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ], 
    "success": true, 
    "totalQuestions": 2
    }


#### POST /quizzes

* Users are allowed to play the game. Category and previous questions are passed to the JSON request as parameters. Returns a JSON object with random questions that are not in previous questions.
* Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category": {"type": "Art", "id": "2"}, "previous_questions": [18,19]}'` 

JSON return:

    {
    "question": {
        "answer": "Mona Lisa", 
        "category": "2", 
        "difficulty": 3, 
        "id": 17, 
        "question": "La Giaconda is better known as what?"
    }, 
    "success": true
    }

## Authors
The creator of the most of the content is <strong>Udacity</strong>.
Ramil Kirner is the author of the API('__init.py__') and this README. 
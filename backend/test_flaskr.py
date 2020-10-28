import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql://postgres:rammel@localhost:5432/test_trivia"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # CATEGORIES ##############################
    # TEST OK
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_error_get_categories(self):
        res = self.client().get('/categories/12312312')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # QUESTIONS  ##############################
    # TEST OK
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_not_valid_questions_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # QUESTION BY CATEGORIES ###################
    # TEST OK
    def test_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_question_by_category(self):
        res = self.client().get('/categories/555555555/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    # DELETE ####################################
    # TEST OK
    def test_delete_question(self):
        test_question = Question('Test question', 'Test answer', 1, '1')
        test_question.insert()

        question_id = test_question.id

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question_query = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question_query, None)

    # TEST OK
    def test_404_delete_not_existing_question(self):
        res = self.client().delete('/questions/100000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # CREATE #######################################################
    # TEST OK
    def test_create_new_question(self):
        question_json = {
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 5,
            'category': '4'
        }

        len_before = len(Question.query.all())
        res = self.client().post('/questions', json=question_json)
        data = json.loads(res.data)
        len_after = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len_before+1, len_after)

    # TEST OK
    def test_422_create_question(self):
        question_json = {
            'question': '',
            'answer': '',
            'difficulty': 5,
            'category': ''
        }
        res = self.client().post('/questions', json=question_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # SEARCH #######################################################
    # TEST OK
    def test_search_questions(self):
        search_json = {'searchTerm': 'a'}
        res = self.client().post('/questions/search', json=search_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['totalQuestions'])

    # TEST OK
    def test_400_search_questions(self):
        # Unlikely possible search term
        search_json = {'searchTerm': 'dkjfaödslfjsadfoajfd'}
        res = self.client().post('/questions/search', json=search_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # QUIZ #######################################################
    # TEST OK
    def test_play_quiz(self):
        quiz_json = {
            'previous_questions': [16,18],
            'quiz_category': {
                'type': 'Art', 'id': '2'
            }
        }

        res = self.client().post('/quizzes', json=quiz_json)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 2)

        self.assertNotEqual(data['question']['id'], 16)
        self.assertNotEqual(data['question']['id'], 18)

    # TEST OK
    def test_400_play_quiz(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

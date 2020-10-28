import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Initializing CORs
    CORS(app, resources={r"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorisation, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PUT, POST, DELETE, OPTIONS')
        return response

    # Retrieve all categories for questions
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()

        category_dict = {}

        for category in categories:
            category_dict[category.id] = category.type

        if len(category_dict) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': category_dict
        })

    # Get all questions including pagination
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate(request, selection)

        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories_dict,
            'current_category': None
        })

    # Delete a question
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        select_question = Question.query.filter(
            Question.id == question_id
        ).one_or_none()

        if select_question is None:
            abort(404)

        else:
            select_question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate(request, selection)

        return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': current_questions,
            'total_questions': len(Question.query.all())
        })

    # Create new question
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        try:
            if not ('question' in body and 'answer' in body):
                abort(400)

            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)

            question = Question(
                new_question,
                new_answer,
                new_category,
                new_difficulty
            )

            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })

        except Exception:
            abort(422)

    # Search questions with a string/substring
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()

        search_term = body.get('searchTerm', None)
        try:
            if search_term:
                search_query = Question.query.filter(
                    (Question.question.ilike('%' + search_term + '%'))
                ).all()

                if (len(search_query) == 0):
                    abort(404)

                return jsonify({
                    'success': True,
                    'questions':
                        [question.format() for question in search_query],
                    'totalQuestions': len(search_query),
                    'currentCategory': None
                })

        except Exception:
            abort(400)

    # GET endpoint to get questions basend on category
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        try:
            questions = Question.query.filter(
                Question.category == str(category_id)
            ).all()

            if len(questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'totalQuestions': len(questions),
                'currentCategory': category_id
            })

        except Exception:
            abort(422)

    # Use the point to start a new quiz game
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():

        try:
            body = request.get_json()

            quiz_category = body.get('quiz_category', None)
            previous_questions = body.get('previous_questions', None)

            if (quiz_category['id'] == 0):
                question_query = Question.query.all()
            else:
                question_query = Question.query.filter(
                Question.category ==
                quiz_category['id']
            ).filter(
                Question.id.notin_((previous_questions))
            ).all()

            new_question = question_query[random.randrange(
                0,
                len(question_query), 1
            )] if len(question_query) > 0 else None

            return jsonify({
                'success': True,
                'question': new_question.format()
                })

        except Exception:
            abort(400)

    # Create errorhandlers for all expected errors
    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(400)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    return app

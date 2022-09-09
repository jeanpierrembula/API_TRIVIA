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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'admin', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_object = {
            'question': 'who is the best player in the world?',
            'answer': 'mputu',
            'difficulty': 5,
            'category': 2
        }

        self.erreur_question = {
            'question': 'What is your name?',
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_trouver_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_recuperer_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_erreur_pour_trouver_une_question(self):

        res = self.client().post('/questions/chercher', json={'terme': 'mbula'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_404_trouver_questions(self):
        res = self.client().get('/questions?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_questions_par_categorie(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone((data['questions']))
        self.assertTrue((data['total_de_questions'] > 0 , True))
        self.assertTrue((data['categorie_courante'] == 2,True))

    def test_404_questions_par_categorie(self):
        res = self.client().get('/categories/c/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_poster_question(self):
        res = self.client().post('/questions', json=self.new_object)
        data = json.loads(res.data)
 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'] > 0,True)

    def test_poster_question(self):
        res = self.client().post('/questions', json=self.erreur_question)
        data = json.loads(res.data)
       
        self.assertEqual(res.status_code, 422)

    def test_quiziew(self):
        new_quiz = {'quiz_category': {'type': 'Entertainment', 'id': 9},'last_questions': []}

        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_404_if_book_does_not_exist(self):
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'non traetable')

    def test_supprimer_question(self):
        NQuestion = Question(question='what is your name', answer='Abdullah Alessa',difficulty=5 , category=6)
        NQuestion.insert()
        res = self.client().delete(f'/questions/{NQuestion.id}')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == NQuestion.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], (NQuestion.id))
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
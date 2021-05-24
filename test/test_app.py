import sys
sys.path.append('..\\')

import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app.app import create_app
from config.config import SetDatabase
from models.models import setup_db, Vessel, Equipment

class AppCompleteTest(unittest.TestCase):
    """This class include tests for all created endpoints"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # Connect to 
        database = SetDatabase('..\\config_test.json')
        database_conn_string = database.connection_string
        setup_db(self.app, database_conn_string)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_post_vessel(self):
        """
        Test success of endpoint vessels with post method.
        """
        vessel_code = 'MV110'
        info = {'code': vessel_code}

        res = self.client().post('/vessels', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertEqual(res.get_json()['code'], vessel_code)

        # Undo the post method
        vessel = Vessel.query.filter_by(code=vessel_code).first()
        vessel.delete()

    def test_post_existent_vessel(self):
        """
        Test failure of endpoint vessels with post method.
        """
        vessel_code = 'MV103'
        info = {'code': vessel_code}

        res = self.client().post('/vessels', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], 'code already exists')

    def test_post_vessel_bad_request(self):
        """
        Test failure of endpoint vessels with post method.
        """
        info = {}

        res = self.client().post('/vessels', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], 'bad request')
    
    def test_post_equipment(self):
        """
        Test success of endpoint equipments with post method.
        """
        info = dict(
            name='compressor',
            code='NewEquip',
            location='Brazil',
            vessel_code='MV102'
        )

        res = self.client().post('/equipments', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertEqual(res.get_json()['vessel_code'], 'MV102')
        self.assertEqual(res.get_json()['name'], 'compressor')
        self.assertEqual(res.get_json()['code'], 'NewEquip')
        self.assertEqual(res.get_json()['location'], 'Brazil')
        self.assertEqual(res.get_json()['activation_status'], True)

        # Undo the post method
        equipment = Equipment.query.filter_by(code='NewEquip').first()
        equipment.delete()

    def test_inactivate_equipments(self):
        """
        Test success of patch equipments endpoint, making activation_status of equipments equals false.
        """
        info = {'equipments':[
            {'code': '5310B9D7'},
            {'code': '5310B9D8'}
        ]}

        res = self.client().patch('/equipments', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertEqual(len(res.get_json()['non_processed_equipments']), 0)

        # Undo patch method
        for item in info['equipments']:
            equipment = Equipment.query.filter_by(code=item['code']).first()
            equipment.activation_status = True  
            equipment.update()

    def test_get_active_equipments(self):
        """
        Test success of get active equipments
        """

        res = self.client().get('/equipments/mv102')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['vessel_code'], 'MV102')
        self.assertEqual(len(res.get_json()['equipments']), 5)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
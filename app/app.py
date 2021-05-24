import sys
sys.path.append('..\\')

from models.models import setup_db, Vessel, Equipment
from config.config import SetDatabase

import os 
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import random


def create_app(test_config=None):
    """
    Create and configure the application.
    """
    app = Flask(__name__)

    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS, PATCH')
        return response

    # Route implemented to get all vessels
    @app.route('/vessels', methods=['GET'])
    def get_vessels():
        """
        Get all existing vessels from the database.
        """
        
        all_vessels = Vessel.query.all()
        all_vessels_format = [vessel.format() for vessel in all_vessels]
        
        return jsonify({'vessels': all_vessels_format, 
        'total_vessels': len(all_vessels),
        'success': True
        })

    @app.route('/vessels', methods=['POST'])
    def add_vessel():
        """
        Add a new vessel.
        """
        body = request.get_json()
        vessel_code = body.get("code")

        if vessel_code is None:

            abort(400)

        vessel = Vessel(code=vessel_code)
        
        # persist data into database
        try:
            vessel.insert()
        except:
            abort(403)

        return jsonify({
            'id': vessel.id,
            'code': vessel.code,
            'success': True,
        })

    @app.route('/equipments', methods=['POST'])
    def add_equipement():
        """
        Add a new equipement, associated with a vessel.
        """
        body = request.get_json()

        equipment = Equipment(
            name=body.get('name'),
            code=body.get('code'),
            location=body.get('location'),
            vessel_code=body.get('vessel_code')
        )

        try:
            equipment.insert()

        except:
            abort(403)

        return jsonify({
            'success': True,
            'id': equipment.id, 
            'code': equipment.code, 
            'name': equipment.name, 
            'location': equipment.location,
            'activation_status': equipment.activation_status, 
            'vessel_code': equipment.vessel_code
        })

    @app.route('/equipments', methods=['PATCH'])
    def inactivate_equipments():
        """
        Receive a list containing one or more equipments to deactivate. This endpoint return a list of non processed equipments considering
        that errors can occurs during the process.
        """
        body = request.get_json()
        equipments_info = body.get('equipments')
        non_processed_equipments = list()

        try:
            for equipment_info in equipments_info:

                equipment_code = equipment_info.get('code') 
                equipment = Equipment.query.filter_by(code=equipment_code).first()

                if equipment is not None:

                    equipment.activation_status = False 
                    equipment.update()

                else:  

                    non_processed_equipments.append({'code': equipment_code})

        except:
            
            # In case of problems with JSON passed.
            abort(400)

        
        return jsonify({
            'success': True,
            'non_processed_equipments': non_processed_equipments,
        })

    @app.route('/equipments/<vessel_code>', methods=['GET'])
    def get_equipments_by_vessel(vessel_code):
        """
        Get all active equipments from a vessel.
        """
        vessel_code = vessel_code.upper()
        vessel = Vessel.query.filter_by(code=vessel_code).first()

        if vessel is None:

            abort(404)

        equipments = vessel.equipments 

        equipments_info = [equipment.format() for equipment in equipments]
        active_equipements = [equipment for equipment in equipments_info if equipment['activation_status'] == True]

        return jsonify({
            'vessel_code': vessel_code,
            'success': True,
            'equipments': active_equipements
        })


    @app.errorhandler(403)
    def internal_server_error(error):

        return jsonify({'success':False,
                        'error': 403,
                        'message': 'code already exists'}), 403

    @app.errorhandler(400)
    def internal_server_error(error):

        return jsonify({'success':False,
                        'error': 400,
                        'message': 'bad request'}), 400

    @app.errorhandler(404)
    def internal_server_error(error):

        return jsonify({'success':False,
                        'error': 404,
                        'message': 'not found'}), 404

    return app
from flask import request, jsonify
from sqlalchemy.sql import text
from flask_cors import cross_origin
from app import app, db_pgl
from app.utils.response import bad_request, bad_request_schema, non_autorhize
from app.controllers.valid_response import ValidatorController


VALIDATION = ValidatorController()
class Application:
    @app.errorhandler(400)
    def error_400(error):
        try:
            return bad_request_schema(error)
        except Exception as e:
            print(e)

    @app.route("/")
    @app.route("/index")
    def index():
        return "Example Backend"

    @app.route("/api/validate_responses/<survey>", methods=["GET"])
    def validate(survey):
        if not survey:
            return jsonify({"error": "Survey UUID must be provided"}), 400
        validation_results = VALIDATION.validate_survey_responses(survey)
        return jsonify(validation_results)

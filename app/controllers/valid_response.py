import sys
from app import db_pgl as db
from app.models.survey_model import Survey
from app.models.question_model import Question
from app.models.response_model import Response
from app.models.user_model import User
from datetime import datetime
from app.utils.validator import validate_responses


class ValidatorController:
    def validate_survey_responses(self, survey_uuid):
        survey = db.session.query(Survey).filter_by(id=survey_uuid).first()
        if not survey:
            return {"error": "Survey not found"}, 404

        responses = db.session.query(Response).filter_by(id_survey=survey_uuid).all()
        if not responses:
            return {"error": "No responses found for this survey"}, 404

        # Diccionario para mapear preguntas con sus respuestas
        question_responses = {}
        for response in responses:
            question = (
                db.session.query(Question).filter_by(id=response.id_question).first()
            )
            if question.question not in question_responses:
                question_responses[question.question] = []
            question_responses[question.question].append(
                (response.id, response.response)
            )

        validation_results = []
        for question, response_list in question_responses.items():
            question_results = validate_responses([question], response_list)
            validation_results.extend(question_results)

        # Actualizar las respuestas no válidas
        for result in validation_results:
            if not result["valid"]:
                question = (
                    db.session.query(Question)
                    .filter_by(question=result["question"], id_survey=survey_uuid)
                    .first()
                )
                if question:
                    self.update_invalid_response(question.id, result["response_id"])

        return validation_results

    def validate_response(self, question_text, response_text):
        from utils.response import is_coherent

        return is_coherent(question_text, response_text)

    def update_invalid_response(self, question_id, response_id):
        response = (
            db.session.query(Response)
            .filter_by(id_question=question_id, id=response_id)
            .first()
        )
        if response:
            response.valid = False
            db.session.commit()
            return {"message": "Response updated successfully"}
        else:
            return {"error": "Response not found"}, 404

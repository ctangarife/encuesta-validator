import spacy

# Cargar el modelo de SpaCy
nlp = spacy.load("en_core_web_sm")


def is_coherent(question, answer):
    doc_question = nlp(question)
    doc_answer = nlp(answer)
    similarity = doc_question.similarity(doc_answer)
    return similarity > 0.6


def validate_responses(questions, responses):
    invalid_responses = []
    if not isinstance(responses, list):
        raise ValueError("Responses should be a list")

    for question in questions:
        for response_id, response_text in responses:
            if not isinstance(response_text, str):
                raise ValueError("Each response should be a string")
            is_valid = is_coherent(question, response_text)
            invalid_responses.append(
                {
                    "question": question,
                    "response": response_text,
                    "response_id": response_id,
                    "valid": is_valid,
                }
            )
    return invalid_responses

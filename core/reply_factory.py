
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id is not None:
        session[f"answer_{current_question_id}"] = answer
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        next_question_id = 0
    elif current_question_id + 1 < len(PYTHON_QUESTION_LIST):
        next_question_id = current_question_id + 1
    else:
        return None, None

    next_question = PYTHON_QUESTION_LIST[next_question_id]['question_text']

    return next_question, next_question_id


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = 0
    for question_id, question_details in enumerate(PYTHON_QUESTION_LIST):
        correct_answer = question_details['answer']
        user_answer = session.get(f"answer_{question_id}")
        if user_answer == correct_answer:
            score += 1

    total = len(PYTHON_QUESTION_LIST)
    response = f"Done! Your Score: {score}/{total}"
    return response

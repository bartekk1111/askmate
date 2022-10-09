from datetime import datetime

def to_datetime(questions):
    for question in questions:
        question['date_created'] = datetime.fromtimestamp(question['date_created'])
    return questions
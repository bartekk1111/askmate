import csv
import os

QUESTION_FILE_PATH = os.getenv('QUESTION_FILE_PATH') if 'QUESTION_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWER_FILE_PATH = os.getenv('ANSWER_FILE_PATH') if 'ANSWER_FILE_PATH' in os.environ else 'sample_data/answer.csv'
SEPARATOR = ";"
QUESTION_HEADER = ["id","submission_time","view_number","vote_number","title","message","image"]
def get_all_questions():
    questions = []
    with open(QUESTION_FILE_PATH, encoding="utf-8") as file:
        dict_reader = csv.DictReader(file)
        for line in dict_reader:
            question = dict(line)
            questions.append(question)
    return questions

def get_answers():
    answers = []
    with open(ANSWER_FILE_PATH, encoding="utf-8") as file:
        dict_reader = csv.DictReader(file)
        for line in dict_reader:
            answer = dict(line)
            answers.append(answer)
    return answers

def read_questions():
    questions = []
    with open(QUESTION_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            question = dict(line)
            questions.append(question)
    return questions

def save_question(question):
    with open(QUESTION_FILE_PATH, "a") as file:
        file.write(f"{question['id']};{question['text']}\n")

def read_write():
    questions = []
    with open(QUESTION_FILE_PATH, encoding="utf-8") as file:
        dict_reader = csv.DictReader(file)
        print(dict_reader)
        for line in dict_reader:
            print(line)
            question = dict(line)
            questions.append(question)
        question = {"id": "3","submission_time": "1493068124","view_number": "20","vote_number": "8",
                    "title": "jakiś tytuł","message": "jakaś wiadomość"}
        questions.append(question)
        print(questions)
    return questions

def write_question(question):
    questions = read_questions()
    with open(QUESTION_FILE_PATH, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=QUESTION_HEADER)
        writer.writeheader()
        for item in questions:
            writer.writerow(item)
        writer.writerow(question)
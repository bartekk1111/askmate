import connection_to_database


@connection_to_database.connection_handler
def delete_row(cursor, row_id):
    query = f"""
                DELETE FROM questions
                WHERE id = {row_id};
                """
    cursor.execute(query)


@connection_to_database.connection_handler
def alter_row(cursor, row_id, column_to_alter, new_value):
    query = f"""
            UPDATE questions
            SET {column_to_alter} = '{new_value}'
            WHERE id = {row_id};
            """
    cursor.execute(query)


@connection_to_database.connection_handler
def get_all_questions(cursor):
    query = """
            SELECT *
            FROM questions
            ORDER BY date_created DESC"""
    cursor.execute(query)
    return cursor.fetchall()


@connection_to_database.connection_handler
def get_top_questions(cursor, limit):
    query = """
            SELECT *
            FROM questions
            ORDER BY date_created DESC
            LIMIT %s"""
    cursor.execute(query, limit)
    return cursor.fetchall()


def get_answers():
    pass


@connection_to_database.connection_handler
def read_question(cursor, question_id):
    query = """
        SELECT * FROM questions WHERE id = (%(id)s)
        """
    cursor.execute(query, {"id": question_id})
    return cursor.fetchall()


@connection_to_database.connection_handler
def get_user(cursor, email):
    query = """
        SELECT * FROM users WHERE user_email = (%(email)s)
        """
    cursor.execute(query, {"email": email})
    return cursor.fetchall()


@connection_to_database.connection_handler
def save_question(cursor, question):
    query = """
        INSERT INTO
        questions (title, content, date_created)
        values ( %(title)s, %(content)s, %(date_created)s )"""
    cursor.execute(query, {"title": question['title'],
                           "content": question['content'],
                           "date_created": question['date_created']})


@connection_to_database.connection_handler
def save_answer(cursor, answer):
    query = """
        INSERT INTO
        answers (content)
        values (%(content)s)"""
    cursor.execute(query, {"content": answer['content']})

@connection_to_database.connection_handler
def add_user(cursor, user):
    query = """
        INSERT INTO
        public.users (user_name, user_email, user_password)
        values ( %(name)s, %(email)s, %(password)s )"""
    cursor.execute(query, {"email": user['user_email'],
                           "password": user['user_password'],
                           "name": user['user_name']})

def read_write():
    pass

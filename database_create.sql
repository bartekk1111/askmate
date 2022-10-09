CREATE TABLE questions (
	id SERIAL PRIMARY KEY,
	title VARCHAR(200) NOT NULL,
	content VARCHAR(1000) NOT NULL,
	user_id INTEGER,
	date_created INTEGER,
	view_number INTEGER,
	vote_number INTEGER,
	image_path VARCHAR(200)
);

CREATE TABLE answers (
	id SERIAL PRIMARY KEY,
	answer VARCHAR(1000) NOT NULL,
	user_id INTEGER,
	date_created INTEGER,
	question_id INTEGER NOT NULL,
	image_path VARCHAR(200)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(200),
    user_email VARCHAR(200),
    user_password VARCHAR(200)
);

CREATE TABLE comments_que (
    id SERIAL PRIMARY KEY,
    comment VARCHAR(1000) NOT NULL,
    user_id INTEGER,
    question_id INTEGER,
    date_created INTEGER

);

CREATE TABLE comments_ans (
    id SERIAL PRIMARY KEY,
    comment VARCHAR(1000) NOT NULL,
    user_id INTEGER,
    question_id INTEGER,
    date_created INTEGER
);

-- EXAMPLES

INSERT INTO questions (title, content) VALUES
    ('How to automatically compile less files in an asp.net core project', 'I have an asp.net core project. This project contains less style sheet files. I can see a compilerconfig.json and compilerconfig.json.defaults files at the root of the project. This 2 files contains ...');
INSERT INTO questions (title, content) VALUES
	('How to implement factory pattern with dagger using annotation', 'What I have done currently is Created an abstract class public interface AbstractRawPathStrategy { String getRouteKey(); void processRequest(); } Implemented the classes public class ...');
INSERT INTO questions (title, content) VALUES
	('Nginx reverse proxy to Apache2 - not working - too many redirects', 'at the beginning I want to apologize, but I am newbie with Nginx. I have a VPS where I have some PHP/Symfony projects (hosted in Apache2). Now I need to add a new application (in Vue especially');
INSERT INTO questions (title, content) VALUES
	('Exporting Evernote notes with Siri Shortcuts', 'I'm writing a Siri Shortcut to export notes from Evernote to another app. But I'm having a devil of a time figuring out how to do it. When I invoke the shortcut from the iOS share sheet, it sends a ...');
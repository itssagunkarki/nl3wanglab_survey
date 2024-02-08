from flask import Flask, render_template, request
import question_file
import json

app = Flask(__name__)



@app.route('/')
def home():
    file = question_file.QuestionFile('/Users/sagunkarki/Desktop/nl3wanglab_survey/static/Template.xlsx')
    questions = file.get_questions_as_dict().get_questions()
    return render_template('questions.html', questions=questions)



if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = "responses" #as people answer questions their answers should be stored here.

@app.route('/')
def home_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home_page.html', title = title, instructions = instructions)

@app.route('/start', methods = ["POST"])
def make_session():
    session[responses] = []

    return redirect ('/questions/0')

@app.route('/questions/<int:q_id>')
def get_questions(q_id):

    the_responses = session.get(responses) 

    if the_responses is None:
        return redirect ('/')

    if len(the_responses) != q_id:
        flash(f'You are accessing an Invalid Question')
        return redirect (f'/questions/{len(the_responses)}')
    
    if len(the_responses) == len(satisfaction_survey.questions):
        return redirect("/complete")

    question = satisfaction_survey.questions[q_id]

    return render_template('question.html', question = question, q_id = q_id)

@app.route('/questions/answer', methods =["POST"])
def post_answer():
    chosen_answer = request.form['answer']
    the_responses = session[responses] 
    the_responses.append(chosen_answer)
    session[responses] = the_responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/complete')

    else:
        return redirect (f'/questions/{len(responses)}')

@app.route('/complete')
def completion():
    title = satisfaction_survey.title
    return render_template('complete.html',title = title)
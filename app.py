import json
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load quiz data from JSON files
def load_json(file_name):
    file_path = os.path.join(os.getcwd(), 'data', file_name)
    with open(file_path, 'r') as f:
        return json.load(f)

# Route for the homepage
@app.route('/')
def index():
    session.clear()  # Clear session at the start of a new quiz
    return render_template('index.html')

# Map personality types to corresponding images
result_to_image = {
    "You're just a chill guy.": "chillguy.jpg",
    "Disappointed, but not surprised.": "failed.jpg",
    "Aray bhai, paper was out of syllabus!": "main_character.jpg"
}

# Meme Quiz Route
@app.route('/meme_quiz', methods=['GET', 'POST'])
def meme_quiz():
    quiz_data = load_json('meme.json')

    # Initialize session variables
    if 'current_question' not in session:
        session['current_question'] = 0
        session['answers'] = []

    # Check if quiz is completed
    if session['current_question'] >= len(quiz_data):
        return redirect(url_for('meme_result'))

    # Handle POST request
    if request.method == 'POST':
        answer = request.form.get('answer')  # Get selected answer
        if answer:
            session['answers'].append(answer)
            session['current_question'] += 1
        return redirect(url_for('meme_quiz'))

    # Get current question
    current_question = quiz_data[session['current_question']]
    return render_template('quiz.html', current_question=current_question, quiz_type='Meme')

@app.route('/meme_result')
def meme_result():
    user_answers = session.get('answers', [])
    quiz_data = load_json('meme.json')

    # Map personality types to their corresponding images
    result_to_image = {
        "You're just a chill guy.": "chillguy.jpg",
        "Disappointed, but not surprised.": "failed.jpg",
        "Aray bhai, paper was out of syllabus!": "main_character.jpg"
    }

    # Determine personality type based on user answers
    result_count = {}
    for answer in user_answers:
        for question in quiz_data:
            for option_text, result in question['options'].items():
                if answer == option_text:
                    result_count[result] = result_count.get(result, 0) + 1

    # Debug: Print result_count to see how answers are being counted
    print(f"Result Count: {result_count}")

    # Get the personality type with the highest count
    personality_type = max(result_count, key=result_count.get, default="Could not guess your personality")
    
    # Debug: Print personality_type to confirm it’s being set correctly
    print(f"Personality Type: {personality_type}")

    image = result_to_image.get(personality_type, "default.png")  # Map personality type to image

    session.clear()  # Clear session after results
    return render_template('meme_result.html', personality_type=personality_type, image=image)


# General Quiz Route
@app.route('/general_quiz', methods=['GET', 'POST'])
def general_quiz():
    quiz_data = load_json('general.json')

    if 'current_question' not in session:
        session['current_question'] = 0
        session['score'] = 0

    if session['current_question'] >= len(quiz_data):
        return redirect(url_for('general_result'))

    if request.method == 'POST':
        answer = request.form.get('answer')
        correct_answer = quiz_data[session['current_question']]['correct']
        if answer and answer == correct_answer:
            session['score'] += 1
        session['current_question'] += 1
        return redirect(url_for('general_quiz'))

    current_question = quiz_data[session['current_question']]
    return render_template('quiz.html', current_question=current_question, quiz_type='General')

@app.route('/general_result')
def general_result():
    score = session.get('score', 0)
    total_questions = len(load_json('general.json'))
    session.clear()  # Clear session after results
    return render_template('general_result.html', score=score, total_questions=total_questions)

# Apocalypse Quiz Route
@app.route('/apocalypse_quiz', methods=['GET', 'POST'])
def apocalypse_quiz():
    quiz_data = load_json('apocalypse.json')

    if 'current_question' not in session:
        session['current_question'] = 0
        session['scare_factor'] = 0

    if session['current_question'] >= len(quiz_data):
        return redirect(url_for('apocalypse_result'))

    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer in quiz_data[session['current_question']]['scare_points']:
            scare_points = int(quiz_data[session['current_question']]['scare_points'][answer])
            session['scare_factor'] += scare_points
        session['current_question'] += 1
        return redirect(url_for('apocalypse_quiz'))

    current_question = quiz_data[session['current_question']]
    return render_template('quiz.html', current_question=current_question, quiz_type='Apocalypse')

@app.route('/apocalypse_result')
def apocalypse_result():
    scare_factor = session.get('scare_factor', 0)
    session.clear()  # Clear session after results

    # Define scare messages and survival tips based on score ranges
    if scare_factor < 20:
        scare_message = "You kept your cool and stayed safe!"
        survival_tips = [
            "Continue to avoid unnecessary risks.",
            "Stay vigilant and plan your moves carefully.",
            "Keep your resources stocked and prioritize safety."
        ]
    elif 20 <= scare_factor < 50:
        scare_message = "You had a few close calls but managed to pull through."
        survival_tips = [
            "Consider balancing bravery with caution.",
            "Stay prepared for unexpected situations.",
            "Work on your decision-making under pressure."
        ]
    else:
        scare_message = "Your actions were daring, but you took significant risks!"
        survival_tips = [
            "Reassess your strategy to avoid unnecessary dangers.",
            "Learn to prioritize survival over boldness.",
            "Build alliances to improve your chances in high-risk scenarios."
        ]

    return render_template(
        'apocalypse_result.html',
        scare_factor=scare_factor,
        scare_message=scare_message,
        survival_tips=survival_tips
    )


if __name__ == '__main__':
    app.run(debug=True)

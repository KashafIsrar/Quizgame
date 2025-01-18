from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)

# Load questions based on category
def load_questions(category):
    filepath = os.path.join("questions", f"{category}.json")
    with open(filepath, "r") as file:
        return json.load(file)

# Homepage
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Start Meme Quiz (Personality Quiz)
@app.route("/start-meme-quiz", methods=["POST"])
def start_meme_quiz():
    category = "meme"  # Fixed category for meme quiz
    questions = load_questions(category)
    return render_template("quiz.html", questions=questions, category=category, is_personality=True)

# Start General or Fun Trivia Quiz (MCQs)
@app.route("/start-quiz", methods=["POST"])
def start_quiz():
    category = request.form.get("category")
    if not category:
        return redirect(url_for("home"))
    questions = load_questions(category)
    is_personality = category == "meme"  # Check if the quiz is a personality quiz
    return render_template("quiz.html", questions=questions, category=category, is_personality=is_personality)

# Submit Quiz and Show Results for Meme Quiz (Personality Quiz)
@app.route("/submit-meme-quiz", methods=["POST"])
def submit_meme_quiz():
    answers = request.json.get("answers", {})
    scores = {
        "Your'e just a chill guy.": 0,
        "Expectes an easy day, failed.": 0,
        "Main character energy? Always ON.": 0,
    }
    for answer in answers.values():
        scores[answer] += 1

    # Determine personality trait
    personality = max(scores, key=scores.get)
    image_map = {
        "Your'e just a chill guy.": "chillguymeme.jpg",
        "Expectes an easy day, failed.": "cilliandissapointedmeme.jpg",
        "Main character energy? Always ON.": "chilkaroakshaymeme.jpg",
    }
    return render_template(
        "result.html", personality=personality, image=image_map[personality]
    )

# Submit Quiz and Show Results for MCQs Quiz (General / Fun Trivia)
@app.route("/submit-quiz", methods=["POST"])
def submit_mcq_quiz():
    answers = request.json.get("answers", {})
    score = 0
    for answer in answers.values():
        if "Correct" in answer:  # Check if the answer contains "Correct"
            score += 1
    
    # Score message based on performance
    if score == len(answers):
        message = "Perfect! You are a trivia master."
    elif score > len(answers) // 2:
        message = "Great job! You're knowledgeable."
    else:
        message = "Better luck next time! Keep learning."

    return render_template("scoreboard.html", score=score, total=len(answers), message=message)

if __name__ == "__main__":
    app.run(debug=True)

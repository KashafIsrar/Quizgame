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

# Start Quiz
@app.route("/start-quiz", methods=["POST"])
def start_quiz():
    category = request.form.get("category")
    if not category:
        return redirect(url_for("home"))
    questions = load_questions(category)
    return render_template("quiz.html", questions=questions, category=category)

# Submit Quiz and Show Results
@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
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
        "Your'e just a chill guy.": "chill.jpg",
        "Expectes an easy day, failed.": "failed.jpg",
        "Main character energy? Always ON.": "main_character.jpg",
    }
    return render_template(
        "result.html", personality=personality, image=image_map[personality]
    )

if __name__ == "__main__":
    app.run(debug=True)

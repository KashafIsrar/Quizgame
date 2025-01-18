from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Hardcoded questions and answers
questions = [
    {
        "id": 1,
        "scenario": "You find a mysterious bunker, but the door has a combination lock. What is the sum of 15 + 27?",
        "options": ["30", "42", "50", "57"],
        "answer": "42"
    },
    {
        "id": 2,
        "scenario": "You encounter a stranger who offers to trade supplies. What is the chemical symbol for water?",
        "options": ["H2O", "O2", "CO2", "H2"],
        "answer": "H2O"
    },
    {
        "id": 3,
        "scenario": "You're trapped in a room filling with gas. Solve this riddle to escape: What has keys but can't open locks?",
        "options": ["Piano", "Locksmith", "Keyboard", "Map"],
        "answer": "Piano"
    }
]

# Track the player's score
player_score = 0

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/game/<int:question_id>', methods=['GET', 'POST'])
def game(question_id):
    global player_score

    # Find the question by ID
    question = next((q for q in questions if q["id"] == question_id), None)

    if not question:
        return redirect(url_for('ending'))

    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        print(f"Selected Answer: {selected_answer}")
        if selected_answer == question["answer"]:
            player_score += 10  # Award points for correct answers
        return redirect(url_for('game', question_id=question_id + 1))

    return render_template('game.html', question=question)

@app.route('/ending')
def ending():
    global player_score
    # Determine the ending based on the score
    if player_score >= 20:
        ending_message = "Congratulations! You survived the apocalypse and found a safe zone."
    elif player_score >= 10:
        ending_message = "You managed to survive but lost many supplies. It's a tough road ahead."
    else:
        ending_message = "You succumbed to the dangers of the apocalypse. Better luck next time!"

    final_score = player_score
    player_score = 0  # Reset the score for the next playthrough
    return render_template('ending.html', ending_message=ending_message, final_score=final_score)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')  # Placeholder for leaderboard logic

if __name__ == '__main__':
    app.run(debug=True)

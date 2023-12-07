from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)

# Load your dataset
full_df = pd.read_csv('christmas_movies.csv')
reduced_df = full_df.dropna()

def pick_movies(df):
    return df.sample(2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_mode', methods=['GET', 'POST'])
def select_mode():
    if request.method == 'POST':
        game_mode = request.form['game_mode']
        return redirect(url_for('play', mode=game_mode))
    return render_template('select_mode.html')


@app.route('/play', methods=['GET', 'POST'])
def play():
    game_mode = request.args.get('mode', 'full')
    df = reduced_df if game_mode == 'reduced' else full_df

    if request.method == 'POST':
        user_guess = request.form['guess']
        movie1_title = request.form['movie1']
        movie2_title = request.form['movie2']
        movie1 = df[df['title'] == movie1_title].iloc[0]
        movie2 = df[df['title'] == movie2_title].iloc[0]

        correct = ((movie2['imdb_rating'] >= movie1['imdb_rating'] and user_guess == 'movie2_higher') or
                   (movie2['imdb_rating'] <= movie1['imdb_rating'] and user_guess == 'movie1_higher'))
        
        return render_template('result.html', movie1=movie1, movie2=movie2, correct=correct)

    movies = pick_movies(df)
    return render_template('play.html', movie1=movies.iloc[0].to_dict(), movie2=movies.iloc[1].to_dict())


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Heroku's PORT environment variable
    app.run(host='0.0.0.0', port=port)
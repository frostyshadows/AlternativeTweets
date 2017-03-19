import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g
import random
import json

app = Flask(__name__)

filtered_tweets = []

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'AlternativeTweetsLeaderboard.db')
    ))

@app.cli.command('init')
def init():
    init_db()
    init_tweets()
    print "Initialized the server"

def init_tweets():
    for i in range(2009, 2018):
        with open("resources/condensed_%d.json" % i) as raw_tweets_json:
            raw_tweets = json.load(raw_tweets_json)
            for tweet in raw_tweets:
                if not tweet["is_retweet"]:
                    filtered_tweets.append(tweet)

    print "Testing init'ing tweets"
    print random_real_tweet()

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as schema:
        db.cursor().executescript(schema.read())
    db.commit()

#create command line command to init db
@app.cli.command('initdb')
def initdb_command():
    init_db()
    print "Initialized the database"

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/leaderboard', methods=['GET', 'POST'])
def update_leaderboard():
    if not hasattr(g, 'sqlite_db'):
        abort(500)
    if request.method == 'POST':
        return "Invalid post request"
    if request.method == 'GET':
        return render_template('leaderboard.html', entries=query_db("select * from scores order by score desc"))

@app.route('/question', methods=['GET'])
def get_tweet():
    if random.randint(0, 1) == 1:
        return random_real_tweet()
    else:
        return #TODO: return a fake tweet

def random_real_tweet():
    random_tweet_index = random.randint(0, len(filtered_tweets) - 1)
    return filtered_tweets[random_tweet_index]["text"]
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g
import random
import json
import urllib2

app = Flask(__name__)

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
        return g.sqlite_db()

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/leaderboard', methods=['GET', 'POST'])
def update_leaderboard():
    if not hasattr(g, 'sqlite_db'):
        abort(500)
    if request.method == 'POST':
    if request.method == 'GET':
        return 'You got the leaderboard yay!'

def random_real_tweet():
    random_year = random.randint(2009,2017)

    # open the json file from that year
    tweets_json = urllib2.urlopen("./resources/condensed_(%d).json" % random_year)
    tweets = json.loads(tweets_json)

    random_tweet_index = random.randint(0, len(tweets))

    while tweets[random_tweet_index]["is_retweet"] == true:
        random_tweet_index = (random_tweet_index + 1) % (len(tweets) - 1)

    return tweets[random_tweet_index]["Text"]
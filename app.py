from starlette.applications import Starlette
from starlette.schemas import SchemaGenerator
from starlette.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, BigInteger, Integer
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
import requests
import settings
import uvicorn

schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Tweeter Test App", "version": "1.0"}}
)
app = Starlette()

app.debug = settings.DEBUG

base = declarative_base()
db_string = settings.DATABASE_URL
db = create_engine(db_string)


class ResultsTwitter(base):

    __tablename__ = 'results_tweet'

    id = Column(Integer, primary_key=True)
    tweet_id = Column('tweet_id', BigInteger)
    hashtag = Column('hashtag', String)
    tweet = Column('tweet', String)
    username = Column('user', String)
    created_at = Column(String)

    def __init__(self, tweet_id, hashtag, tweet, username, created_at):
        self.tweet_id = tweet_id
        self.hashtag = hashtag
        self.tweet = tweet
        self.username = username
        self.created_at = created_at


def connect():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        base.metadata.create_all(db)
        return session
    except sqlalchemy.exc.DatabaseError as e:
        print(e)

@app.route('/tweets', methods=['GET'])
async def get_last_tweet(request):
    errors = []
    try:
        phrase = settings.PHRASE
        twitter_token = settings.TWITTER_TOKEN
        number = settings.LAST_TWEETS
        search_request: requests.Response = requests.get(
            url='https://api.twitter.com/1.1/search/tweets.json',
            params={'q': phrase, 'lang': 'en', 'count': number, 'src': 'typd'},
            headers={'Authorization': f"Bearer {twitter_token}"}
        )
    except requests.exceptions.RequestException:
        errors.append("Unable to get URL. Please make sure it's valid and try again"
                      )
        return {'error': errors}

    search_list, id_list, pubtime_list, user_list, hashtag_list = [], [], [], [], []

    statuses = search_request.json().get('statuses')

    for status in statuses:
        if 'text' in status:
            tweet = status.get('text')
            id_message = status.get('id')
            published_at = status.get('created_at')
            user = status['user']['name']
            tags = ", ".join([status['text'] for status in status['entities']['hashtags']])
            entry = ResultsTwitter(id_message, tags, tweet, user, published_at)
            ses = connect()
            ses.add(entry)
            ses.commit()
            ses.close()
            search_list.append(tweet)
            id_list.append(id_message)
            pubtime_list.append(published_at)
            user_list.append(user)
            hashtag_list.append(tags)
    response = {'id': id_list,
                'phrase': search_list,
                'published_at': pubtime_list,
                'author': user_list,
                'hashtags': hashtag_list}
    # return JSONResponse(statuses)
    return JSONResponse(response)


@app.route('/uniq', methods=['GET'])
async def get_uniq_tweet():
    pass


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

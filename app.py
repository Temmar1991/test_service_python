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
import models
import uvicorn

schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Tweeter Test App", "version": "1.0"}}
)
app = Starlette()

app.debug = settings.DEBUG

base = declarative_base()


class ResultsTwitter(base):

    __tablename__ = 'results_tweet'

    id = Column(Integer, primary_key=True)
    tweet_id = Column('tweet_id', BigInteger)
    tweet = Column('tweet', String)
    username = Column('user', String)
    created_at = Column(String)

    def __init__(self, tweet_id, tweet, username, created_at):
        self.tweet_id = tweet_id
        self.tweet = tweet
        self.username = username
        self.created_at = created_at


def connect(tweet_id, tweet, username, createdat):
    db_string = settings.DATABASE_URL
    db = create_engine(db_string)
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        base.metadata.create_all(db)
        entry = ResultsTwitter(tweet_id, tweet, username, createdat)
        session.add(entry)
        session.commit()
        session.close()
    except sqlalchemy.exc.DatabaseError as e:
        print(e)
    return


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

    search_list, id_list, pubtime_list, user_list = [], [], [], []

    statuses = search_request.json().get('statuses')

    for status in statuses:
        if 'text' in status:
            text_field = status.get('text')
            id_message = status.get('id')
            published_at = status.get('created_at')
            user = status.get('user').get('id')
            connect(id_message, text_field, user, published_at)
            search_list.append(text_field)
            id_list.append(id_message)
            pubtime_list.append(published_at)
            user_list.append(user)
    response = {'id': id_list,
                'phrase': search_list,
                'published_at': pubtime_list,
                'author_id': user_list}
    # return JSONResponse(statuses)
    return JSONResponse(response)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

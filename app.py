from starlette.applications import Starlette
from starlette.schemas import SchemaGenerator
from starlette.responses import JSONResponse
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


@app.route('/tweets', methods=['GET'])
async def get_last_tweet(request):
    phrase = settings.PHRASE
    twitter_token = settings.TWITTER_TOKEN
    number = settings.LAST_TWEETS
    search_list, id_list, pubtime_list, user_list = [], [], [], []
    search_request: requests.Response = requests.get(
        url='https://api.twitter.com/1.1/search/tweets.json',
        params={'q': phrase, 'lang': 'en', 'count': number, 'src': 'typd'},
        headers={'Authorization': f"Bearer {twitter_token}"}
    )
    if search_request.status_code == 200:
        statuses = search_request.json().get('statuses')
        for status in statuses:
            text_field = status.get('text')
            id_message = status.get('id')
            published_at = status.get('created_at')
            user = status.get('user').get('id')
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

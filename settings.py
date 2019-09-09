from starlette.config import Config
from starlette.datastructures import URL

config = Config('.env')

DEBUG = config('DEBUG', cast=bool, default=False)
LAST_TWEETS = config('LAST_TWEETS', cast=int)
DELAY = config('LAST_TWEETS', cast=int)
PHRASE = config('PHRASE', cast=str)
DATABASE_URL = config('DATABASE_URL', cast=URL)
TWITTER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAMIu9gAAAAAAHAcWjBhL4pvzVlvC92g%2BWxECBIc%3DbumOvxGOtvH9kOaozn8iiLZZ3w91sEcQLe1jsMQbwDuwYtOXpb'




from sqlalchemy import create_engine
from sqlalchemy import Column, String, BigInteger, Integer
from sqlalchemy.ext.declarative import declarative_base
import settings

# database_url = settings.DATABASE_URL
#
# metadata = sqlalchemy.MetaData()
#
# twitter_app = sqlalchemy.Table(
#     "twitter_app",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("message_id", sqlalchemy.Integer),
#     sqlalchemy.Column("created_at", sqlalchemy.Date),
#     sqlalchemy.Column("user_id", sqlalchemy.Integer),
#     sqlalchemy.Column("text", sqlalchemy.Text)
# )
#
# database = databases.Database(database_url)


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


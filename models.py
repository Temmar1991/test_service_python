import databases
import sqlalchemy
import settings

database_url = settings.DATABASE_URL

metadata = sqlalchemy.MetaData()

twitter_app = sqlalchemy.Table(
    "twitter_app",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("message_id", sqlalchemy.Integer),
    sqlalchemy.Column("created_at", sqlalchemy.Date),
    sqlalchemy.Column("user_id", sqlalchemy.Integer),
    sqlalchemy.Column("text", sqlalchemy.Text)
)

database = databases.Database(database_url)

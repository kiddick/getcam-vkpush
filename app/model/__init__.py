import databases
import orm
import sqlalchemy

from app import conf

database = databases.Database(conf.db_uri)
metadata = sqlalchemy.MetaData()


class Channel(orm.Model):
    __tablename__ = "channels"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    cam = orm.String(max_length=100)
    group_id = orm.Integer()


# Create the database
engine = sqlalchemy.create_engine(str(database.url))
# metadata.create_all(engine)

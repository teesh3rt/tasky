from peewee import *

db = SqliteDatabase("tasky.db")

class Task(Model):
    task = CharField()
    done = BooleanField(default=False)
    user = IntegerField()

    class Meta:
        database = db

db.connect()
db.create_tables([Task])

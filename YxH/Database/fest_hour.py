from . import db
import random
import datetime

db = db.fest_hour

def today():
    return str(datetime.datetime.now()).split()[0]

async def set_fest_hour() -> int:
    random_hour = random.randint(0, 23)
    await db.insert_one({'date': today(), 'fest_hour': random_hour})
    return random_hour

async def get_fest_hour() -> int:
    x = await db.find_one({'date': today()})
    if x:
        return x['fest_hour']
    return await set_fest_hour()

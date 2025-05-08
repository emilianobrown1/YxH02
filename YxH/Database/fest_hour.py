from . import db
import random
import datetime
import pytz

db = db.fest_hour
IST = pytz.timezone("Asia/Kolkata")

def today():
    return str(datetime.datetime.now(IST)).split()[0]

async def set_fest_hour() -> int:
    random_hour = random.randint(0, 23)
    await db.insert_one({'date': today(), 'fest_hour': random_hour})
    return random_hour

async def get_fest_hour() -> int:
    x = await db.find_one({'date': today()})
    if x:
        return x['fest_hour']
    return await set_fest_hour()

async def get_time_until_fest() -> str:
    fest_hour = await get_fest_hour()
    now = datetime.datetime.now(IST)
    fest_time = now.replace(hour=fest_hour, minute=0, second=0, microsecond=0)

    if fest_time < now:
        fest_time += datetime.timedelta(days=1)

    time_left = fest_time - now
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes = remainder // 60

    return f"{hours} hour(s) and {minutes} minute(s)"
from . import db
import pickle

db = db.scramble

async def get_scramble(scramble_id):
    x = await db.find_one({"scramble_id": scramble_id})
    if x:
        return pickle.loads(x["info"])

async def get_scrambles_count() -> int:
    x = db.find()
    x = await x.to_list(length=None)
    return len(x)

async def get_scrambles() -> list:
    x = db.find()
    x = await x.to_list(length=None)
    return [pickle.loads(i["info"]) for i in x]
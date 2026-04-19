import os
from typing import Optional

from pymongo import MongoClient

_client: Optional[MongoClient] = None
_database = None


def get_database():
    global _client, _database

    if _database is not None:
        return _database

    if os.getenv("MONGO_USE_MOCK") == "1":
        import mongomock

        _client = mongomock.MongoClient()
        _database = _client[os.getenv("MONGO_DB_NAME", "events_db")]
        return _database

    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    database_name = os.getenv("MONGO_DB_NAME", "events_db")

    _client = MongoClient(mongo_url)
    _database = _client[database_name]
    return _database


def set_test_database(database) -> None:
    global _database
    _database = database


def get_next_sequence(sequence_name: str) -> int:
    counter = get_database().counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=True,
    )
    return counter["value"]


def ensure_indexes() -> None:
    database = get_database()

    database.users.create_index("id", unique=True)
    database.users.create_index("login", unique=True)
    database.users.create_index("email", unique=True)
    database.users.create_index("first_name")
    database.users.create_index("last_name")

    database.events.create_index("id", unique=True)
    database.events.create_index("event_date")
    database.events.create_index("organizer_id")

    database.event_participants.create_index("id", unique=True)
    database.event_participants.create_index("event_id")
    database.event_participants.create_index("user_id")
    database.event_participants.create_index(
        [("event_id", 1), ("user_id", 1)],
        unique=True,
    )


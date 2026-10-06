from app.database.database import init_db
from app.database.models import Detection, EventRecord


def test_database_operations_initialize_models():
    init_db()
    assert Detection.__tablename__
    assert EventRecord.__tablename__

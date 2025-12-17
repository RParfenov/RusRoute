from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

import source.db_system.models as models

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(PROJECT_ROOT, 'source', '.env')

load_dotenv(ENV_PATH)

rel_path = os.getenv('DATABASE_RELATIVE_PATH', os.path.join('db', 'rusroute.db'))

database_path = os.path.join(PROJECT_ROOT, rel_path)
DATABASE_URL = f'sqlite:///{database_path}'

__factory = None

def global_init():
    global __factory
    if __factory is not None:
        return
    # TODO: После завершения работы над бекендом, поставить параметр echo=False
    engine = create_engine(DATABASE_URL)
    __factory = sessionmaker(bind=engine)

    models.SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global __factory
    return __factory()


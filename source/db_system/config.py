import sqlalchemy as sa
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os

import source.db_system.models as models

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
env_path = os.path.join(project_root, 'source', '.env')

load_dotenv(env_path)

rel_path = os.getenv('DATABASE_RELATIVE_PATH', os.path.join('db', 'cache.db'))

DATABASE_PATH = os.path.join(project_root, rel_path)
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

__factory = None

def global_init():
    global __factory
    if __factory is not None:
        return
    # TODO: После завершения работы над бекендом, поставить параметр echo=False
    engine = sa.create_engine(DATABASE_URL, echo=True)
    __factory = orm.sessionmaker(bind=engine)

    models.SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> orm.Session:
    global __factory
    return __factory()

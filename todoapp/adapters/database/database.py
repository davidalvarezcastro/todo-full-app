from contextlib import contextmanager

import attrs
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker


@attrs.define
class DatabaseConnector:
    db_url: str = attrs.field(init=True)
    engine: Engine = attrs.field(init=False)
    SessionLocal: sessionmaker = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.engine = create_engine(url=self.db_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=self.engine)

    def migrate(self):
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.attributes["migrate_from_app"] = True
        alembic_cfg.set_main_option("sqlalchemy.url", self.db_url)

        command.upgrade(alembic_cfg, "head")

    def get_new_connection(self):
        return self.SessionLocal()

    @contextmanager
    def session_scope(self):
        session = self.get_new_connection()

        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

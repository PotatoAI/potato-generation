from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from diff.config import DBConfig
from diff.schema import Base

db_session = False

def db_url(cfg: DBConfig):
    if cfg.adapter == "psql":
        return f"postgresql+psycopg2://{cfg.user}:{cfg.password}@{cfg.host}:{cfg.port}/{cfg.database}"
    if cfg.adapter == "sqlite":
        return f"sqlite:///{cfg.database}"

    return "unknown"


def connect(cfg: DBConfig):
    return create_engine(db_url(cfg), echo=bool(cfg.echo))


def migrate(cfg: DBConfig):
    engine = connect(cfg)
    Base.metadata.create_all(engine)


def session(cfg: DBConfig):
    engine = connect(cfg)
    session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        ))

    Base.query = session.query_property()
    global db_session
    db_session = session

    return session

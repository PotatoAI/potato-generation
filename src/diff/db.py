from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from diff.config import DBConfig
from diff.schema import Base


def db_url(cfg: DBConfig):
    if cfg.adapter == "psql":
        return f"postgresql+psycopg2://{cfg.user}:{cfg.password}@{cfg.host}:{cfg.port}/{cfg.database}"
    if cfg.adapter == "sqlite":
        return f"sqlite:///{cfg.database}"

    return "unknown"


def connect(cfg: DBConfig) -> Engine:
    return create_engine(db_url(cfg), echo=bool(cfg.echo))


def migrate(cfg: DBConfig):
    engine = connect(cfg)
    Base.metadata.create_all(engine)


def init_session(engine: Engine) -> scoped_session:
    session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        ))

    Base.query = session.query_property()

    return session

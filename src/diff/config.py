import yaml
from pydantic import BaseModel
from typing import Optional


class HuggingConfig(BaseModel):
    token: Optional[str]


class DBConfig(BaseModel):
    adapter: str
    database: str
    user: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int]


class Config(BaseModel):
    hf: HuggingConfig
    db: DBConfig


def read(fname) -> Config:
    with open(fname, 'r') as stream:
        return Config(**yaml.safe_load(stream))

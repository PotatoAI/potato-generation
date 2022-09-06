import yaml
from pydantic import BaseModel
from typing import Optional


class HuggingConfig(BaseModel):
    token: Optional[str]


class DBConfig(BaseModel):
    adapter: str
    database: str
    echo: Optional[bool]
    user: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int]


class GenConfig(BaseModel):
    batch_size: int
    batch_count: int
    inference_steps: int


class VideoConfig(BaseModel):
    frames_per_pic: int


class Config(BaseModel):
    hf: HuggingConfig
    db: DBConfig
    gen: GenConfig
    video: VideoConfig


def read(fname) -> Config:
    with open(fname, 'r') as stream:
        return Config(**yaml.safe_load(stream))

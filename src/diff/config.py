import yaml
from logging import info
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
    small_vram: bool = False
    batch_size: int
    batch_count: int
    inference_steps: int


class VideoConfig(BaseModel):
    frames_per_pic: int
    scale: str


class NatsConfig(BaseModel):
    host: str
    port: int
    user: Optional[str]
    password: Optional[str]

    def url(self):
        return f"nats://{self.user}:{self.password}@{self.host}:{self.port}"


class Config(BaseModel):
    hf: HuggingConfig
    db: DBConfig
    gen: GenConfig
    video: VideoConfig
    nats: NatsConfig


global_config: Config


def init_config(fname: str):
    info(f"Reading config from {fname}")
    global global_config
    global_config = read(fname)


def config() -> Config:
    global global_config
    return global_config


def read(fname: str) -> Config:
    with open(fname, 'r') as stream:
        return Config(**yaml.safe_load(stream))

from pydantic import BaseModel


class BaseTask(BaseModel):
    request_id: int
    kind: str = 'upscale'


class GenVideoTask(BaseModel):
    request_id: int
    kind: str = 'gen-video'


class AddAudioTask(BaseModel):
    request_id: int
    video_id: int
    file_path: str
    kind: str = 'add-audio'

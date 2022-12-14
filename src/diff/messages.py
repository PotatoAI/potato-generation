from pydantic import BaseModel


class DiffusionTask(BaseModel):
    uid: str
    request_id: int
    kind: str = 'diffusion'


class UpscaleTask(BaseModel):
    uid: str
    image_id: int
    kind: str = 'upscale'


class GenVideoTask(BaseModel):
    uid: str
    request_id: int
    kind: str = 'gen-video'


class AddAudioTask(BaseModel):
    uid: str
    video_id: int
    file_path: str
    kind: str = 'add-audio'

from diff.image_result import ImagesResult
from logging import warn


class Upscaler:

    def __init__(self):
        self.something = 9

    def upscale(self) -> ImagesResult:
        warn("Upscale not implemented")
        return ImagesResult([], 0, 0)

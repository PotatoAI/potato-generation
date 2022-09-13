import uuid
from PIL import Image
from typing import List, Any
from logging import info
from dataclasses import dataclass

@dataclass
class ImagesResult:
    images: List[Any]
    batch_count: int
    batch_size: int

    def save(
        self,
        request_id: int,
        task_id: int,
        folder: str,
    ) -> List[str]:
        path = f"{folder}/{request_id}"
        os.makedirs(path, exist_ok=True)

        images = []

        for i, img in enumerate(self.images):
            id = uuid.uuid1()
            fname = f"{path}/{task_id}-{i}-{id}.png"
            img.save(fname)
            images.append(fname)

        return images

import torch
import os
from diffusers import StableDiffusionPipeline
from PIL import Image
from torch import autocast
from dataclasses import dataclass
from typing import List, Any
import uuid


def image_grid(imgs, rows, cols):
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


@dataclass
class ImagesResult:
    images: List[Any]
    rows: int
    cols: int

    def grid(self):
        return image_grid(self.images, self.rows, self.cols)

    def save(self, promt: str, task_id: str, it: str, folder: str) -> List[str]:
        path = f"{folder}/{promt}"
        os.makedirs(path, exist_ok=True)

        images = []

        for i, img in enumerate(self.images):
            fname = f"{path}/{task_id}-{it}-{uuid.uuid1()}.png"
            img.save(fname)
            images.append(fname)

        return images


class Generator:
    def __init__(self):
        print('Initializing pipeline')
        pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            revision="fp16",
            torch_dtype=torch.float16,
            use_auth_token=True)
        pipe.bypass_nsfw_filter = True
        print('Moving pipeline to CUDA')
        self.pipe = pipe.to("cuda")

    def generate(self, prompt_str: str, cols=3, rows=1, inference_steps=50):
        prompt = [prompt_str] * cols
        all_images = []

        for i in range(rows):
            with autocast("cuda"):
                images = self.pipe(
                    prompt, num_inference_steps=inference_steps)["sample"]
            all_images.extend(images)

        return ImagesResult(all_images, rows, cols)

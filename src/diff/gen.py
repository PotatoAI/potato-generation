import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
from torch import autocast
from dataclasses import dataclass
from typing import List, Any


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

    def save(self, folder: str):
        for i, img in enumerate(self.images):
            img.save(f"{folder}/{i}.png")


class Generator:
    def __init__(self):
        pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            revision="fp16",
            torch_dtype=torch.float16,
            use_auth_token=True)
        pipe.bypass_nsfw_filter = True
        self.pipe = pipe.to("cuda")

    def generate(self, prompt_str: str, cols=3, rows=1):
        prompt = [prompt_str] * cols
        all_images = []

        for i in range(rows):
            with autocast("cuda"):
                images = self.pipe(prompt)["sample"]
            all_images.extend(images)

        return ImagesResult(all_images, rows, cols)

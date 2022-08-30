import torch
import os
from diffusers import StableDiffusionPipeline
from PIL import Image
from torch import autocast
from dataclasses import dataclass
from typing import List, Any


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
            fname = f"{path}/{task_id}-{i}.png"
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

    def generate(self,
                 prompt_str: str,
                 batch_size=3,
                 batch_count=1,
                 inference_steps=50):
        prompt = [prompt_str] * batch_size
        all_images = []

        for i in range(batch_count):
            with autocast("cuda"):
                images = self.pipe(
                    prompt, num_inference_steps=inference_steps)["sample"]
            all_images.extend(images)

        return ImagesResult(all_images, batch_count, batch_size)

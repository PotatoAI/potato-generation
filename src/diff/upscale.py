import os
from diff.image_result import ImagesResult
from logging import warn, info
from diff.storage import get_request, read_binary_file


class Upscaler:

    def __init__(self):
        self.runtime_path = "BSRGAN"

    def upscale(self, rid: int) -> ImagesResult:
        images = []
        img_folder = "output/tmp"
        request = get_request(rid)

        for image in request.images:
            print(f"Image {image.oid}")

            fname = f"{self.runtime_path}/input.png"
            with open(fname, 'wb') as fb:
                info(f"Writing {fname}")
                fb.write(read_binary_file(image.oid))

            command = f"cd {self.runtime_path} && make upscale"
            info(command)
            img_out_fname = f"{image.id}.png"
            os.makedirs(img_folder, exist_ok=True)
            command = f"cp {self.runtime_path}/output.png {img_folder}/{img_out_fname}"
            info(command)
            # images.append(img_out_fname)

        warn(f"Upscale not implemented {request.id}")
        return ImagesResult(images, 0, len(images))

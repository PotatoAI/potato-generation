import os
from typing import List
from logging import warn, info
from diff.storage import get_request, read_binary_file, save_binary_file, commit


class Upscaler:
    def __init__(self):
        self.runtime_path = "BSRGAN"

    def upscale(self, rid: int):
        img_folder = "output/tmp"
        request = get_request(rid)

        os.makedirs(img_folder, exist_ok=True)

        for image in request.images:
            fname = f"{self.runtime_path}/input.png"
            with open(fname, 'wb') as fb:
                info(f"Writing {fname}")
                fb.write(read_binary_file(image.oid))

            command = f"cd {self.runtime_path} && make upscale"
            info(command)
            os.system(command)

            img_out_fname = f"{image.id}.png"
            img = f"{img_folder}/{img_out_fname}"
            command = f"cp {self.runtime_path}/output.png {img}"
            info(command)
            os.system(command)

            image.hqoid = save_binary_file(fname)
            info(f"Saved HQ version of image#{image.id}")
            commit()

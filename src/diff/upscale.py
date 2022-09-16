import os
from typing import List
from logging import warn, info
from diff.storage import get_image, read_binary_file, save_binary_file, commit


class Upscaler:
    def __init__(self):
        self.runtime_path = "BSRGAN"

    def upscale(self, img_id: int):
        img_folder = "output/tmp"
        os.makedirs(img_folder, exist_ok=True)

        image = get_image(img_id)

        if image.hqoid:
            info(f"Skipping {image.id} since it has HQ version")
            return

        fname = f"{self.runtime_path}/input.png"
        with open(fname, 'wb') as fb:
            info(f"Writing {fname}")
            fb.write(read_binary_file(image.oid))

        command = f"cd {self.runtime_path} && make upscale"
        info(command)
        os.system(command)

        img_out_fname = f"{image.id}-hq.png"
        img = f"{img_folder}/{img_out_fname}"
        command = f"cp -f {self.runtime_path}/output.png {img}"
        info(command)
        os.system(command)

        image.hqoid = save_binary_file(img)
        info(f"Saved HQ version of image#{image.id} -> {image.hqoid}")
        commit()

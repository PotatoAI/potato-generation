from huggingface_hub.hf_api import HfApi, HfFolder
from getpass import getpass
from typing import Optional


# Tokens can be found here https://huggingface.co/settings/tokens
# Dont forget to request access here https://huggingface.co/CompVis/stable-diffusion-v1-4
def login(hf_token: Optional[str] = None):
    token = HfFolder.get_token()

    if not token:
        if hf_token:
            token = hf_token
        else:
            token = getpass('Give me token: ')

    hf_api = HfApi()
    hf_api.set_access_token(token)
    HfFolder.save_token(token)

import os
from sys import platform

if platform == "linux" or platform == "linux2":
    from dotenv import load_dotenv

    load_dotenv()


def get_env_variable(arg: str):
    return os.getenv(arg)

import os
from abc import ABC
from typing import Final


class Env(ABC):
    TOKEN: Final = os.environ.get('DISCORD_TOKEN', 'define me!')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY','define me!')
#!/usr/bin/env python
# PlaywrightGym: Visual Web envs for RL Agent training
__version__ = "0.0.3"

import sys
import os

from gym.envs.registration import register

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from playwrightgym.playwright_env import ACTION_KEY_MAP


_AVAILABLE_ENVS = {
    "LoginFormVisual-v0": {
        "entry_point": "playwrightgym.playwright_env:PlaywrightEnv",
        "discription": "Login form with username, password",
    },
}


for env_id, val in _AVAILABLE_ENVS.items():
    register(id=env_id, entry_point=val.get("entry_point"))

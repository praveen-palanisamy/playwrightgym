#!/usr/bin/env python
# Gather demonstrations and save to RLLib-compatible file format

import gym
import playwrightgym
import numpy as np
import os
import sys
import cv2

from ray.rllib.evaluation.sample_batch_builder import SampleBatchBuilder
from ray.rllib.offline.json_writer import JsonWriter

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from demonstrator import Demonstrator

SAVE_DIR = "generated_demonstrations"
if not os.path.isdir(SAVE_DIR):
    os.makedirs(SAVE_DIR)


def preprocess_obs(obs):
    return cv2.resize(obs, (84, 84), interpolation=cv2.INTER_AREA)


if __name__ == "__main__":
    batch_builder = SampleBatchBuilder()
    writer = JsonWriter(SAVE_DIR)
    env_name = "LoginFormVisual-v0"
    demonstrator = Demonstrator(env_name)

    for episode in range(2):
        obs = demonstrator.env.reset()
        prev_action = np.zeros_like(demonstrator.env.action_space.sample())
        prev_reward = 0
        done = False
        step = 0
        while not done:
            action = demonstrator.get_action(obs)
            new_obs, reward, done, info = demonstrator.env.step(action)
            batch_builder.add_values(
                t=step,
                eps_id=episode,
                agent_index=0,
                obs=preprocess_obs(obs),
                actions=action,
                rewards=reward,
                prev_actions=prev_action,
                prev_rewards=prev_reward,
                dones=done,
                infos=info,
                new_obs=preprocess_obs(new_obs),
            )
            obs = new_obs
            prev_action = action
            prev_reward = reward
            step += 1
            print(
                f"Ep#:{episode} step#:{step} action:{action} rew:{reward} done:{done}"
            )
        writer.write(batch_builder.build_and_reset())

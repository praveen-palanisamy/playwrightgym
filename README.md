# PlaywrightGym - Train RL Agents for Web tasks

Web-Browser-based learning environments for Deep Reinforcement Learning.

## Usage

```python
import gym
import playwrightgym
env = gym.make("LoginFormVisual-v0")
```

## Examples

- [examples/demonstrator.py](https://github.com/praveen-palanisamy/playwrightgym/examples/demonstrator.py): Starter class to get human/manual demonstrations
- [examples/gather_demonstrations.py](https://github.com/praveen-palanisamy/playwrightgym/examples/gather_demonstrations.py): Starter script to gather human/manual demonstrations and store in RLLib-compatible file format for offline RL

## Dev Setup

1. Install [python-poetry](https://python-poetry.org/): `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`
1. Clone and `cd` to this projects: `git clone https://github.com/praveen-palanisamy/playwrightgym && cd playwrightgym`
1. Activate python venv: `poetry shell`
1. Install dependencies and `playwrightgym` in editable mode: `poetry install`
1. Install browsers for playwright: `playwright install`
1. Ready!

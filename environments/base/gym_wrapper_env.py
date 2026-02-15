import gymnasium as gym
from environments.base.env_system import EnvSystem

class EnvWrapper(gym.Wrapper):

    def __init__(self, base_env, env: EnvSystem):
        super().__init__(base_env)
        self.created_env = env

    def step(self, actions):

        actions = self.created_env.pre_action(actions, self.env)

        obs, reward, terminated, truncated, info = self.env.step(actions)

        self.created_env.post_step(actions, self.env)

        obs = self.created_env.modify_obs(obs, self.env)
        reward = self.created_env.modify_reward(reward, self.env)
        terminated = self.created_env.check_termination(terminated, self.env)

        return obs, reward, terminated, truncated, info

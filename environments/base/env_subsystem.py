from abc import ABC

class EnvSubsystem(ABC):

    after = ()

    def pre_action(self, actions, base_env, env):
        return actions
    
    def post_step(self, base_env, env):
        pass

    def modify_obs(self, obs, base_env, env):
        return obs
    
    def modify_reward(self, reward, base_env, env):
        return reward
    
    def check_termination(self, terminated, base_env, env):
        return terminated
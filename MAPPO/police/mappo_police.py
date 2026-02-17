import torch
import torch.distributions as D

class Policy:
    def __init__(self, actor_net):
        self.actor = actor_net

    def act(self, obs):
        """
        obs: Tensor
        """
        logits = self.actor(obs)
        dist = D.Categorical(logits=logits)

        action = dist.sample()
        log_prob = dist.log_prob(action)
        entropy = dist.entropy()

        return action, log_prob, entropy

    def log_prob(self, obs, action):
        if action is not torch.Tensor:
            action = torch.tensor(action)
        logits = self.actor(obs)
        dist = D.Categorical(logits=logits)
        return dist.log_prob(action), dist.entropy()

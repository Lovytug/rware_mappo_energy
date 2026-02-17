class RolloutBuffer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.obs = []        # list[list[obs_i]]
        self.states = []
        self.actions = []    # list[list[action_i]]
        self.log_probs = []  # list[list[log_prob_i]]
        self.rewards = []    # list[float]
        self.values = []     # list[float]
        self.dones = []      # list[bool]

    def add(self, obs, state, actions, log_probs, value, reward, done):
        self.obs.append(obs)
        self.states.append(state)
        self.actions.append(actions)
        self.log_probs.append(log_probs)
        self.values.append(value)
        self.rewards.append(reward)
        self.dones.append(done)

    def compute_returns_advantages(self, gamma, lam):
        T = len(self.rewards)

        returns = [None] * T
        advantages = [None] * T

        next_value = 0.0
        gae = 0.0

        for t in reversed(range(T)):
            rewards_t = self.rewards[t]

            if isinstance(rewards_t, (list, tuple)):
                rewards_t = sum(rewards_t) / len(rewards_t)

            delta = (
                rewards_t
                + gamma * next_value * (1 - self.dones[t])
                - self.values[t]
            )

            gae = delta + gamma * lam * (1 - self.dones[t]) * gae

            advantages[t] = gae
            returns[t] = gae + self.values[t]

            next_value = self.values[t]

        return returns, advantages

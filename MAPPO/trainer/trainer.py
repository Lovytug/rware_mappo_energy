import torch
import torch.optim as optim
from MAPPO.buffer.multi_agent_buffer import RolloutBuffer

class MAPPOTrainer:
    def __init__(
        self,
        factory,
        policy,
        critic,
        actor_lr=3e-4,
        critic_lr=3e-4,
        gamma=0.99,
        lam=0.95,
        clip_eps=0.2,
        entropy_coef=0.01,
        value_coef=0.5,
        device="cpu",
    ):
        self.factory = factory
        self.policy = policy
        self.critic = critic

        self.gamma = gamma
        self.lam = lam
        self.clip_eps = clip_eps
        self.entropy_coef = entropy_coef
        self.value_coef = value_coef

        self.device = device

        self.actor_optim = optim.Adam(
            self.policy.actor.parameters(), lr=actor_lr
        )
        self.critic_optim = optim.Adam(
            self.critic.parameters(), lr=critic_lr
        )

    def collect_rollout(self, ctx, rollout_len):
        buffer = RolloutBuffer()
        obs, _ = ctx.env.reset()

        first_step = True
        for _ in range(rollout_len):
            obs_tensors = [
                torch.tensor(
                    (list(o) + [0.0, 0.0]) if first_step else o,
                    dtype=torch.float32,
                    device=self.device
                )
                for o in obs
            ]
            
            first_step = False
        

            actions = []
            log_probs = []

            for o in obs_tensors:
                a, lp, _ = self.policy.act(o)
                actions.append(a)
                log_probs.append(lp.detach())

            ctx.repos.refresh()
            state = ctx.assembler.build(ctx.repos)
            with torch.no_grad():
                value = self.critic(state)

            actions = [int(a) for a in actions]
            next_obs, reward, terminated, truncated, _ = ctx.env.step(
                tuple(actions)
            )

            reward = list(reward)

            buffer.add(
                obs=obs_tensors,
                state=state,
                actions=actions,
                log_probs=log_probs,
                value=value.detach(),
                reward=reward,
                done=terminated,
            )

            obs = next_obs
            if terminated or truncated:
                break

        return buffer

    def update(self, buffer, ppo_epochs=4):
        returns, advantages = buffer.compute_returns_advantages(
            self.gamma, self.lam
        )

        for _ in range(ppo_epochs):
            for t in range(len(buffer.obs)):
                obs = buffer.obs[t]
                state = buffer.states[t]
                actions = buffer.actions[t]
                old_log_probs = buffer.log_probs[t]

                advantage = torch.tensor(
                    advantages[t], device=self.device
                )
                ret = torch.tensor(
                    returns[t], device=self.device
                )

                # ---- critic ----
                value = self.critic(state)
                critic_loss = (value - ret).pow(2)

                self.critic_optim.zero_grad()
                critic_loss.backward()
                self.critic_optim.step()

                # ---- actor ----
                new_log_probs = []
                entropies = []

                for o, a in zip(obs, actions):
                    lp, ent = self.policy.log_prob(o, a)
                    new_log_probs.append(lp)
                    entropies.append(ent)

                new_log_probs = torch.stack(new_log_probs)
                old_log_probs = torch.stack(old_log_probs)
                entropies = torch.stack(entropies)

                ratio = torch.exp(new_log_probs - old_log_probs)

                surr1 = ratio * advantage
                surr2 = torch.clamp(
                    ratio, 1 - self.clip_eps, 1 + self.clip_eps
                ) * advantage

                actor_loss = -torch.min(surr1, surr2).mean()
                entropy_loss = -entropies.mean()

                total_loss = (
                    actor_loss
                    + self.entropy_coef * entropy_loss
                )

                self.actor_optim.zero_grad()
                total_loss.backward()
                self.actor_optim.step()

    def train(self, num_updates, rollout_len):
        for _ in range(num_updates):
            ctx = self.factory.create()
            buffer = self.collect_rollout(ctx, rollout_len)
            self.update(buffer)

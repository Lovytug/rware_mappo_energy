from typing import TypeVar, Generic, Any
from abc import ABC
from environments.base.env_subsystem import EnvSubsystem
from collections import deque

T = TypeVar("T", bound=EnvSubsystem)
class EnvSystem(Generic[T], ABC):

    def __init__(self, subsystem: list[T]):
        self.subsystems = topological_sort_subsystems(subsystem)

    def get(self, subsystem_type: type[T]) -> T:
        for s in self.subsystems:
            if isinstance(s, subsystem_type):
                return s
        raise KeyError(subsystem_type)
            
    def pre_action(self, actions: list[int], rware_env):
        for s in self.subsystems:
            actions = s.pre_action(actions, rware_env, self)
        return actions
    
    def post_step(self, action:list[int], rware_env):
        for s in self.subsystems:
            s.post_step(action, rware_env, self)

    def modify_reward(self, reward: list[float], rware_env):
        for s in self.subsystems:
            reward = s.modify_reward(reward, rware_env, self)
        return reward
    
    def modify_obs(self, obs: list[Any], rware_env):
        for s in self.subsystems:
            obs = s.modify_obs(obs, rware_env, self)
        return obs

    def check_termination(self, terminated: bool, rware_env):
        for s in self.subsystems:
            terminated = s.check_termination(terminated, rware_env, self)
        return terminated


def topological_sort_subsystems(subsystems: list[EnvSubsystem]) -> list[EnvSubsystem]:
    """Топологическая сортировка подсистем по зависимостям `after`."""

    type_map = {type(s): s for s in subsystems}

    graph = {s: set() for s in subsystems}
    in_degree = {s: 0 for s in subsystems}

    # Строим граф
    for sub in subsystems:
        for dep_type in sub.after:
            dep = type_map.get(dep_type)
            if dep is None:
                continue

            graph[dep].add(sub)
            in_degree[sub] += 1

    # Kahn algorithm
    queue = deque(s for s in subsystems if in_degree[s] == 0)
    result = []

    while queue:
        current = queue.popleft()
        result.append(current)

        for nxt in graph[current]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)

    if len(result) != len(subsystems):
        remaining = [type(s).__name__ for s in subsystems if s not in result]
        raise ValueError(f"Обнаружен цикл зависимостей: {remaining}")

    return result
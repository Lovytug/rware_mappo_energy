class PriorityCompose:

    def __init__(self):
        self._wrappers = []

    def register(self, wrapper_cls, **kwargs):
        self._wrappers.append((wrapper_cls, kwargs))
        return self
    
    def build(self, env):
        sorted_wrappers = sorted(
            self._wrappers,
            key=lambda w: w[0].priority
        )

        for wrapper_cls, kwargs in sorted_wrappers:
            env = wrapper_cls(env, **kwargs)

        return env
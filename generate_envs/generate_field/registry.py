from generate_envs.generate_field.field_generator import FieldGenerator

class GeneratorRegisrty:
    def __init__(self):
        self.generators: list[FieldGenerator] = []

    def regist(self, gen: FieldGenerator):
        self.generators.append(gen)
        self.generators.sort(key=lambda g: g.phase)

    def resolve(self, name, cfg, ctx):
        for gen in self.generators:
            if gen.can_handle(cfg):
                return gen.generate(name, cfg, ctx)
            
        raise ValueError(f"Нет генератора для поля {name}. Пришлом {cfg}")
from environments.base.extract_field_config.json.field_extractor import FieldExtactor    
from environments.base.builder.builder_conf import RuntimeContext

class RegisterExtractors:

    def __init__(self):
        self.ctx: RuntimeContext | None = None
        self.generators: list[FieldExtactor] = []

    def set_context(self, ctx: RuntimeContext):
        self.ctx = ctx
        
    def regist(self, gen: FieldExtactor):
        self.generators.append(gen)
        self.generators.sort(key=lambda g: g.phase)

    def regist(self, gens: list[FieldExtactor]):
        self.generators.extend(gens)
        self.generators.sort(key=lambda g: g.phase)

    def resolve(self, name, cfg):
        for gen in self.generators:
            if gen.can_handle(cfg):
                return gen.generate(name, cfg, self.ctx)
            
        raise ValueError(f"Нет генератора для поля {name}. Пришлом {cfg}")
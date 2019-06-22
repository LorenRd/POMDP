from models.model import Model

class TigerSampleModel(Model):
    def __init__(self, env):
        Model.__init__(self, env)
        size, num_rocks = self.model_spec.split('x')
        self.state = int(size)
        self.num_rocks = int(num_rocks)

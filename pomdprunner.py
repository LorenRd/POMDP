from parsers import PomdpParser
from pathlib import Path
from models import TigerSampleModel, Model
from solvers import POMCP, PBVI

class pomdprunner():

    def __init__(self, problem, algorithm, mode):
        self.run(problem, algorithm, mode)

    def create_model(self, problema):
        MODELS = {
            'A': TigerSampleModel,

        }

        return MODELS.get(problema['model_name'], Model)(problema)


    def create_solver(self, algorithm, model):
        SOLVERS = {
            'A': PBVI,
            'B': POMCP,
        }
        return SOLVERS.get(algorithm)(model)


    def run(self,problem,algorithm, mode):
        data_folder = Path("files")
        datos_tigre = data_folder / "TigerProblemData.POMDP"

        with PomdpParser(datos_tigre) as ctx:
            modelo = self.create_model(ctx.copy_env())
            pomdp = self.create_solver(algorithm, modelo)
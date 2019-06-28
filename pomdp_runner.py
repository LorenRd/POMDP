import os

from models import RockSampleModel, Model
from solvers import POMCP, PBVI
from parsers import PomdpParser, GraphViz
from logger import Logger as log
import numpy as math


class PomdpRunner:

    def __init__(self, params):
        self.params = params
        if params.logfile is not None:
            log.new(params.logfile)

    def create_model(self, env_configs):
        MODELS = {
            'RockSample': RockSampleModel,
        }
        return MODELS.get(env_configs['model_name'], Model)(env_configs)

    def create_solver(self, algo, model):
        SOLVERS = {
            'pbvi': PBVI,
            'pomcp': POMCP,
        }
        return SOLVERS.get(algo)(model)

    def snapshot_tree(self, visualiser, tree, filename):
        visualiser.update(tree.root)
        visualiser.render('./dev/snapshots/{}'.format(filename))  # TODO: parametrise the dev folder path

    def run(self, modo, problema, algo, T, **kwargs):
        steps = math.array([], float)
        rewards = math.array([], float)
        if modo == "Benchmark":
            c = 0
        else:
            c = 29
        while c < 30:
            c += 1
            if modo == "Benchmark":
                log.info("===================== Ejecucion " + str(c) + '=====================' )
            visualiser = GraphViz(description='tmp')
            params, pomdp = self.params, None
            total_rewards, budget = 0, params.budget

            with PomdpParser(params.env_config) as ctx:
                model = self.create_model(ctx.copy_env())
                pomdp = self.create_solver(algo, model)

                belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

                if algo == 'pbvi':
                    belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                    pomdp.add_configs(belief_points)
                elif algo == 'pomcp':
                    pomdp.add_configs(budget, belief, **kwargs)

            if modo != "Benchmark":
                log.info('''
                ++++++++++++++++++++++
                    Estado inicial:  {}
                    Presupuesto:  {}
                    Creencia: {}
                    Horizonte de tiempo: {}
                    Numero de juegos maximo: {}
                ++++++++++++++++++++++'''.format(model.curr_state, budget, belief, T, params.max_play))
            condicion_parada = False
            i = 0
            while not condicion_parada and params.max_play > i:
                i += 1
                pomdp.solve(T, modo)
                action = pomdp.get_action(belief)
                new_state, obs, reward, cost = pomdp.take_action(action)

                if problema == "Tigre":
                    condicion_parada = action == "open-left" or action == "open-right"
                elif problema == "LaserTag":
                    condicion_parada = action == "Catch"
                elif problema == "Recipientes":
                    condicion_parada = action == "bebe-izq" or action == "bebe-med" or action == "bebe-der"

                if params.snapshot and isinstance(pomdp, POMCP):
                    self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))

                belief = pomdp.update_belief(belief, action, obs)
                total_rewards += reward
                budget -= cost

                if modo == "Interactivo":
                    log.info('\n'.join([
                      'Accion tomada: {}'.format(action),
                      'Observacion: {}'.format(obs),
                      'Recompensa: {}'.format(reward),
                      'Presupuesto: {}'.format(budget),
                      'Nuevo estado: {}'.format(new_state),
                      'Nueva creencia: {}'.format(belief),
                      'Paso numero: {}'.format(i),
                      '=' * 20
                    ]))

                if budget <= 0:
                    log.info('Se ha sobrepasado el presupuesto establecido.')
                if params.max_play != 'inf' and params.max_play <= i:
                    log.info('Se ha sobrepasado el número máximo de pasos establecido.')

            log.info('{} pasos ejecutados. Recompensa total acumulada = {}\n'.format(i, total_rewards))
            steps = math.append(steps, i)
            rewards = math.append(rewards, total_rewards)

        if modo == "Benchmark":
            mean_steps = steps.mean()
            std_steps = steps.std()
            mean_rewards = rewards.mean()
            std_rewards = rewards.std()
            print("#########################################################################################")
            print("#    RESULTADOS DEL BENCHMARK:")
            print("#    Valor medio pasos: ", mean_steps)
            print("#    Desviacion tipica pasos: ", std_steps)
            print("#    Valor medio recompensas: ", mean_rewards)
            print("#    Desviacion tipica recompensas: ", std_rewards)
            print("#########################################################################################")

        return pomdp

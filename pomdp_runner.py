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
        """
        Builder method for creating model (i,e, agent's environment) instance
        :param env_configs: the complete encapsulation of environment's dynamics
        :return: concrete model
        """
        MODELS = {
            'RockSample': RockSampleModel,
        }
        return MODELS.get(env_configs['model_name'], Model)(env_configs)

    def create_solver(self, algo, model):
        """
        Builder method for creating solver instance
        :param algo: algorithm name
        :param model: model instance, e.g, TigerModel or RockSampleModel
        :return: concrete solver
        """
        SOLVERS = {
            'pbvi': PBVI,
            'pomcp': POMCP,
        }
        return SOLVERS.get(algo)(model)

    def snapshot_tree(self, visualiser, tree, filename):
        visualiser.update(tree.root)
        visualiser.render('./dev/snapshots/{}'.format(filename))  # TODO: parametrise the dev folder path

    def run(self, modo, algo, T, **kwargs):
        steps = math.array([], float)
        rewards = math.array([], float)
        if modo == "Benchmark":
            c = 0
        else:
            c = 29
        while c < 30:
            c += 1
            visualiser = GraphViz(description='tmp')
            params, pomdp = self.params, None
            total_rewards, budget = 0, params.budget

            #log.info('~~~ initialising ~~~')
            with PomdpParser(params.env_config) as ctx:
                # creates model and solver
                model = self.create_model(ctx.copy_env())
                pomdp = self.create_solver(algo, model)

                # supply additional algo params
                belief = ctx.random_beliefs() if params.random_prior else ctx.generate_beliefs()

                if algo == 'pbvi':
                    belief_points = ctx.generate_belief_points(kwargs['stepsize'])
                    pomdp.add_configs(belief_points)
                elif algo == 'pomcp':
                    pomdp.add_configs(budget, belief, **kwargs)

            # have fun!
            if modo != "Benchmark":
                log.info('''
                ++++++++++++++++++++++
                    Estado inicial:  {}
                    Presupuesto:  {}
                    Creencia: {}
                    Horizonte de tiempo: {}
                    Numero de juegos maximo: {}
                ++++++++++++++++++++++'''.format(model.curr_state, budget, belief, T, params.max_play))

            for i in range(params.max_play):
                # plan, take action and receive environment feedbacks
                pomdp.solve(T, modo)
                action = pomdp.get_action(belief)
                new_state, obs, reward, cost = pomdp.take_action(action)

                if params.snapshot and isinstance(pomdp, POMCP):
                    # takes snapshot of belief tree before it gets updated
                    self.snapshot_tree(visualiser, pomdp.tree, '{}.gv'.format(i))

                # update states
                belief = pomdp.update_belief(belief, action, obs)
                total_rewards += reward
                budget -= cost

                # print ino
                if modo == "Iterativo":
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
                    log.info('Budget spent.')
            log.info('{} juegos. Recompensa total acumulada = {}'.format(i , total_rewards))
            steps = math.append(steps, i)
            rewards = math.append(rewards, total_rewards)
        if modo == "Benchmark":
            mean_steps = steps.mean()
            std_steps = steps.std()
            mean_rewards = rewards.mean()
            std_rewards = rewards.mean()
            print("Valor medio pasos: ", mean_steps)
            print("Desviacion tipica pasos: ", std_steps)
            print("Valor medio recompensas: ", mean_rewards)
            print("Desviacion tipica pasos: ", std_rewards)
        return pomdp

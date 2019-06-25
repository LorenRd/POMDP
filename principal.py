import argparse
import os
import json
import multiprocessing
from pomdp_runner import PomdpRunner
from util import RunnerParams


if __name__ == '__main__':
    print("POMDP por Lorenzo y Jose Manuel")
    fin = False
    while not fin:
        print("Seleccione un problema:")
        print("[1] - Tigre")
        print("[2] - LaserTag")
        print("[3] - Problema1")
        print("[4] - Problema2")
        opcionesProblema = [1, 2, 3, 4]

        numeroCorrecto = False
        problema = ""
        while problema == "":
            numProblema = int(input())
            if numProblema in opcionesProblema:
                if numProblema == 1:
                    problema = "Tigre"
                    print("Problema seleccionado:", problema)
                elif numProblema == 2:
                    problema = "LaserTag"
                    print("Problema seleccionado:", problema)
                elif numProblema == 3:
                    problema = "Problema 1"
                    print("Problema seleccionado:", problema)
                else:
                    problema = "Problema 2"
                    print("Problema seleccionado:", problema)
            else:
                print("El número seleccionado no corresponde a ningún problema.")

        print("Seleccione un algoritmo resolvedor:")
        print("[1] - POMCP")
        print("[2] - PVBI")
        opcionesAlgoritmo = ["pomcp", "pvbi"]
        algoritmo = ""
        while algoritmo == "":
            numAlgoritmo = int(input())
            if numAlgoritmo == 1:
                algoritmo = "pomcp"
                print("Algoritmo seleccionado:", algoritmo)
            elif numAlgoritmo == 2:
                algoritmo = "pvbi"
                print("Algoritmo seleccionado:", algoritmo)
            else:
                print("El número introducido no corresponde a ningún algoritmo.")

        print("Seleccione un modo de ejecución:")
        print("[1] - Iterativo")
        print("[2] - Silencioso")
        print("[3] - Benchmark")
        opcionesModo = [1, 2, 3]
        modo = ""
        while modo == "":
            numModo = int(input())
            if numModo == 1:
                modo = "Iterativo"
                print("Modo de ejecución seleccionado:", modo)
            elif numModo == 2:
                modo = "Silencioso"
                print("Modo de ejecución seleccionado:", modo)
            elif numModo == 3:
                modo = "Benchmark"
                print("Modo de ejecución seleccionado:", modo)
            else:
                print("El número introducido no corresponde a ningún modo de ejecución.")
        fin = True

    """
    Parse generic params for the POMDP runner, and configurations for the chosen algorithm.
    Algorithm configurations the JSON files in ./configs

    Example usage:
        > python main.py pomcp --env Tiger-2D.POMDP
        > python main.py pbvi --env Tiger-2D.POMDP
    """
    parser = argparse.ArgumentParser(description='Solve pomdp')
    parser.add_argument('--config', type=str, default=algoritmo, help='The file name of algorithm configuration (without JSON extension)') #pbvi o pomcp
    parser.add_argument('--env', type=str, default=problema+".POMDP", help='The name of environment\'s config file')#.pomdp
    parser.add_argument('--budget', type=float, default=float('inf'), help='The total action budget (default to inf)')
    parser.add_argument('--snapshot', type=bool, default=False, help='Whether to snapshot the belief tree after each episode')
    parser.add_argument('--logfile', type=str, default=None, help='Logfile path')
    parser.add_argument('--random_prior', type=bool, default=False, help='Whether or not to use a randomly generated distribution as prior belief, default to False')
    parser.add_argument('--max_play', type=int, default=10, help='Maximum number of play steps')

    args = vars(parser.parse_args())
    params = RunnerParams(**args)

    with open(params.algo_config) as algo_config:
        algo_params = json.load(algo_config)
        runner = PomdpRunner(params)

        runner.run(modo, **algo_params)
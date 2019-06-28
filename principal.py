import argparse
import os
import json
import multiprocessing
from pomdp_runner import PomdpRunner
from util import RunnerParams


if __name__ == '__main__':
    fin = False
    while not fin:
        print("Seleccione un problema:")
        print("[1] - Tigre")
        print("[2] - LaserTag")
        print("[3] - Recipientes")
        print("[4] - Rocksample")
        opciones_problema = [1, 2, 3, 4]

        numero_correcto = False
        problema = ""
        while problema == "":
            num_problema = int(input())
            if num_problema in opciones_problema:
                if num_problema == 1:
                    problema = "Tigre"
                    print("Problema seleccionado:", problema)
                elif num_problema == 2:
                    problema = "LaserTag"
                    budget = float('inf')
                    print("Problema seleccionado:", problema)
                    num_intentos = float('inf')
                elif num_problema == 3:
                    problema = "Recipientes"
                    print("Problema seleccionado:", problema)
                else:
                    problema = "Rocksample"
                    budget = float('inf')
                    print("Problema seleccionado:", problema)

                print("Maximo numero de intentos: ", end="")
                max_play = input()
                if max_play == "":
                    max_play = float('inf')
                if problema == "Tigre" or problema == "Recipientes":
                    print("Maximo presupuesto: ", end="")
                    budget = input()
                    if budget == "":
                        budget = float('inf')
            else:
                print("El número seleccionado no corresponde a ningún problema.")

        opciones_algoritmo = ["pomcp", "pbvi"]
        algoritmo = ""
        while algoritmo == "":
            print("Seleccione un algoritmo resolvedor:")
            print("[1] - POMCP")
            print("[2] - PBVI")
            num_algoritmo = int(input())
            if num_algoritmo == 1:
                algoritmo = "pomcp"
                print("Algoritmo seleccionado:", algoritmo)
            elif num_algoritmo == 2:
                algoritmo = "pbvi"
                print("Algoritmo seleccionado:", algoritmo)
            else:
                print("El número introducido no corresponde a ningún algoritmo.")

        opciones_modo = [1, 2, 3]
        modo = ""
        while modo == "":
            print("Seleccione un modo de ejecución:")
            print("[1] - Interactivo")
            print("[2] - Silencioso")
            print("[3] - Benchmark")
            numModo = int(input())
            if numModo == 1:
                modo = "Interactivo"
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

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default=algoritmo)
    parser.add_argument('--env', type=str, default=problema + ".POMDP")
    parser.add_argument('--budget', type=float, default=budget)
    parser.add_argument('--snapshot', type=bool, default=False)
    parser.add_argument('--logfile', type=str, default=None)
    parser.add_argument('--random_prior', type=bool, default=False)
    parser.add_argument('--max_play', type=int, default=max_play)

    args = vars(parser.parse_args())
    params = RunnerParams(**args)

    with open(params.algo_config) as algo_config:
        algo_params = json.load(algo_config)
        runner = PomdpRunner(params)

        runner.run(modo, problema, **algo_params)
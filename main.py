from pomdprunner import pomdprunner

def solve_algorithm (problem):
    while True:
        algorithm = input("Elige un algoritmo resolvedor: [A] POMCP, [B] PBVI \n").upper()
        if algorithm not in "AB" or len(algorithm) != 1:
            print("Elige un algoritmo resolvedor \n")
        if action == 'A':
            print("Elegiste POMCP!")
            break
        elif action == 'B':
            print("Elegiste PBVI!")
        break
    execution_mode(problem, algorithm)

def execution_mode (problem, algorithm):
    while True:
        mode = input("Elige un modo de ejecucion: [A] INTERACTIVA, [B] SILECIONSA, [C] BENCHMARK \n").upper()
        if mode not in "ABC" or len(mode) != 1:
            print("Elige un algoritmo resolvedor \n")
        if action == 'A':
            print("INTERACTIVA!")
            break
        elif action == 'B':
            print("SILENCIOSA!")
            break
        elif action == 'C':
            print("BENCHMARK -> 30 SIMULACIONES SILENCIOSAS!")
            break

    pomdprunner(problem, algorithm, mode)



if __name__ == '__main__':
    print("POMDP por Lorenzo y Jose Manuel")
    while True:
        action = input("Elige un problema: [A] Tigre, [B] Tag, [C] Problema 1, [D] Problema 2 \n").upper()
        if action not in "ABCD" or len(action) != 1:
            print("Elige un problema de la lista\n")
        if action == 'A':
            print("Elegiste Tigre!")
            solve_algorithm(action)
            break
        elif action == 'B':
            print("Elegiste Tag!")
            solve_algorithm(action)
            break
        elif action == 'C':
            print("Elegiste el problema 1!")
            solve_algorithm(action)
            break
        elif action == 'D':
            print("Elegiste el problema 2!")
            solve_algorithm(action)
            break

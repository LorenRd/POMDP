if __name__ == '__main__':
    print("POMDP por Lorenzo y Jose Manuel")
    while True:
        action = input("Elige un problema: [A] Tigre, [B] Tag, [C] Problema 1, [D] Problema 2").upper()
        if action not in "ABCD" or len(action) != 1:
            print("Elige un problema de la lista")
        if action == 'A':
            print("Elegiste Tigre!")
        elif action == 'B':
            print("Elegiste Tigre!")
        elif action == 'C':
            print("Elegiste el problema 1!")
        elif action == 'D':
            print("Elegiste el problema 2!")



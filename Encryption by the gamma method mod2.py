import random

gamma_len = 8                                           #Длина гаммы

def gamma():                                             #генерация гаммы случайным образом
    g = []
    gg = ""
    for i in range(gamma_len):
        g.append(random.randint(32, 175))
        gg += chr(g[i])
    print(g)
    return gg

def code(txt, g):                                       #функция шифрования и дешифрования
    result_str = ""
    j = 0
    for i in range(len(txt)):
        result_str += chr(ord(txt[i]) ^ ord(g[j]))      #xor
        j += 1
        if j == gamma_len:                                      #перебираем гамму
            j = 0
    return result_str

def main():
    print("Введите 1 - если хотите зашифровать текст\nВведите 2 - если хотите расшифровать текст")
    mode = input()
    if mode == "1":
        g = gamma()
        print("Введите текст, который хотите использовать:")
        txt = input()
        output_txt = code(txt, g)
        with open("Shifr.txt", "w", encoding="utf-8") as file:
            file.write(output_txt)
            file.write("\n")
            file.write(str(g))

    elif mode == "2":
        with open("Shifr.txt", "r", encoding="utf-8") as file:
            txt = file.readline()
            g = file.readline()
        print(txt[:-1])
        output_txt = code(txt[:-1], g)
    else:
        print("Введён неверный аргумет")
        return 1
    print(output_txt, end='')

main()
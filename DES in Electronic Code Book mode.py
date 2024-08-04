import base64
from textwrap import wrap
import operator
from functools import reduce
 
KEY = '133457799BBCDFF1'  # 64 битный ключ 

'''Первая таблица перестановок ключа'''
IP_TABLE = [
 
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
    56, 48, 40, 32, 24, 16, 8, 0,
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6
 
]
 
INVERSE_PERMUTATION = [
 
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25,
    32, 0, 40, 8, 48, 16, 56, 24,
 
]
 
S_TABLE = [
 
    [
        14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
        0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
        4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
        15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13
    ],
    [
        15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
        3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
        0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
        13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9
    ],
    [
        10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
        13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
        13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
        1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12
    ],
    [
        7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
        13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
        10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
        3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14
    ],
    [
        2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
        14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
        4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
        11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3
    ],
    [
        12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
        10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
        9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
        4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13
    ],
    [
        4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
        13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
        1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
        6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12
    ],
    [
        13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
        1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
        7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
        2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
    ]
 
]
 
EXPANSION = [
 
    31, 0, 1, 2, 3, 4,
    3, 4, 5, 6, 7, 8,
    7, 8, 9, 10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31, 0
 
]
PERMUTATION = [
 
    15, 6, 19, 20, 28, 11, 27, 16,
    0, 14, 22, 25, 4, 17, 30, 9,
    1, 7, 23, 13, 31, 26, 2, 8,
    18, 12, 29, 5, 21, 10, 3, 24
 
]
 
PC1_TABLE = [
 
    56, 48, 40, 32, 24, 16, 8,
    0, 57, 49, 41, 33, 25, 17,
    9, 1, 58, 50, 42, 34, 26,
    18, 10, 2, 59, 51, 43, 35,
    62, 54, 46, 38, 30, 22, 14,
    6, 61, 53, 45, 37, 29, 21,
    13, 5, 60, 52, 44, 36, 28,
    20, 12, 4, 27, 19, 11, 3
 
]
 
PC2_TABLE = [
 
    13, 16, 10, 23, 0, 4,
    2, 27, 14, 5, 20, 9,
    22, 18, 11, 3, 25, 7,
    15, 6, 26, 19, 12, 1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31
 
]
 
ROTATES = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
 
 
def WrapSrc(string):
    """Делим исходный текст на блоки по 64 бит в 16 формате"""
    return [i.zfill(16) for i in wrap(''.join([hex(ord(i))[2:] for i in string]), 16)]
 
 
def to_bin(s):
    """Преобразуем 16 символ в двоичный формат по 4 бит на символ"""
    return ''.join([bin(int(i, 16))[2:].zfill(4) for i in s])
 
 
def permute(block, box):
    """Делаем перестановки блока в соответствии с таблицей box"""
    return ''.join([block[i] for i in box])
 
 
def XOR(arg_1, arg_2):
    return ''.join([str(int(i) ^ int(j)) for i, j in zip(arg_1, arg_2)])
 
 
def rotate_left(block, i):
    """Сдвигаем блок влево на i бит"""
    return bin(int(block, 2) << i & 0x0fffffff | int(block, 2) >> 28 - i)[2:].zfill(28)
 
 
def concatenate(args):
    return reduce(operator.iadd, args, [])
 
 
def key_gen(block_1, block_2):
    """Сдвигаем левый и правый блок в соответствии с таблицей ROTATES, после чего делаем перестановку по таблице PC2"""
    li = []
    for i in ROTATES:
        block_1 = rotate_left(block_1, i)
        block_2 = rotate_left(block_2, i)
        li.append(permute(block_1 + block_2, PC2_TABLE))
 
    return li
 
 
def f(block, key):
    """Расширяем блок с 32 до 48 бит с помощью таблицы EXPANSION. После этого для каждого 6 битного блока делаем перестановки таблицами S получая блоки по 4 бит и 32 бит на выходе"""
    final = []
 
    for j, i in enumerate(wrap(XOR(permute(block, EXPANSION), key), 6)):
        temp_box = [
            S_TABLE[j][0:16],
            S_TABLE[j][16:32],
            S_TABLE[j][32:48],
            S_TABLE[j][48:64]
        ]
        final.append(bin(temp_box[int(i[0] + i[-1], 2)]
                         [int(i[1:-1], 2)])[2:].zfill(4))
 
    return permute(''.join(final), PERMUTATION)
 
 
def des(block, key_array):
    """Делим блок на левый и правый, каждую итерацию вычисляем для правого функцию f и делим по модулю 2 от левого блока, а в левый блок переносим исходный правый"""
    left, right = block[0: len(block) // 2], block[len(block) // 2:]                    #Функция Фейстеля
    for j, i in zip(range(1, 17), key_array):
        right, left = XOR(f(right, i), left), right
    return wrap(permute(right + left, INVERSE_PERMUTATION), 8)

def Encrypt(src):
    encrypted_list = []
    for i in WrapSrc(src):
        bin_mess, bin_key = to_bin(i), to_bin(KEY) #переводим исходный текст и ключ в двоичный формат

        permuted_key, permuted_block = permute(bin_key, PC1_TABLE), permute(bin_mess, IP_TABLE) #Начальные перестановки для ключа и исходного блока

        key_list = key_gen(permuted_key[: len(permuted_key) // 2], permuted_key[len(permuted_key) // 2:]) #Делим ключ на левый и правый

        encrypted_list.append(''.join([hex(int(i, 2))[2:].zfill(2).upper() for i in des(permuted_block, key_list)]))

    return ''.join(encrypted_list)

def Decrypt(src):
    temp_li = []
    final = []
    for i in wrap(src, 16):
        bin_mess, bin_key = to_bin(i), to_bin(KEY) #переводим исходный текст и ключ в двоичный формат

        permuted_key, permuted_block = permute(bin_key, PC1_TABLE), permute(bin_mess, IP_TABLE) #Начальные перестановки для ключа и исходного блока

        key_list = key_gen(permuted_key[: len(permuted_key) // 2], permuted_key[len(permuted_key) // 2:]) #Делим ключ на левый и правый

        temp_li.append(''.join([hex(int(i, 2))[2:].zfill(2).upper() for i in des(permuted_block, reversed(key_list))]))

    return ''.join(concatenate([[chr(int(j, 16)) for j in wrap(i, 2) if int(j, 16) != 0] for i in temp_li]))
 
 
def encode_base64(data):
    encoded_bytes = base64.b64encode(data.encode("utf-8"))
    return str(encoded_bytes, "utf-8")
 
 
if __name__ == '__main__':
    src = ""
    while len(src) <= 0: #Повторяем приглашение на ввод пока не будет заполнена переменная
        print("Введите текст который нужно зашифровать: ", end='')
        src = input()

    EncryptStr = Encrypt(encode_base64(src))
    DecryptStr = str(base64.b64decode(Decrypt(EncryptStr)), "utf-8")

    print(f'Зашифрованный текст: {EncryptStr}')
    print(f'Расшифрованный текст: {DecryptStr}')
    print(f'Исходный и расшифрованный текст одинаковы: {src.lower() == DecryptStr.lower()}')
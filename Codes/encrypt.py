# coding=utf-8
import math
import random

# Initialize variables:
A = '0x67452301'
B = '0xefcdab89'
C = '0x98badcfe'
D = '0x10325476'
F = lambda x, y, z: ((x & y) | ((~x) & z))
G = lambda x, y, z: ((x & z) | (y & (~z)))
H = lambda x, y, z: (x ^ y ^ z)
I = lambda x, y, z: (y ^ (x | (~z)))
rotate_left = lambda x, n: (((x << n) | (x >> (32 - n))) & (0xffffffff))

# Constants and auxiliary functions
shi_1 = (7, 12, 17, 22) * 4
shi_2 = (5, 9, 14, 20) * 4
shi_3 = (4, 11, 16, 23) * 4
shi_4 = (6, 10, 15, 21) * 4

m_1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
m_2 = (1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12)
m_3 = (5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2)
m_4 = (0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9)


def T(i):
    result = (int(4294967296 * abs(math.sin(i)))) & 0xffffffff
    return result


def shift(shift_list):
    shift_list = [shift_list[3], shift_list[0], shift_list[1], shift_list[2]]
    return shift_list

# Encryption function
def fun(fun_list, f, m, shi):
    count = 0
    global Ti_count
    while count < 16:
        xx = int(fun_list[0], 16) + f(int(fun_list[1], 16), int(fun_list[2], 16), int(fun_list[3], 16)) + int(m[count], 16) + T(Ti_count)
        xx = xx & 0xffffffff
        ll = rotate_left(xx, shi[count])
        fun_list[0] = hex((int(fun_list[1], 16) + ll) & (0xffffffff))
        fun_list = shift(fun_list)
        count += 1
        Ti_count += 1
    return fun_list


def genM16(order, ascii_list, f_offset):
    ii = 0
    m16 = [0] * 16
    f_offset = f_offset * 64
    for i in order:
        i = i * 4
        m16[ii] = '0x' + ''.join((ascii_list[i + f_offset] + ascii_list[i + 1 + f_offset] + ascii_list[
            i + 2 + f_offset] + ascii_list[i + 3 + f_offset]).split('0x'))
        ii += 1
    for c in m16:
        ind = m16.index(c)
        m16[ind] = reverse_hex(c)
    return m16


def reverse_hex(hex_str):
    hex_str = hex_str[2:]
    hex_str_list = []
    for i in range(0, len(hex_str), 2):
        hex_str_list.append(hex_str[i:i + 2])
    hex_str_list.reverse()
    hex_str_result = '0x' + ''.join(hex_str_list)
    return hex_str_result


def show_result(f_list):
    result = ''
    f_list1 = [0] * 4
    for i in f_list:
        f_list1[f_list.index(i)] = reverse_hex(i)[2:]
        result = result + f_list1[f_list.index(i)]
    return result

def generate_random(n):
    ranStr = ''
    for i in range(n):
        ranStr += str(random.randint(0, 1))
    return ranStr

# Main loop
while True:
    abcd_list = [A, B, C, D]
    Ti_count = 1
    input_m = input('msg>>>')
    N = 23 # a random setup number because I love Lebron James
    K = -1
    while True:
        key_input = input('key>>>')
        try:
            K = int(key_input)
            if K >= 0:
                break
            else:
                print("Please enter a non-negative integer.")
        except ValueError:
            print("Please enter a number.")

    ascii_list = list((map(hex, map(ord, input_m))))
    msg_lenth = len(ascii_list) * 8
    ascii_list.append('0x80')

    while (len(ascii_list) * 8 + 64) % 512 != 0:
        ascii_list.append('0x00')
    msg_lenth_0x = hex(msg_lenth)[2:]
    msg_lenth_0x = '0x' + msg_lenth_0x.rjust(16, '0')
    msg_lenth_0x_big_order = reverse_hex(msg_lenth_0x)[2:]
    msg_lenth_0x_list = []
    for i in range(0, len(msg_lenth_0x_big_order), 2):
        msg_lenth_0x_list.append('0x' + msg_lenth_0x_big_order[i:i + 2])
    ascii_list.extend(msg_lenth_0x_list)

    for i in range(0, len(ascii_list) // 64):
        aa, bb, cc, dd = abcd_list

        order_1 = genM16(m_1, ascii_list, i)
        order_2 = genM16(m_2, ascii_list, i)
        order_3 = genM16(m_3, ascii_list, i)
        order_4 = genM16(m_4, ascii_list, i)

        abcd_list = fun(abcd_list, F, order_1, shi_1)
        abcd_list = fun(abcd_list, G, order_2, shi_2)
        abcd_list = fun(abcd_list, H, order_3, shi_3)
        abcd_list = fun(abcd_list, I, order_4, shi_4)

        output_a = hex((int(abcd_list[0], 16) + int(aa, 16)) & 0xffffffff)
        output_b = hex((int(abcd_list[1], 16) + int(bb, 16)) & 0xffffffff)
        output_c = hex((int(abcd_list[2], 16) + int(cc, 16)) & 0xffffffff)
        output_d = hex((int(abcd_list[3], 16) + int(dd, 16)) & 0xffffffff)

        abcd_list = [output_a, output_b, output_c, output_d]

        Ti_count = 1

    result = show_result(abcd_list)
    result = bin(int(result, 16))[2:]
    while len(result) < 128:
        result = '0' + result
    result = result[:K] + generate_random(N) + result[K + N:]
    print(hex(int(result, 2))[2:])
    break
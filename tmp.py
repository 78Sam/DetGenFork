# in_one = "8484d609"
# in_two = "3"

# in_one = int(in_one, 16)
# in_two = int(in_two, 16)

# res = hex(in_one >> in_two)
# print(res)

# scale = 16 ## equals to hexadecimal

# num_of_bits = 32

# print(bin(int(hex(in_one), scale))[2:].zfill(num_of_bits))
# print(bin(int(res, scale))[2:].zfill(num_of_bits))

def binary(value: int, bits: int = 32):
    if value < 0:
        value = str((1 << bits)) + str(value)
    return bin(value)[2:].zfill(bits)


in1_hex = "b1f05663"
in2_hex = "06b97b0d"
expected = "fffd8f82"
ours = "ffffffff"

print(int("d", 16))

in1_int = int(in1_hex, 16)
in2_int = int(in2_hex, 16)
int_expected = int(expected, 16)
ours = int(ours, 16)

print(binary(in1_int), in1_int)
print(binary(in2_int), in2_int)
print(binary(int_expected), int_expected)
print(binary(ours), ours)

# print(binary(-in1_int >> 1))
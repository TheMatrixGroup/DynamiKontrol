import binascii

def print_bytearray(ba):
    hex_string = str(binascii.hexlify(ba), 'ascii')
    return ' '.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))

from pypbc import Parameters, Pairing, Element, G1, G2, GT, Zr
from flask import current_app as app
import math
import os

PP_FOLDER = 'PP/'
CA_FOLDER = 'CA/'

def public_params():
    if not os.path.exists(PP_FOLDER+ "param.dat"):
        param = Parameters(qbits=4*k,rbits=k)
        params_file = open(PP_FOLDER+"param.dat", 'w')
        print(param, file = params_file)
        params_file.close()
    params_file = open(PP_FOLDER+'param.dat', 'r')
    param_string = params_file.read()
    param = Parameters(param_string = param_string) 
    params_file.close()
    pairing =  Pairing(param)
    if not os.path.exists(PP_FOLDER+'g.dat'): 
        g = Element.random(pairing, G1)
        g_file = open(PP_FOLDER+'g.dat','w')
        print(g, file = g_file)
        g_file.close()
    g_file = open(PP_FOLDER+"g.dat", "r")
    g_string = g_file.read()
    g_file.close()
    return param_string, g_string

def ca(params):
    if not os.path.exists(CA_FOLDER+ "msk.dat"):
        msk = Element.random(params["e"], Zr)
        msk_file = open(CA_FOLDER+"msk.dat", 'w')
        print(msk, file = msk_file)
        msk_file.close()
    msk_file = open(CA_FOLDER+'msk.dat', 'r')
    msk_string = msk_file.read()
    msk = Element(params['e'],Zr,value= int(msk_string,16)) 
    msk_file.close()
    if not os.path.exists(CA_FOLDER+ "p.dat"):
        p = Element(params["e"], G1, value= params["g"] ** msk)
        p_file = open(CA_FOLDER+"p.dat", 'w')
        print(p, file = p_file)
        p_file.close()
    p_file = open(CA_FOLDER+'p.dat', 'r')
    p_string = p_file.read()
    p = Element(params['e'],G1,value= p_string) 
    p_file.close()
    return msk, p

def fix_params(param_string,g_string):
    param = Parameters(param_string = param_string) 

    pairing =  Pairing(param)
    g = Element(pairing,G1, value = g_string)    

    q = int(str(param).split("\n")[1].split(" ")[1])

    def hash1(message):
        return Element.from_hash(pairing, G1, str(message))

    def hash2(element):
        return Element.from_hash(pairing, Zr, str(element))

    def hash3(message):
        return Element.from_hash(pairing, Zr, str(message))
    params = {
            'q': q,
            'e': pairing,
            'g': g,
            'H1': hash1,
            'H2': hash2,
            'H3': hash3
    }
    return params

def keyGen(params):
    pairing = params["e"]
    g = params["g"]
    private_key = Element.random(pairing, Zr)
    public_key = Element(pairing, G1, value=g**private_key)
    return private_key, public_key

def skeyGen(params, attr_list, msk, public_key_to_encrypt):
    attr_string = "".join(attr_list)
    Q = params["H1"](attr_string)
    ak = Element(params["e"], G1, value=Q ** msk)
    int_val = key_byte_to_int(str(ak).encode())
    block_size = len(str(int(params['q'])))-1
    ak_enc, len_msg = elgamal_encrypt_block(int_val, params['g'], params['e'], public_key_to_encrypt, params['q'], block_size)
    return ak_enc, len_msg

def key_byte_to_int(sym_key):
    new_key = ''
    for c in sym_key.decode():
        new_key += str(ord(c)).zfill(3)
    return int(new_key)

def key_int_to_byte(key):

    l = len(str(key))
    # print(f"L = {l}")
    x = math.ceil(l/3) * 3
    # print(f"X = {x}")
    key = str(key).zfill(x)

    new_key = ''
    for i in range(0, x, 3):
        new_key += chr(int(key[i:i+3]))
        
    return new_key.encode()

def elgamal_encrypt(msg, g, pairing, public_key, q):
    # Choose random k
    k = Element.random(pairing, Zr)
    # Compute C1 = g^k
    C1 = Element(pairing, G1, value=g**k)
    # Compute C2 = msg + h(k*publci_key) mod q
    # print(f"Pairing: {pairing}")


    kerpk = Element(pairing, G1, value=public_key**k)
    hash_value = Element.from_hash(pairing, Zr, str(kerpk))
    # print(int(hash_value))
    C2 = ( msg + int(hash_value) ) % q
    return C1, C2

def elgamal_decrypt(C1, C2, pairing, private_key, g, q):
    R = Element(pairing, G1, value=C1**private_key)
    hash_value = Element.from_hash(pairing, Zr, str(R))
    message = (C2 - int(hash_value)) % q
    # print(message)
    return message

def elgamal_encrypt_block(msg, g, pairing, public_key, q, block_size = 40):
    # Assume that msg is a long integer
    str_msg = str(msg)
    len_msg = len(str_msg)
    iters = math.ceil(len_msg / block_size)
    # print("Iterations: ", iters)
    # print("Total length of data: ", len_msg)
    encrypted_data = []
    for i in range(iters):
        block_data = str_msg[i*block_size:(i+1)*block_size]
        # print(f"block_data {i}: {block_data}")
        block_int = int(block_data)
        encryption = elgamal_encrypt(block_int, g, pairing, public_key, q)
        encrypted_data.append(encryption)
    return encrypted_data, len_msg

def elgamal_decrypt_block(encrypted_data, g, pairing, private_key, q, len_msg ,block_size = 40):
    decrypted_data = []
    for i in encrypted_data:
        # print(f"I = {i}")
        decryption = elgamal_decrypt(i[0], i[1], pairing, private_key, g, q)
        # print(f"decryption : {decryption}")
        decrypted_data.append(decryption)
    # Combine to single int-string
    str_msg = ""
    iters = math.ceil(len_msg / block_size)
    for i in range(iters):
        if i != iters -1:
            block_data = str(decrypted_data[i]).zfill(block_size)
            str_msg += block_data
        else:
            # print("Here")
            block_data = str(decrypted_data[i]).zfill(len_msg % block_size)
            str_msg += block_data
    # print("Reconstructed length: ", len(str_msg))
    return int(str_msg)

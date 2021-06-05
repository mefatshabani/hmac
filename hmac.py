#!/usr/bin/env python3

import codecs, hashlib, sys
from pyasn1.codec.der import decoder
sys.path = sys.path[1:] # don't remove! otherwise the library import below will try to import your hmac.py
import hmac



OID_MD5 = (1,2,840,113549,2,5)
OID_SHA1 = (1,3,14,3,2,26)
OID_SHA256 = (2,16,840,1,101,3,4,2,1)


#==== ASN1 encoder start ====

def nb(i):
    # helper function, transforms i:int into hexarray
    accum = []
    while i:
       accum.insert(0, i & 255)
       i >>= 8    
    return accum

def bitstr_to_int(bitstring):
    i = 0
    for bit in bitstring:
        i <<= 1
        if bit == '1':
            i|= 1
    return i
       
def asn1_len(value_bytes):
    # helper function - should be used in other functions to calculate length octet(s)
    # value_bytes - bytes containing TLV value byte(s)
    # returns length (L) byte(s) for TLV
    L = len(value_bytes)
    if L < 128:
         return bytes([L])
    else:
        L_bitstring = nb(L)
        L_bitstring.insert(0, len(L_bitstring) | 128)
        return bytes(L_bitstring)

def asn1_null():
    # returns DER encoding of NULL
    return bytes([0x05]) + b'\x00'

def asn1_octetstring(octets):
    # octets - arbitrary byte string (e.g., b"abc\x01")
    # returns DER encoding of OCTETSTRING    
    return bytes([0x04]) + asn1_len(octets) + octets

def asn1_objectidentifier(oid):
    # oid - list of integers representing OID (e.g., [1,2,840,123123])
    # returns DER encoding of OBJECTIDENTIFIER    
    first_byte_int = 40*oid[0] + oid[1]
    first_byte_hex_representation = nb(first_byte_int)
    encoded_hex_representation = []
    for i in oid[2:][::-1]:
        encoded_hex_representation.insert(0, i & 127)
        while i > 127:
            i >>= 7
            encoded_hex_representation.insert(0, 128 | (i & 127))
    encoded_hex_representation = first_byte_hex_representation + \
                                 encoded_hex_representation       
    return bytes([0x06]) + asn1_len(encoded_hex_representation) + \
                           bytes(encoded_hex_representation)

def asn1_sequence(der):
    # der - DER bytes to encapsulate into sequence
    # returns DER encoding of SEQUENCE    
    return bytes([0x30]) + asn1_len(der) + der

def asn1_digest_info(algo_oid, octets_text):
    return asn1_sequence(asn1_sequence(asn1_objectidentifier(algo_oid) + \
                         asn1_null()) + asn1_octetstring(octets_text))

#==== ASN1 encoder end ====


def read_chunks_gen(file_handle, chunk_size=512):
    """Generator for reading in blocks of desired bytes length"""
    while True:
        data = file_handle.read(chunk_size)
        if not data:
            break
        yield data


def mac_different_algos(filename, hash_f):
    key = input("[?] Enter key: ").encode()
    hmac_object = hmac.new(key, digestmod=hash_f)
    with open(filename, 'rb', buffering=512) as f:
        # The use of buffering allows to avoid reading from raw stream,
        # what can have high latency
        for chunk in read_chunks_gen(f):
            hmac_object.update(chunk)
    return hmac_object.digest()


def mac(filename):
        hmac_256 = mac_different_algos(filename, hashlib.sha256)
        print("[+] Calculated HMAC-SHA256:", hmac_256.hex())
        print("[+] Writing HMAC DigestInfo to", filename+".hmac")
        # Encode as ASN1_digest_info structure
        hmac_as_asn1_digest_info = asn1_digest_info(OID_SHA256, hmac_256)
        with open(filename+".hmac", 'wb') as f:
            f.write(hmac_as_asn1_digest_info)     

        
def verify(filename):
    print("[+] Reading HMAC DigestInfo from", filename+".hmac")
    # I read which hash function should I use
    der = open(filename+".hmac", 'rb').read()
    oid, known_digest = decoder.decode(der)[0][0][0], decoder.decode(der)[0][1]
    if oid == OID_MD5:
        hash_name = "MD5"
        hash_func = hashlib.md5
    elif oid == OID_SHA1:
        hash_name = "SHA1"
        hash_func = hashlib.sha1
    elif oid == OID_SHA256:
        hash_name = "SHA256"
        hash_func = hashlib.sha256
    else:
        print("[-] Hash Function not recognised, aborting!!!")
        raise SystemExit()
    # print out the digest
    print("[+] HMAC-" + hash_name + " digest:", known_digest.prettyPrint()[2:])
    # ask for the key and calculate the digest    
    digest_calculated = mac_different_algos(filename, hash_func)        
    # print out the calculated HMAC-X digest
    print("[+] Calculated HMAC-" + hash_name + ":", digest_calculated.hex())
    if digest_calculated != known_digest:
        print("[-] Wrong key or message has been manipulated!")
    else:
        print("[+] HMAC verification successful!")


def usage():
    print("Usage:")
    print("-mac <filename>")
    print("-verify <filename>")
    sys.exit(1)


if len(sys.argv) != 3:
    usage()
elif sys.argv[1] == '-mac':
    mac(sys.argv[2])
elif sys.argv[1] == '-verify':
    verify(sys.argv[2])
else:
    usage()


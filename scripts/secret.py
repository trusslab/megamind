import os
from Commu import Commu
import json
#For Asymetric public/private key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key

#For symetric AES
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC,OFB,CFB
from hashlib import sha3_256
from os import urandom
from cryptography.hazmat.backends import default_backend

import hmac
backend = default_backend()


import base64


class AES_Cipher:
  def __init__(self,key):
    self.key = key

  def encrypt(self,plain_text):
    initialization_vector = urandom(16)
    cipher = Cipher(AES(self.key),OFB(initialization_vector),backend)
    encryption_engine = cipher.encryptor()
    return initialization_vector + encryption_engine.update(plain_text.encode("utf-8")) + encryption_engine.finalize()

  def decrypt(self,cipher_text):
    initialization_vector = cipher_text[:16]
    cipher = Cipher(AES(self.key),OFB(initialization_vector),backend)
    decryption_engine = cipher.decryptor()
    return (decryption_engine.update(cipher_text[16:]) + decryption_engine.finalize()).decode("utf-8")

AES_KEY = sha3_256(urandom(32)).digest()
AES_engine = AES_Cipher(AES_KEY)
print('\n\n\n\n\n\n\n\n\n\n secret chat \n\n\n\n\n')
pubkey_pem = b"-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDlWUe72WqerBFdIIpFroL26E7i\n/P/qSeTN+5spVpHXmikNJ+EJtiY8vcfQ8mzSFlzrOQWz2geawjeAGy+6mBiNjr8i\nizlagasYtGGC+YuIQsiHs8C8yn2pQRE67gsXL32f66m5AcGZ2NxZFe6lAHa15BxV\nc5yVonZPcSquis7yxQIDAQAB\n-----END PUBLIC KEY-----\n"

plaintextMessage = AES_KEY
alicePubKey = load_pem_public_key(pubkey_pem,default_backend())
ciphertext = alicePubKey.encrypt(
    plaintextMessage,
    padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
  )
)
#print('cipher text', ciphertext)
s1 = base64.b32encode(ciphertext)
#print(s1)
str1 = s1.decode()
s1 = (str1.replace('=' , '')).lower()
#print(s1)


def pr(*args , **kwargs):
	print( '**** ' + " ".join(map(str,args)) + " ****" , **kwargs)

def encrypt_request(req):
        #print('enc req KEY IS: ', AES_KEY)
        cypher = AES_engine.encrypt(req)
        digest = hmac.new(AES_KEY, cypher, sha3_256).digest()
        #print(digest)
        coded_digest = base64.b32encode(digest)
        coded_cypher = base64.b32encode(cypher)
#       print('[1]', coded_cypher)
        coded_cypher = coded_cypher.decode().replace('=','').lower()
        coded_digest = coded_digest.decode().replace('=','').lower()
        #print(coded_digest)
#       print('[2]',coded_cypher)
        return coded_cypher + '8' + coded_digest


def decrypt_response(resp):
        #print('dec resp KEY IS: ' ,AES_KEY)
        index = resp.find('8')
        new_resp = resp[0:index]
        hash_resp = resp[index+1:]
        resp = new_resp
        old_resp = resp
        l = len(resp)
        r = l % 8
        if( r != 0):
                for i in range(0,8-r):
                        resp = resp + '='
        l = len(hash_resp)
        r = l % 8
        if( r != 0):
                for i in range(0,8-r):
                        hash_resp = hash_resp + '='
        hash_text = hash_resp.upper()

        try:
                cypher_text = resp.upper()
        #       print(cypher_text)
                cypher_text_bytes = base64.b32decode(cypher_text)
        #       print(cypher_text_bytes)
                digest = hmac.new(AES_KEY, cypher_text_bytes, sha3_256).digest()
                coded_digest = base64.b32encode(digest)
                coded_digest = coded_digest.decode()
                #print( 'coded_digest=  ',coded_digest, ' len= ',len(coded_digest))
                #print( 'hash_text   =  ',hash_text   , ' len= ',len(hash_text))
                if(coded_digest != hash_text):
                        print('[1]')
                        return 'HMAC does not match'
                plain_text = AES_engine.decrypt(cypher_text_bytes)
        except:
                plain_text = old_resp
        return plain_text


pr("secret chat extention")
comm = Commu()
#comm.update_ready(False)
comm.init_pipes()
while True:
	#comm.wait_for_new_data()
	#session = comm.read_data()
	session = comm.read_data_blocking()
	#pr(session)
	item = comm.get_item_of_interest(session)
	
	#print(item)
	if (comm.is_request(session)):	
		if(comm.get_num_of_requests(session) == 1):
			pass
		else:
			if (comm.get_num_of_requests(session) == 2):
				item = "key is " + s1
			else:
				item = "search " +  encrypt_request(item)
				#print('item = ' , item)
		comm.write_response(item)
		#comm.update_ready(True)
	else:
		if(comm.get_num_of_responses(session) > 2):
			if 'Goodbye' in item:
				item = item
			else:
				item =  decrypt_response(item)
			#print('item = ' , item)
		comm.write_response(item)
		#comm.update_ready(True)
		

	

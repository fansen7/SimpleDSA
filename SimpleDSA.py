### DSA ###
'''
	p = 67
	q = 11
	g = 59
	x = 5
	M = "myDSAbooo"
	y = 62
	r, s = sign(g,p,q,x,M)
	print(r,s)
	print(verify(g, p, q, y, M, r, s))
'''

import random
import hashlib

#Square and Mutiply
# x^H mod n
def sqr_mul(x, H, n): 
	H = bin(int(H)).split('b')[1]
	y = 1
	for c in H:
		y = (y ** 2) % n
		if c == '1':
			y = (y * x) % n 
	return y

#Inverse element
def inv_ele(e, r):
    d = 2
    while (e * d)% r != 1 :
        d += 1
    return d

#Inverse element(extended euclidean algorithm)
def inv_ele_ext_euclid(a, b):
     if b == 0:
         return 1, 0, a
     else:
         x, y, q = inv_ele_ext_euclid(b, a % b)
         x, y = y, (x - (a // b) * y)
         return x, y, q

#Big Number Generator
def prime_gen(bits): 
	prime = '1'
	for _ in range(bits - 2):
		prime += str(random.randint(0,1))
	prime += '1'

	return int(prime, 2)

#Prime Number Test
def Miller_Rabin(N): 
	if N == 1 or N == 2 or N == 3:
		#print('Prime')
		return 1	# is Prime
	elif N <= 0 :
		return 0
	k = 0
	m = N-1
	while m % 2 == 0 :
		m >>= 1
		k += 1
	a = random.randint(2,N - 2)
	b = sqr_mul(a , m , N)
	if b != 1 and b != (N - 1):
		i = 1
		while i < k and b != (N -1):
			b = (b ** 2) % N
			if b == 1 :
				return 0 # not Prime
			i += 1
		if b !=(N - 1):
			return 0	 # not Prime
	return 1 # is Prime

#signature
def sign(g, p, q, x, M): 
	k = random.randint(0, q)
	r = sqr_mul(g, k, p) % q
	sha = hashlib.sha1()
	sha.update(M.encode('UTF-8'))
	H_m = sha.hexdigest()
	H_m = int(H_m, 16)
	k_inv, _, _ = inv_ele_ext_euclid(k, q)
	while k_inv < 0 :
		k_inv += q
	s = ((H_m + x * r) * k_inv) % q
	return r, s

#verification
def verify(g, p, q, y, M, r, s):
	s_inv, _, _ = inv_ele_ext_euclid(s, q)
	while s_inv < 0:
		s_inv += q
	w  = s_inv % q

	sha = hashlib.sha1()
	sha.update(M.encode('UTF-8'))
	H_m = sha.hexdigest()
	H_m = int(H_m, 16)
	
	u1 = (H_m * w) % q
	u2 = (r * w) % q
	v = (((sqr_mul(g, u1, p) * sqr_mul(y, u2, p)) % p) % q)
	print('v = ' + str(v))
	print('r = ' + str(r))
	if v == r:
		return True
	else :
		return False

#main
if __name__ == '__main__':
	M = "myDSAbooo"
	print('*****************************************')
	print('*                  DSA                  *')
	print('*****************************************')
	
	M = input('Please Input Your Messege:')
	print('Messege:' + M)
	print("Key Generation:")
	
	flag = 0
	k = prime_gen(864)
	p = prime_gen(1024)
	q = prime_gen(160)

	#Generate two prime number p&q and make sure  (p - 1) mod q == 0
	while flag == 0:
		i = 0
		while Miller_Rabin(q) == 0:
			q = prime_gen(160)
		while i < 100:
			k = random.randint(2 ** 863, 2 ** 864)
			p = k * q + 1
			if Miller_Rabin(p) == 1:
				flag = 1
				break
			i += 1

	#Generate g
	g = 1
	while True:
		h = random.randint(2, p - 2)
		g = sqr_mul(h, int((p - 1) // q), p)
		if sqr_mul(g, q, p) == 1 and g != 1:
			break

	print('p = ' + str(p))
	print('q = ' + str(q))
	print('g = ' + str(g))
	print('')
	
	#Generate public key and private key
	pri_key = random.randint(1, q - 1)  #x
	pub_key = sqr_mul(g, pri_key, p)	#y
	print("Private Key:" + str(pri_key))
	print("Public Key:" + str(pub_key))
	print("") #print 換行
	
	#Generate signature
	print("Signature generation:")
	r,s = sign(g, p, q, pri_key,M)
	print('r = ' + str(r))
	print('s = ' + str(s))
	
	#Verification
	print('Signature verification:')
	r_ = int(input("Input r of your Signature:"))
	s_ = int(input("Input s of your Signature:"))
	if verify(g, p, q, pub_key, M, r_, s_) == True:
		print("Signature is Vaild.")
	else:
		print('Signature is Invalid.')
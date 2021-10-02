import pickle
import alg
from alg import conv_pol as co

class req:
        def uni(msg): # converts message into list of ord of all its characters and then to a nested list of sublist length 16
              L = []
              for i in msg:
                   L.append(ord(i)) # adds ascii value
              while len(L)%16!= 0  or len(L) == 0: # converts no of elements to a multiple of 16 by adding space
                  L.append(32)
              p = 0
              L1 = []
              while p < len(L):
                  L1.append(L[p:p+16])
                  p+=16
              return L1
        
        def bin8(j): # 8 bit converter
                x = bin(j)
                if len(x) < 10:
                        x = "0b" + (10-len(x))*"0" + x[2:]
                return x

        def xor(b1,b2): # xor of 2 8 bit binary numbers returning an 8 bit binary 
                 a = b1[2:]
                 b = b2[2:]
                 c = ""
                 for i in range(8):
                          c+= str((int(a[i]) + int(b[i]))%2)
                 c = "0b" + c
                 return c
    
        def xorm(L): # xor of multiple values
                if len(L) == 2:
                     return req.xor(L[0],L[1])
                elif len(L) > 2:
                     return req.xorm([req.xor(L[0],L[1])]+L[2:]) #recursion

        def dotp(a,b): #dot product of a and b returned
                p = alg.pol_mul(co(a),co(b)) # convert a and b to polynomials and multiply them
                q = {8:1,4:1,3:1,1:1,0:1} # standard polynomial to reduce polynomials to degree 8 and convert a binary number to byte length
                x = (alg.pol_div(p,q))[1] # find remainder of polynomials p by q 
                y = alg.inv_pol(x) #convert x from polynomial back to binary form
                return y 
                
        def colm(c1,c2): # matrix multiplication 1 row * 1 column
                r = []
                for i in range(4):
                        r.append(req.bin8(int(req.dotp(c1[i],c2[i]),2))) # multiply -> dot product
                a = req.xorm(r) # add -> xor
                return int(a,2)
                       
def sbox(b): # sbox converter
    f = open("sbox.dat","rb")
    l = pickle.load(f)
    f.close()
    return l[b]

def sbox_inv(b): #sbox inverter
    f = open("sbox_inv.dat","rb")
    l = pickle.load(f)
    f.close()
    return l[b]

def rows(L): #converts 4*4 matrix to nested list of rows
	r = []
	for i in range(4):
		r.append([L[i],L[i+4],L[i+8],L[i+12]])
	return r

def cols(L):  #converts 4*4 matrix to nested list of columns
	c = []
	for i in range(0,13,4):
		c.append([L[i],L[i+1],L[i+2],L[i+3]])
	return c

def shift_rows(L): #shift rows algorithm 
        x = rows(L).copy()
        x[1] = x[1][1:] + x[1][0:1]
        x[2] = x[2][2:] + x[2][0:2]
        x[3] = x[3][3:4] + x[3][0:3]
        y = []
        for i in range(4):  
              y += x[i]
        y = rows(y) #applying rows again to get the original order
        x = []
        for i in range(4):
             x += y[i]
        return x
 
def inv_shift_rows(L): #inverse shift rows algorithm
        x = rows(L).copy()
        x[1] = x[1][3:4] + x[1][0:3]
        x[2] = x[2][2:] + x[2][0:2]
        x[3] = x[3][1:] + x[3][0:1]
        y = []
        for i in range(4):
              y += x[i]
        y = rows(y)
        x = []
        for i in range(4):
             x += y[i]
        return x

def mix_columns(L): 
        a = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
        c = cols(L)
        o = []
        for i in c:
                for j in a:
                        o.append(req.colm(i,j)) #multiply ith row of a with jth column of a
        return o

def inv_mix_columns(L): #inverse mix columns algorithm
        a = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]
        c = cols(L)
        o = []
        for i in c:
                for j in a:
                        o.append(req.colm(i,j))
        return o

def key_gen(key): # function to generate 10 roundkeys given key 0
        keylist = {}
        rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
        keylist[0] = key
        for i in range(1,11):
                l = [req.bin8(rcon[i-1]),req.bin8(0),req.bin8(0),req.bin8(0)] # ith round rcon list
                a = cols(keylist[i-1]) #previous key
                for j in range(4):
                        a[j] = a[j][3:4] + a[j][0:3] #rotword
                b = []
                for j in a:
                        b+=j
                for j in range(16):
                        b[j] = req.bin8(sbox(b[j])) #substitution 
                c = cols(b)
                m = (keylist[i-1]).copy()
                for j in range(16):
                         m[j] = req.bin8(j)
                m = cols(m) # storing columns of binary form of previous roundkey in a variable 
                for j in range(4):
                        a1 = m[j]
                        a2 = c[j]
                        for n in range(4):   # key generation function 
                                a1[n] = int(req.xorm([a1[n],a2[n],l[n]]),2) # since we're passing by reference, m also gets updated
                k = []    
                for j in m:
                       k += j
                keylist[i] = k
        return keylist

def add_round_key(L,key): # adding (xor) round key to given list
        c = []
        for i in range(16):
                c.append(int(req.xor(req.bin8(L[i]),req.bin8(key[i])),2)) 
        return c

def encrypt(plaintext,key0):
        L = req.uni(plaintext)
        L1 = req.uni(key0)
        key_ord = []
        if len(key0) > 16: # if key len is greater than 16 we reduce it to 16 by xor-ing corresponding list elements of the uni list
            for i in range(16):
                   L2 = []
                   for j in L1:
                           L2.append(req.bin8(j[i]))
                   key_ord.append(int(req.xorm(L2),2))
        else:
                key_ord = L1[0]
        rkeys = key_gen(key_ord) # generating round keys
        n = len(L)
        s = L.copy()
        for j in range(9):  # 9 rounds
                for k in range(n):
                        s[k] = add_round_key(s[k],rkeys[j]) # add round key j
                        for m in range(16):
                                s[k][m] = sbox(s[k][m]) # substitution layer
                        s[k] = shift_rows(s[k]) #permutation layer (i)
                        s[k] = mix_columns(s[k]) #permutation layer (ii)
        for k in range(n): # last round no mix columns
                        s[k] = add_round_key(s[k],rkeys[9])
                        for m in range(16):
                                s[k][m] = sbox(s[k][m])
                        s[k] = shift_rows(s[k])
                        s[k] = add_round_key(s[k],rkeys[10])
        t = []
        ciphertext = ''
        for i in s:
                t+= i
        for i in t:
                ciphertext += chr(i) # converting back into characters
        return ciphertext
        
        

def decrypt(ciphertext,key0): #similarly coded as encrypt function
        L = req.uni(ciphertext)
        L1 = req.uni(key0)
        key_ord = []
        if len(key0) > 16:
            for i in range(16):
                   L2 = []
                   for j in L1:
                           L2.append(req.bin8(j[i]))
                   key_ord.append(int(req.xorm(L2),2))
        else:
                key_ord = L1[0]
        rkeys = key_gen(key_ord)
        n = len(L)
        s = L.copy()
        # Reversing encryption step by step
        for k in range(n): # 1st round no inv mix columns
                        s[k] = add_round_key(s[k],rkeys[10])  
                        s[k] = inv_shift_rows(s[k])
                        for m in range(16):
                                s[k][m] = sbox_inv(s[k][m])
                        s[k] = add_round_key(s[k],rkeys[9])
        for j in range(8,-1,-1):# final 9 rounds
                for k in range(n):
                        s[k] = inv_mix_columns(s[k])
                        s[k] = inv_shift_rows(s[k])
                        for m in range(16):
                                s[k][m] = sbox_inv(s[k][m])
                        s[k] = add_round_key(s[k],rkeys[j])
        t = []
        plaintext = ''
        for i in s:
                t+= i
        for i in t:
               plaintext += chr(i)
        return plaintext




                        
        
        

        
        










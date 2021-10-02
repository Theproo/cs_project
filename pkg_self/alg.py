def conv_pol(i):
    j = (bin(i))[2:]
    j = (list(j))[::-1]
    d = {}
    for k in range(len(j)):
        d[k] = int(j[k])
    return d
            
def clr(d):
    d1 = {0:0}
    if len(d) == 0:
        return d1
    for i in d:
        if d[i] != 0:
            d1[i] = d[i]
    return d1

def pol_add(d1,d2):
    d = {}
    for i in d1:
        d[i] = 0
    for j in d2:
        d[j] = 0
    for k in d:
        d[k] = d1.get(k,0) + d2.get(k,0)
    return clr(d)

def pol_smul(d,k):
	d1 = {}
	for i in d:
	    d1[i] = (d[i])*k
	return clr(d1)

def pol_mul(d1,d2):
	d = {}
	for i in d1:
	    for j in d2:
	        if i+j not in d.keys():
	              d[i+j] = 0
	        d[i+j] += d1[i]*d2[j]
	return (clr(d))

def deg(d):
             s = list(dict.keys(clr(d)))
             return max(s)

def pol_div(d1,d2):
    r = d1.copy()
    q = {0:0}
    while deg(r) >= deg(d2):
        a = deg(r) - deg(d2)
        c = (r[deg(r)])/(d2[deg(d2)])
        q = pol_add(q,{a:c})
        x = pol_mul(q,d2)
        y = pol_smul(x,-1)
        r = pol_add(d1,y)
    return (clr(q),clr(r))

def inv_pol(d):
    s = ''
    d1 = {}
    for i in range(deg(d)+1):
        d1[i] = d.get(i,0)
    for j in d1:
        s += str(int((d1[j])%2))
    s = "0b"+s[::-1]
    return s





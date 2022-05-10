from Customer import locationfunctions
d = 256

def search(pat, txt, q):
    M = len(pat)
    N = len(txt)
    if M > N:
        return False
    i = 0
    j = 0
    p = 0    
    t = 0   
    h = 1
    for i in range(M-1):
        h = (h*d)%q
    for i in range(M):
        p = (d*p + ord(pat[i]))%q
        t = (d*t + ord(txt[i]))%q
    for i in range(N-M+1):
        if p==t:
            for j in range(M):
                if txt[i+j] != pat[j]:
                    break
                else: 
                    j+=1
            if j==M:
                return True
        if i < N-M:
            t = (d*(t-ord(txt[i])*h) + ord(txt[i+M]))%q
            if t < 0:
                t = t+q
    return False
        


def SearchFind(pattern, lat, long):
    d = locationfunctions.shoploc(lat, long)
    q = 101
    data = []
    for oneshop in d:
        if search(pattern, oneshop['agent_shop_name'].lower(), q) :
            data.append(oneshop)
    return data
    
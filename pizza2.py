def solv(nos, smax, top,res=[],pi=[],n=0,d=-1):
    s = sum(res)
    if s <= smax and s > n:
        n = s
        yield [s , pi]
    if s >= smax:
        return  
    for i in range(len(nos)):
        n = nos[i]
        d+=1
        rm = nos[i+1:]
        yield from solv(rm, smax,top, res + [n],pi+[d],n,d) 


if __name__ == "__main__":
    k , t = list(map(int,input().split()))
    lis = list(map(int,input().split()))
    p = max(list(solv(lis,k,lis)),key=lambda x:x[0])
    print(len(p[1]))
    print(" ".join(map(str,p[1])))

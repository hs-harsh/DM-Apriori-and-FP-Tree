import timeit
import pandas as pd

def store(C):
  d={}
  for t in C:
    if t not in d:
      d[t]=0
  return d


def findwithmin(t,d1):
    temp=t.split(" ")
    imin=10000000000
    k="-1"
    for i in temp:
        if imin>d1[i]:
            imin=d1[i]
            k=i
    return k


def update(data,d,C,s,k,d1,d2):
  for trans in C:
    k=findwithmin(trans,d1)                                       
    lis=d2[k]
    for i in lis:
      if set(trans.split(" ")).issubset(set(data[i].split(" "))):
        if d[trans]<s:                                            
            d[trans]+=1
        else:
            break


def subsets(t):
  l=[]
  l=set(l)
  tempt=t
  tempt=tempt.split(" ")
  for i in tempt:
    temp=[]
    for j in tempt:
      if i!=j:
        temp=temp+[j]
    l.add(" ".join(temp))
  return l



def candgen(L):
  alpha=L[0]
  k=len(alpha.split(" "))
  C=[]
  n=len(L)
  if k==1:
    for i in range(n):
      for j in range(i+1,n):
        if L[i]!=L[j]:
          C.append(str(min(int(L[i]),int(L[j])))+" "+str(max(int(L[i]),int(L[j]))))
  else:
    for i in range(n):
      for j in range(i+1,n):
        p=L[i].split(" ")
        q=L[j].split(" ")
        temp=True
        for ind in range(k-1):
          temp=temp and p[ind]==q[ind]
        if temp==True and p[k-1]!=q[k-1]:
          C.append(" ".join((p[:k-1]+[str(min(int(p[k-1]),int(q[k-1])))]+[str(max(int(p[k-1]),int(q[k-1])))])))

  d=store(L)
  for t in C:
    l=subsets(t)
    for i in l:
      if i not in d:
        C.remove(t)
        break
  return C


def candwithsup(C,d,s):
  L=[]
  for t in C:
    if t in d and d[t]>=s:
      L.append(t)
  return L


file=open("forests.txt")
data=[]
for line in file:
  line=line.strip().split(" ")
  if line[len(line)-1]==" ":
    line=line[:len(line)-1]
  data.append(" ".join(line))

def Apriori(data,s):
  Fqsets=[]
  count=len(data)
  d1={}
  d2={}
  L1=[]
  for i in range(len(data)):
    tempt=data[i]
    tempt=tempt.split(" ")
    for j in range(len(tempt)):
      if tempt[j] in d1:
        d1[tempt[j]]+=1
      else:
        d1[tempt[j]]=1
      if tempt[j] in d2:
        d2[tempt[j]].append(i)
      else:
        d2[tempt[j]]=[]
        d2[tempt[j]].append(i)
    
  C1=list(d1.keys())
  for k in C1:
    if d1[k]>=s*count:
      L1.append(k)
  currL=L1
  k=1
  for i  in range(len(data)):                                        
    tempdata=data[i].split(" ")
    for t in tempdata:
        if t not in L1:
            tempdata.remove(t)
    data[i]=" ".join(tempdata)
  while(len(currL)!=0):
    # print("K : "+str(k))
    Fqsets=Fqsets+currL
    C=candgen(currL)
#     C=list(set(C))
    if len(C)==0:
      break
    d=store(C)
    update(data,d,C,s*count,k+1,d1,d2)
    newL=candwithsup(C,d,s*count)
#     newL=list(set(newL))
    currL=newL 
    k+=1
  return Fqsets


start_time = timeit.default_timer()
l=Apriori(data,0.6)
elapsed = timeit.default_timer() - start_time
print(elapsed)
print(len(l))



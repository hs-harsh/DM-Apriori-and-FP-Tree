import timeit
import pandas as pd

def store(C):
  hashtree={}
  k=len(C[0].split(" "))
  for t in C:
    curr=hashtree
    tempt=t
    t=list(map(int,t.split(" ")))
    for i in range(0,k-1):
      if t[i]%m in curr:
        curr=curr[t[i]%m]
      else:
        curr[t[i]%m]={}
        curr=curr[t[i]%m]

    if t[k-1]%m in curr:
      curr[t[k-1]%m]['val'].append([tempt,0])
    else:
      curr[t[k-1]%m]={}
      curr[t[k-1]%m]['val']=[]
      curr[t[k-1]%m]['val'].append([tempt,0])
    t=tempt
  return hashtree


def search(tree,t):
  curr=tree
  tempt=t
  t=list(map(int,t.split(" ")))
  k=len(t)
  for i in range(0, k):
    if t[i]%m in curr:
      curr = curr[t[i]%m]
    else: 
      t=tempt
      return False
  ans=False
  for i in curr['val']:
    if i[0]==tempt:
      ans=True
      t=tempt
      break
  return ans


def update(data,tree,C,k):
  for trans in C:
    temptrans=trans
    count=0
    for t in data:
      if set(trans.split(" ")).issubset(set(t.split(" "))):
        count+=1
    trans=list(map(int,trans.split(" ")))
    curr=tree
    for i in range(0, k):
      if trans[i]%m in curr:
        curr = curr[trans[i]%m]
      else: 
        break
    if 'val' in curr:
      for val in curr['val']:
        if val[0]==temptrans:
          val[1]+=count

def subsets(t):
  l=[]
  tempt=t
  tempt=tempt.split(" ")
  for i in tempt:
    temp=[]
    for j in tempt:
      if i!=j:
        temp=temp+[j]
    l.append(" ".join(temp))
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


  tree=store(L)
  for t in C:
    l=subsets(t)
    for i in l:
      if search(tree,i)==False:
        C.remove(t)
        break
  return C


def candwithsup(C,hashtree,s):
  L=[]
  curr=hashtree
  for t in C:
    curr=hashtree
    tempt=t
    t=t.split(" ")
    t=list(map(int,t))
    n=len(t)
    for i in range(n):
      curr=curr[t[i]%m]
    for i in curr['val']:
      if i[1]>=s:
        L.append(i[0])
    t=tempt
  return L

file=open("forests.txt")
data=[]
for line in file:
  line=line.strip().split(" ")
  if line[len(line)-1]==" ":
    line=line[:len(line)-1]
  data.append(" ".join(line))
m=3


def Apriori(data,s):
  Fqsets=[]
  count=len(data)
  d={}
  L1=[]
  for t in data:
    tempt=t
    t=list(map(int,t.split(" ")))
    for i in range(len(t)):
      if str(t[i]) in d:
        d[str(t[i])]+=1
      else:
        d[str(t[i])]=1
    t=tempt
  C1=list(d.keys())
  for k in C1:
    if d[k]>=s*count:
      L1.append(k)
  currL=L1
  k=1
  while(len(currL)!=0):
    # print("K : "+str(k))
    Fqsets=Fqsets+currL
    C=candgen(currL)
    C=list(set(C))
    if len(C)==0:
      break
    tree=store(C)
    update(data,tree,C,k+1)
    newL=candwithsup(C,tree,s*count)
    newL=list(set(newL))
    currL=newL 
    k+=1
#   print(Fqsets)
  return Fqsets


start_time = timeit.default_timer()
l=Apriori(data,0.6)
print(len(l))
elapsed = timeit.default_timer() - start_time
print(elapsed)


# arr is list of tuple of tuple [(a,b,c)]
# a is difficulty
# b is number of times asked (score)
# c is id
from sortedcontainers import SortedList 
import random

diff_level=5 #difficulty levels
def choosequestions(arr, avg, n):
    sum=int(avg*n)
    mp=[SortedList() for _ in range(diff_level+1)]
    for x in arr:
        mp[x[0]].add((x[1],x[2]))
 
    ans=0
    fina=[SortedList() for _ in range(diff_level+1)]
    findic=[SortedList() for _ in range(diff_level+1)]
    
    fina=[SortedList() for _ in range(diff_level+1)]
    for x in arr:
        fina[x[0]].add((x[1],x[2]))
    c=0
    for i in range (n):
        for j in range (1,diff_level+1):
            if(len(mp[j])>i):
                fina[j].discard((mp[j][i][0],mp[j][i][1]))
                findic[j].add((mp[j][i][0],mp[j][i][1]))
                ans+=j
                c+=1
            if(c==n):
                break
        if(c==n):
            break
    diff=ans-sum
  
    if(diff<0):
        x=random.choice([1,2,3,4])
        for i in range(x,diff_level+1):
            if(len(findic[i])!=0):
                for j in range(i+1,diff_level+1):
                    if (len(fina[j])!=0 and len(findic[i])!=0):
                        fina[i].add(findic[i][len(findic[i])-1])
                        findic[i].discard(findic[i][len(findic[i])-1])
                        findic[j].add(fina[j][0])
                        fina[j].discard(fina[j][0])
                        diff+=j-i

                    if(diff>=0):
                        break
            if(diff>=0):
                break
        for i in range(1,diff_level+1):
            if(len(findic[i])!=0):
                for j in range(i+1,diff_level+1):
                    if (len(fina[j])!=0 and len(findic[i])!=0):
                        fina[i].add(findic[i][len(findic[i])-1])
                        findic[i].discard(findic[i][len(findic[i])-1])
                        findic[j].add(fina[j][0])
                        fina[j].discard(fina[j][0])
                        diff+=j-i

                    if(diff>=0):
                        break
            if(diff>=0):
                break
                    
    elif(diff>0):
        x=random.choice([2,3,4,5])
        for i in range(diff_level,x,-1):
            if(len(findic[i])!=0):
                for j in range(i-1,0,-1):
                    if (len(fina[j])!=0):
                        fina[i].add(findic[i][len(findic[i])-1])
                        findic[i].discard(findic[i][len(findic[i])-1])
                        findic[j].add(fina[j][0])
                        fina[j].discard(fina[j][0])
                        diff+=j-i
                    if(diff<=0):
                        break
            if(diff<=0):
                break
        for i in range(diff_level,1,-1):
            if(len(findic[i])!=0):
                for j in range(i-1,0,-1):
                    if (len(fina[j])!=0):
                        fina[i].add(findic[i][len(findic[i])-1])
                        findic[i].discard(findic[i][len(findic[i])-1])
                        findic[j].add(fina[j][0])
                        fina[j].discard(fina[j][0])
                        diff+=j-i
                    if(diff<=0):
                        break
            if(diff<=0):
                break


    finans=[]
    for i in range(1,diff_level+1):
        if(len(findic[i])):
            for z in findic[i]:
                finans.append((i,z[0],z[1]))
    return finans

    
# arr=[(1,1,1),(2,2,3),(3,1,4),(3,2,4),(3,3,4),(5,2,4),(4,3,4),(1,2,3)]
# choosequestions(arr, 3, 3)
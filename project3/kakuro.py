import sys
import time
import csp

def add(num):
    sum=0
    for n in num:
        sum=sum+n
    return sum

class Kakuro(csp.CSP):

    def constraints(self,A,B,x,y):
        if(A[1]==B[1] or A[2]==B[2]):
            f=0
            for l in self.lines:
                if A in l[0]:
                    if B in l[0]:
                        f=1
            if A==B and f==1:
                return False

        numList=[]

        for l in self.lines:
            variables=l[0]
            res=l[1]
            nval=0
            vlen=len(variables)
            if A in variables:
                if B in variables:
                    if vlen==2:
                        sum=add([x,y])
                        if sum is res:
                            return True
                        return False
                    else:
                        for v in variables:
                            if v==A:
                                numList+=[x]
                            elif v==B:
                                numList+=[y]
                            else:
                                if self.curr_domains == None or len(self.curr_domains[v])>1:
                                    nval+=1
                            
                        sum=add(numList)
                        if nval is 0:
                            if sum is res:
                                    return True
                            return False
                        else:
                            if sum<=res:
                                return True
                            return False

    def _init_(self,rows,coloumns,lines,blackspaces):

        self.rows=rows
        self.coloumns=coloumns
        self.lines=lines
        self.blackspaces=blackspaces

        visited=[]
        adjacents=[]
        for i in rows:
            for j in coloumns:
                space=(i,j)
                if space not in blackspaces:
                    visited+=[space]
                    for x in rows:
                        for y in coloumns:
                            aspace=(x,y)
                            if aspace!=space and (i==x or j == y) and (aspace not in blackspaces):
                                adjacents[space]+=[aspace]
                    


        csp.CSP._init_(self,visited,adjacents,self.kakuro_constraints)

if _name_ == '_main_':

    inputFile=open(sys.argv[1],'r')
    dat=inputFile.readlines()
    inputFile.close()

    rows=int(len(dat[0])-1)
    coloumns=int(len(dat[1])-1)
    c=0
    posn=[]
    PosnWithSum=[]
    l=len(dat)
    for i in range(3,l):
        rows1=dat[i].split()
        coloumns1=dat[i+rows].split()
        rownums=rows1[0].split(",")
        colomnums=coloumns1[0].split(",")

        lenmax=max(len(rownums,colomnums))
        for k in range(0,lenmax-1):
            posn+=[(rownums[k],colomnums[k])]
        
        for k in range(0,lenmax-1):
            if rownums[k] is not '#' and rownums[k]!=0:
                rowsum=rownums[k]
            if colomnums[k] is not '#' and colomnums[k]!=0:
                colummsum=colomnums[k]

        PosnWithSum+=[posn,rownums,colomnums]

    blackspaces=[]

    for i in range(0,rows-1):
        for j in range(0,coloumns):
            for l in PosnWithSum:
                if posn in PosnWithSum[0]:
                    blackspaces+=[posn]

    BackTrackingS=Kakuro(rows,coloumns,PosnWithSum,blackspaces)
    final=csp.backtrackingSearch(BackTrackingS)

    MaintainingAC=Kakuro(rows,coloumns,PosnWithSum,blackspaces)
    finalMAC=csp.backtrackingSearch(MaintainingAC,csp.mac)
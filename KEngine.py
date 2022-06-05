from data.python.mainEditor import Start,newP,loadProject,CreateProject,path
import os
import sys
import shutil
true=False
t3=True
argt=""
def getStr(arr):
    r=""
    for s in arr:
        r+=s
    return r
if len(sys.argv)>0:
    i=0
    while i < len(sys.argv):
        arg=sys.argv[i]
        if arg.startswith("-"):
            true=True
            argt=arg[0:]
            t3=False
        for j in range(len(argt)):
            t2=True
            a=argt[j]
            n=0
            if a=="l":
                n=0
            elif a=="n":
                n=3
            if i+j+n<len(sys.argv) and true:
                if a=="l":
                    n=0
                    loadProject(sys.argv[i+j])
                    t3=False
                elif a=="n":
                    n=3
                    CreateProject(sys.argv[i+j],sys.argv[i+j+1],int(sys.argv[i+j+2]),int(sys.argv[i+j+3]))
            else:
                break
        i+=1
if len(sys.argv)==0 or t3:
    if os.path.isdir(sys.path[0]+"/projectStart"):
        shutil.rmtree(sys.path[0]+"/projectStart")
    newP(path,"projectStart",500,500)
    Start()
    shutil.rmtree(path+"/projectStart")
else:
    Start()
class IdError(Exception):
    def __init__(self, id) -> None:
        self.msg="o modulo: "+str(id)+" não existe, por favor coloque um modulo existente, ou adicione usando o 'addModule'"
    def __str__(self) -> str:
        return self.msg
class Module:
    def __init__(self,dict={}) -> None:
        for i in dict:
            self.__dict__.setdefault(i,dict[i])
def moduleGame(txt,scope={},modulesC={},isMain=True):
    def getModule(id=""):
        if id in modulesC:
            if isinstance(modulesC[id],dict):
                if "src" in modulesC[id]:
                    code=""
                    f=open(modulesC[id]["src"],"r")
                    f.seek(0)
                    code=f.read()
                    f.close()
                    if modulesC[id]["src"].endswith(".py"):
                        mc=dict(modulesC)
                        mc.pop(id)
                        d=moduleGame(code,{},mc,False)
                        return Module(d)
            elif isinstance(modulesC[id],str):
                mc=dict(modulesC)
                mc.pop(id)
                d=moduleGame(modulesC[id],{},mc,False)
                return Module(d)
        else:
            print(IdError(id))
    def addModule(id="",src=None,code=None):
        if id=="" or id==None:
            return
        if src!=None:
            code=""
            f=open(modulesC[id]["src"],"r")
            f.seek(0)
            code=f.read()
            f.close()
        elif code!=None:
            pass
        else:
            code=""
        modulesC.setdefault(id,code)
    if not "getModule" in scope:
        scope.setdefault("getModule",getModule)
    if not "addModule" in scope:
        scope.setdefault("addModule",addModule)
    if not "__isMain__" in scope:
        scope.setdefault("__isMain__",isMain)
    exec(txt,scope)
    if "getModule" in scope:
        scope.pop("getModule")
    return scope
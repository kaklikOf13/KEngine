#from kivy.graphics.texture import Texture
from copy import copy
#import pyduktape
import pygame
import time
from json import loads,dumps
from socket import socket,AF_INET,SOCK_STREAM
from multiprocessing import Process
from _thread import start_new_thread
from .moduleCustom import moduleGame
def noo(event=""):
    pass
def pFunction(conn,data,i=0):
    pass
def getC(id="",ca=[]):
    for i in range(len(ca)):
        if ca[i]["id"]==id:
            return i
    return None
def getStr(st='',n=1):
    chunks=[st[i:i+n] for i in range(0, len(st), n)]
    return chunks
plen=-1
def s():
    pass
class conns:
    def __init__(self,conn=""):
        self.conn=conn
    def sendPro(self,st):
        chuncks=getStr(st,1024)
        self.conn.send(str.encode(str(len(chuncks))))
        self.conn.recv(1024)
        self.conn.send(str.encode(st))
    def send(self,msg):
        if isinstance(msg,str):
            msg="str "+msg
        elif isinstance(msg,int):
            msg=str(msg)
            msg="int "+msg
        elif isinstance(msg,float):
            msg=str(msg)
            msg="float "+msg
        elif isinstance(msg,dict) or isinstance(msg,list):
            msg=dumps(msg)
            msg="dict "+msg
        self.sendPro(msg)
def switch(i,obj,txt):
    return obj.get(i,txt)
class Server:
    def __init__(self,ip,port,maxPlayers=2,configF=pFunction,commads=[{"id":"disconnect","emit":"disconnect"}]):
        self.commads=commads
        self.configF=configF
        self.addr=(ip,port)
        self.playersN=maxPlayers
        self.s=socket(AF_INET,SOCK_STREAM)
        self.playersN=0
        self.isRun=True
        self.commads=[{"id":"disconnect","emit":"disconnect"}]
        self.uptThread=None
        self.sockets=[]
    def tC(self,conn,addr):
        global plen
        reply=""
        plen+=1
        mp=plen
        conn.send(str.encode(str(self.addr)))
        conn2=conns(self.conn)
        while self.isRun:
            reply=b""
            c=None
            try:
                c=int(conn.recv(1024).decode())
            except:
                pass
            if not c:
                c=getC("disconnect",self.commads)
                if c!=None:
                    self.configF(conn2,self.commads[c]["emit"],mp)
                plen-=1
                break
            else:
                conn.send(str.encode("g"))
                for i in range(c):
                    reply+=conn.recv(1024)
                reply=reply.decode("utf-8")
                if reply!="g":
                    if reply.startswith("str "):
                        reply=reply[4:]
                    elif reply.startswith("int "):
                        reply=reply[4:]
                        reply=int(reply)
                    elif reply.startswith("float "):
                        reply=reply[6:]
                        reply=float(reply)
                    elif reply.startswith("dict "):
                        reply=reply[5:]
                        reply=loads(reply)
                    self.configF(conn2,reply,mp)
        conn.close()
    def start(self):
        self.s.bind(self.addr)
        self.s.listen(self.playersN)
    def run(self,wheel):
        self.isRun=True
        self.start()
        def thread():
            while self.run:
                wheel()
        self.uptThread=Process(target=thread,args=())
        self.uptThread.start()
        while self.isRun:
            self.update()
    def stop(self):
        self.isRun=False
        self.s.close()
        while len(self.sockets)>0:
            self.sockets[0].terminate()
            self.sockets.pop(0)
        exit()
    def update(self):
        conn,ender=self.s.accept()
        self.sockets.append(Process(target=self.uptThread,args=(conn,ender)))
        self.sockets[len(self.sockets)-1].start()
class Client:
    def __init__(self,ip,port):
        self.addr=(ip,port)
        self.s=socket(AF_INET,SOCK_STREAM)
    def send(self,data,pro=True):
        try:
            switer={
                str:"str "+data,
                int:"int "+str(data),
                float:"float "+str(data),
                dict:"dict "+dumps(data),
                list:"dict "+dumps(data)
            }
            data=switer[type(data)]
            chuncks=getStr(data,1024)
            self.s.send(str.encode(str(len(chuncks))))
            self.s.recv(1024)
            self.s.send(str.encode(data))
            c=int(self.s.recv(1024))
            self.s.send(str.encode("g"))
            d=""
            for i in range(c):
                d+=self.s.recv(1024).decode()
            if pro:
                if d.startswith("str "):
                    d=d[4:]
                elif d.startswith("int "):
                    d=d[4:]
                    d=int(d)
                elif d.startswith("float "):
                    d=d[6:]
                    d=float(d)
                elif d.startswith("dict "):
                    d=d[5:]
                    d=loads(d)
            return d
        except:
            pass
    def connect(self):
        try:
            self.s.connect(self.addr)
            self.id=self.s.recv(1024).decode()
        except:
            self.id=None
pygame.init()
class Interpret:
    """def javascript(txt,globals={}):
        context=pyduktape.DuktapeContext()
        for i in globals:
            context.set_globals(i=globals[i])
        return context.eval_js(txt)"""
    def python(txt,globals={}):
        exec(txt,globals)
        return globals
class Loader:
    def __init__(self,game=None) -> None:
        self.game=game
    def getFileTxt(self,src=""):
        file=open(src,"r+")
        file.seek(0)
        txt=file.read()
        file.close()
        return txt
    def writeFile(self,src,value):
        file=open(src,"w+")
        file.seek(0)
        file.write(value)
        file.close()
    def getJson(self,src):
        return loads(self.getFileTxt(src))
    def getPrefab(self,src=""):
        if not src.endswith(".prefab"):
            src+=".prefab"
        js=self.getJson(src)
        return js
    def savePrefab(self,obj,src):
        r={"name":obj.name,"tag":obj.tag,"comps":{"names":obj.componentsName,"publics":[]}}
        for x in range(len(obj.components)):
            if "publics" in obj.components[x]:
                r["comps"]["publics"].append({"value":obj.components[x]["publics"],"comp":r["comps"]["names"][x]})
        if not src.endswith(".prefab"):
            src+=".prefab"
        self.writeFile(src,dumps(r))
    def exportScene(self,src,game):
        r={"layers":[]}
        for i in range(len(game.layers)):
            l={"objs":[],"type":game.layers[i]["type"],"name":game.layers[i]["name"]}
            if l["type"]=="objects":
                for j in range(len(game.layers[i]["objs"])):
                    obj={"transform":{"position":{"x":game.layers[i]["objs"][j].transform.position.x,"y":game.layers[i]["objs"][j].transform.position.y},"scale":{"x":game.layers[i]["objs"][j].transform.scale.x,"y":game.layers[i]["objs"][j].transform.scale.y},"rotation":game.layers[i]["objs"][j].transform.rotation},"name":game.layers[i]["objs"][j].name,"tag":game.layers[i]["objs"][j].tag,"comps":{"names":game.layers[i]["objs"][j].componentsName,"publics":[]}}
                    if game.layers[i]["objs"][j].prefab==None:
                        for x in range(len(game.layers[i]["objs"][j].components)):
                            if "publics" in game.layers[i]["objs"][j].components[x]:
                                obj["comps"]["publics"].append({"value":game.layers[i]["objs"][j].components[x]["publics"],"comp":obj["comps"]["names"][x]})
                    else:
                        obj["comps"]=game.layers[i]["objs"][j].prefab
                    l["objs"].append(obj)
            r["layers"].append(l)
        if not src.endswith(".scene"):
            src+=".scene"
        self.writeFile(src,dumps(r))
    def getScene(self,src):
        if not src.endswith(".scene"):
            src+=".scene"
        js=self.getJson(src=src)
        for i in range(len(js["layers"])):
            for j in range(len(js['layers'][i]["objs"])):
                if isinstance(js['layers'][i]["objs"][j]["comps"],str):
                    prefab=self.getPrefab(js['layers'][i]["objs"][j]["comps"])
                    js['layers'][i]["objs"][j].setdefault("prefab",js['layers'][i]["objs"][j]["comps"])
                    js['layers'][i]["objs"][j]["comps"]=prefab["comps"]
                    js['layers'][i]["objs"][j]["name"]=prefab["name"]
                    js['layers'][i]["objs"][j]["tag"]=prefab["tag"]
        return Scene(js["layers"])
    def getImage(self,src=""):
        img=Image(self.game)
        obj=self.getJson(src)
        colors=None
        size=None
        if "size" in obj:
            size=obj["size"]
        if "colors" in obj:
            colors=obj["colors"]
        for i in obj["anims"]:
            if colors!=None:
                if "colors" in i:
                    i["colors"]=colors
                else:
                    i.setdefault("colors",colors)
            if size!=None:
                if "size" in i:
                    i["size"]=colors
                else:
                    i.setdefault("size",colors)
            img.loadAnim(i)
        return img
    def getSurface(self,src,color,width,height):
        if isinstance(src,str):
            return pygame.image.load(src).convert()
        else:
            img=pygame.Surface([width,height])
            i=0
            for y in range(height):
                for x in range(width):
                    img.fill(getrgb(color[src[i]]),[x,y,1,1])
                    i+=1
            return img.convert()
class Vector2:
    def __init__(self,x=0,y=0) -> None:
        self.x=x
        self.y=y
    def __repr__(self) -> str:
        return "<Vector2 x:"+str(self.x)+",y:"+str(self.y)+">"
class Transform:
    def __init__(self,position=Vector2(),scale=Vector2(),rotation=0) -> None:
        self.position=position
        self.scale=scale
        self.rotation=rotation
    def __repr__(self) -> str:
        return "<Transform position:"+self.position.__repr__()+", scale:"+self.scale.__repr__()+", rotation:"+str(self.rotation)+">"
def none():
    pass
class GameObject:
    def getCompPublic(self,comp=0,compsPublics=[]):
        for i in range(len(compsPublics)):
            if compsPublics[i]==None:
                continue
            if compsPublics[i]["comp"]==comp:
                return i
        return None
    def __init__(self,transform=Transform(),components=[],tag="",layer="",name="",game=None,compsPublics=[],inEditor=False,prefab=None) -> None:
        self.components=[]
        self.componentsName=[]
        self.tag=""
        self.layer=""
        self.game=None
        self.name=""
        self.transform=transform
        self.game=copy(game)
        self.name=name
        self.tag=tag
        self.layer=layer
        self.inEditor=inEditor
        self.prefab=prefab
        self.loadComps(components,compsPublics)
    def __repr__(self) -> str:
        return "<GameObejct transform:"+self.transform.__repr__()+">"
    def addComp(self,comp="",publics=None):
        txt=""
        try:
            compSrc=self.game.compsSrc[comp]
        except:
            print("não existe o component",comp)
            exit()
        if compSrc:
            self.componentsName.append(comp)
            with open(compSrc) as file:
                file.seek(0)
                txt=file.read()
                file.close()
            compR={"Image":Image,"Interpret":Interpret(),"OnEvent":noo,"hex_to_rgb":self.game.rgb,"Server":Server,"Client":Client,"gameObject":copy(self),"transform":copy(self.transform),"components":copy(self.components),"componentsNames":copy(self.componentsName),"game":copy(self.game),"name":self.name,"tag":self.tag,"layer":self.layer,"Loader":self.game.Loader(self.game),"Transform":Transform,"Vector2":Vector2,"Game":Game,"Scene":Scene,"GameObject":GameObject,"Key":self.game.key,"Mouse":self.game.mouse,"Update":none,"Draw":none,"Start":none,"inEditor":self.inEditor,"Editor":none,"OnDestroy":none}
            if compSrc.endswith(".py"):
                moduleGame(txt,compR)
                if "publics" in compR and publics!=None:
                    compR["publics"]=publics
                else:
                    compR.setdefault("publics",{})
                compR.setdefault("componentLang","python")
            """elif compSrc.endswith(".js"):
                context=pyduktape.DuktapeContext()
                context.set_globals(Image=pygame.image.load,Interpret=Interpret(),OnEvent=noo,Server=Server,Client=Client,gameObject=copy(self),transform=copy(self.transform),components=copy(self.components),componentsNames=copy(self.componentsName),game=copy(self.game),name=self.name,tag=self.tag,layer=self.layer,Loader=Loader(),Transform=Transform,Vector2=Vector2,Game=Game,Scene=Scene,GameObject=GameObject,Key=Key,Update=none,Draw=none,Start=none,inEditor=self.inEditor,Editor=none,hex_to_rgb=getrgb)
                if context.get_global("publics")!=None and publics!=None:
                    compR.setdefault("publics",publics)
                    context.set_globals(publics=compR["publics"])
                else:
                    compR.setdefault("publics",{})
                context.eval_js(txt)
                compR["Start"]=copy(context.get_global("Start"))
                compR["Update"]=copy(context.get_global("Update"))
                compR["Draw"]=copy(context.get_global("Draw"))
                if context.get_global("Editor"):
                    compR.setdefault("Editor",copy(context.get_global("Editor")))
                compR["transform"]=copy(context.get_global("transform"))
                if "publics" in compR and publics!=None:
                    compR["publics"]=copy(context.get_global("publics"))
                compR["components"]=copy(context.get_global("components"))
                compR["componentsNames"]=copy(context.get_global("componentsNames"))
                compR["game"]=copy(context.get_global("game"))
                compR.setdefault("componentLang","javascript")"""
            self.components.append(compR)
    def getComponent(self,comp=""):
        for i in range(len(self.componentsName)):
            if self.componentsName[i]==comp:
                return i
    def loadComps(self,components,compsPublics):
        i=0
        self.componentsPublics=compsPublics
        for comp in components:
            aaa=self.getCompPublic(comp,compsPublics)
            value=None
            if aaa!=None:
                value=compsPublics[aaa]["value"]
            self.addComp(comp,value)
            i+=1
    def delComp(self,i):
        self.components.pop(i)
        self.componentsName.pop(i)
    def UpComps(self):
        for comp in range(len(self.components)):
            self.components[comp]["transform"]=copy(self.transform)
    def Update(self):
        for comp in range(len(self.components)):
            self.components[comp]["Update"]()
    def Draw(self):
        for comp in range(len(self.components)):
            self.components[comp]["Draw"]()
    def Start(self):
        for comp in range(len(self.components)):
            self.components[comp]["Start"]()
    def Event(self,event):
        for comp in range(len(self.components)):
            self.components[comp]["OnEvent"](event)
    def Destroy(self):
        for comp in range(len(self.components)):
            self.components[comp]["OnDestroy"]()
    def rename(self,name):
        self.name=name
        
class Key:
    class code:
        a=ord("a")
        b=ord("b")
        c=ord("c")
        d=ord("d")
        e=ord("e")
        f=ord("f")
        g=ord("g")
        h=ord("h")
        i=ord("i")
        j=ord("j")
        k=ord("k")
        l=ord("l")
        m=ord("m")
        n=ord("n")
        o=ord("o")
        p=ord("p")
        q=ord("q")
        r=ord("r")
        s=ord("s")
        t=ord("t")
        u=ord("u")
        v=ord("v")
        w=ord("w")
        x=ord("x")
        y=ord("y")
        z=ord("z")
        space=ord(" ")
    def __init__(self):
        pass
    def pressed(self,key=ord("w")):
        if pygame.key.get_pressed()[key]:
            return True
        else:
            return False
    def down(self,key=ord("w")):
        ok=False
        for e in pygame.event.get():
            if e.type==pygame.KEYDOWN:
                if e.key==key:
                    ok=True
        return ok
    def up(self,key=ord("w")):
        ok=False
        for e in pygame.event.get():
            if e.type==pygame.KEYUP:
                if e.key==key:
                    ok=True
        return ok
class Mouse:
    def __init__(self) -> None:
        self.previewPos=self.pos()
    class code:
        leftButton=0
        middleButton=1
        rightButton=2
        scrollUp=4
        scrollDown=5
    def pos(self):
        x,y=pygame.mouse.get_pos()
        return [x,y]
    def posx(self):
        x=self.pos()[0]
        return x
    def posy(self):
        y=self.pos()[1]
        return y
    def vel(self):
        currentPos=self.pos()
        x=self.previewPos[0]-currentPos[0]
        y=self.previewPos[1]-currentPos[1]
        self.previewPos=currentPos
        return [x,y]
    def velx(self):
        vel=self.vel()
        return vel[0]
    def vely(self):
        vel=self.vel()
        return vel[0]
    def visible(self,value=True):
        pygame.mouse.set_visible(value)
    def set_pos(self,x,y):
        pygame.mouse.set_pos(x,y)
    def pressed(btn=0):
        if pygame.mouse.get_pressed()[btn]:
            return True
        else:
            return False
    def down(btn=0):
        ok=False
        for e in pygame.event.get():
            if e.type==pygame.MOUSEBUTTONDOWN:
                if e.button==btn:
                    ok=True
        return ok
    def up(btn=0):
        ok=False
        for e in pygame.event.get():
            if e.type==pygame.MOUSEBUTTONUP:
                if e.button==btn:
                    ok=True
        return ok

class Scene:
    def __init__(self,layers=[]) -> None:
        self.layers=layers
class Game:
    def mudar(self,componentsSrc={},width=500,height=500):
        self.compsSrc=componentsSrc
    def renameObj(self,i=0,layer="",name=""):
        if name=="":
            return
        l=self.getLayer(layer)
        if l!=None:
            self.layers[l]["objs"][i].rename(name)
    def renameLayer(self,layer,name):
        l=self.getLayer(layer)
        if l!=None:
            self.layers[l]["name"]=name
    def __init__(self,componentsSrc={}):
        self.compsSrc=componentsSrc
        self.Loader=Loader
        self.layers=[]
        self.isRun=True
        self.inEditor=False
        self.currentScene=None
        self.cam={"x":0,"y":0}
        self.globals={}
    def get_global(self,key):
        if key in self.globals:
            return self.globals[key]
        else:
            self.globals.setdefault(key,None)
            return self.globals[key]
    def set_global(self,key,value):
        if key in self.globals:
            self.globals[key]=value
        else:
            self.globals[key]=value
    def AddLayer(self,name):
        self.layers.append({"name":name,"type":"objects","objs":[]})
    def DeleteLayer(self,name):
        l=self.getLayer(name)
        if l!=None:
            self.layers.pop(l)
    def getLayer(self,name=""):
        for l in range(len(self.layers)):
            if self.layers[l]["name"]==name:
                return l
        return None
    def getLayerObjects(self,layer):
        return copy(self.layers[layer]["objs"])
    def InstantiatePro(self,transform=Transform(),comps=[],layer="",tag="",name="",compsP=[],chamarStart=True,prefab=None):
        l=self.getLayer(layer)
        if l!=None:
            true=False
            number=1
            if prefab!=None:
                prefab2=Loader().getPrefab(prefab)
                name=prefab2["name"]
                comps=prefab2["comps"]["names"]
                compsP=prefab2["comps"]["publics"]
                tag=prefab2["tag"]
            for i in range(len(self.layers[l]["objs"])):
                if self.layers[l]["objs"][i].name.startswith(name):
                    true=True
                    if self.layers[l]["objs"][i].name.startswith(name+" "):
                        number=int(self.layers[l]["objs"][i].name.replace(name+" ","",1))+1
            if true:
                name=name+" "+str(number)
            obj=GameObject(transform,comps,tag,layer,name,copy(self),compsP,self.inEditor,prefab)
            self.layers[l]["objs"].append(obj)
            if chamarStart:
                self.layers[l]["objs"][len(self.layers[l]["objs"])-1].Start()
            
        else:
            print("não existe a layer",layer)
            return 1
        return 0

    def Instantiate(self,gameObject=GameObject(),transform=Transform(),layer=""):
        try:
            v=self.InstantiatePro(transform,gameObject.componentsName,layer,gameObject.tag,gameObject.name,prefab=gameObject.prefab)
            return v
        except:
            return 1
    def Update(self):
        for i in range(len(self.layers)):
            if self.layers[i]["type"]=="objects":
                for obj in range(len(self.layers[i]["objs"])):
                    if obj<len(self.layers[i]["objs"]):
                        self.layers[i]["objs"][obj].Update()
    def UpComps(self):
        for i in range(len(self.layers)):
            if self.layers[i]["type"]=="objects":
                for obj in range(len(self.layers[i]["objs"])):
                    self.layers[i]["objs"][obj].UpComps()
    def Draw(self):
        for i in range(len(self.layers)):
            if self.layers[i]["type"]=="objects":
                for obj in range(len(self.layers[i]["objs"])):
                    self.layers[i]["objs"][obj].Draw()
    def Run(self):
        self.isRun=True
        while self.isRun:
            self.Update()
            time.sleep(0.030)
    def getObj(self,gameObject=GameObject(),layer=""):
        l=self.getLayer(layer)
        if l!=None:
            for obj in range(len(self.layers[l]["objs"])):
                if self.layers[l]["objs"][obj].name==gameObject.name and self.layers[l]["objs"][obj].tag==gameObject.tag:
                    return obj
        else:
            print("não existe a layer",layer)
            exit()
        return None
    def Destroy(self,gameObject=GameObject(),layer=""):
        obj=self.getObj(gameObject,layer)
        if obj!=None:
            self.layers[self.getLayer(layer)]["objs"][obj].Destroy()
            self.layers[self.getLayer(layer)]["objs"].pop(obj)
    def LoadScene(self,scene=Scene(),chamarStart=True):
        if isinstance(scene,str):
            scene=Loader().getScene(scene)
        self.LoadSceneS(scene,chamarStart)
    def LoadSceneS(self,scene=Scene(),chamarStart=True):
        while len(self.layers)>0:
            while len(self.layers[0]["objs"])>0:
                self.Destroy(self.layers[0]["objs"][0],self.layers[0]["name"])
            self.DeleteLayer(self.layers[0]["name"])
        self.currentScene=scene
        self.cam={"x":0,"y":0}
        for l in scene.layers:
            self.AddLayer(l["name"])
            for o in l["objs"]:
                prefab=None
                if "prefab" in o:
                    prefab=o["prefab"]
                self.InstantiatePro(Transform(Vector2(o["transform"]["position"]["x"],o["transform"]["position"]["y"]),Vector2(o["transform"]["scale"]["x"],o["transform"]["scale"]["y"]),o["transform"]["rotation"]),o["comps"]["names"],l["name"],o["tag"],o["name"],o["comps"]["publics"],chamarStart,prefab)
from PIL.ImageColor import getrgb
class Image:
    def __init__(self,game=Game()) -> None:
        self.anims=[]
        self.currentImg=None
        self.delay=5
        self.frame=0
        self.anim=0
        self.game=game
    def Update(self):
        if self.delay>0:
            self.delay-=1
        else:
            if self.frame<len(self.anims[self.anim]["frames"])-1:
                self.frame+=1
            else:
                self.frame=0
            self.delay=self.anims[self.anim]["delay"]
            self.currentImg=self.anims[self.anim]["frames"][self.frame]
    def playAnim(self,anim=0):
        self.anim=anim
        self.frame=0
        self.delay=self.anims[self.anim]["delay"]
        self.currentImg=self.anims[self.anim]["frames"][self.frame]
    def loadAnim(self,src):
        obj=src
        if isinstance(src,str):
            if src.endswith(".ka"):
                obj=self.game.Loader().getJson(src)
        anim={"frames":[],"delay":60}
        if "delay" in obj:
            anim["delay"]=obj["delay"]
        colors=[]
        size={"width":32,"height":32}
        if "colors" in obj:
            colors=obj["colors"]
        if "size" in obj:
            size=obj["size"]
        for f in obj["frames"]:
            frame=self.game.Loader(self.game).getSurface(f,colors,size["width"],size["height"])
            anim["frames"].append(frame)
        self.anims.append(anim)
class PygameGame(Game):
    def rgb(self,color):
        return getrgb(color)
    def __init__(self,width=500,height=500,componentsSrc={},bgColor="#0ff") -> None:
        super().__init__(componentsSrc)
        self.window=None
        self.key=Key()
        self.mouse=Mouse()
        self.bgColor=self.rgb(bgColor)
        self.window=pygame.display.set_mode((width,height))
        self.width=self.window.get_width()
        self.height=self.window.get_height()
        self.clock=pygame.time.Clock()
        self.frames=0
        self.fps=60
    def thread(self):
        while self.isRun:
            pygame.time.wait(1000)
            self.fps=self.frames
            self.frames=0
    def Draw(self):
        for i in range(len(self.layers)):
            if self.layers[i]["type"]=="objects":
                for obj in range(len(self.layers[i]["objs"])):
                    self.layers[i]["objs"][obj].Draw()
    def event(self,e):
        for i in range(len(self.layers)):
            if self.layers[i]["type"]=="objects":
                for obj in range(len(self.layers[i]["objs"])):
                    self.layers[i]["objs"][obj].Event(e)
    def drawImage(self,transform,img):
        if self.inCam(transform):
            if img.currentImg!=None:
                imgd=img.currentImg
                t1=False
                t2=False
                if transform.scale.x<0:
                    t1=True
                if transform.scale.y<0:
                    t2=True
                imgd=pygame.transform.flip(img.currentImg,t1,t2)
                self.window.blit(pygame.transform.rotate(pygame.transform.scale(imgd,(abs(transform.scale.x),abs(transform.scale.y))),transform.rotation),(transform.position.x-self.cam["x"],transform.position.y-self.cam["y"]))
    def drawRect(self,transform=Transform,color=(0,0,0)):
        if self.inCam(transform):
            pygame.draw.rect(self.window,color,[transform.position.x-self.cam["x"],transform.position.y-self.cam["y"],abs(transform.scale.x),abs(transform.scale.y)])
    def drawCenterRect(self,transform=Transform,color=(0,0,0)):
        if self.inCam(transform):
            rect=pygame.rect.Rect(transform.position.x-self.cam["x"],transform.position.y-self.cam["y"],abs(transform.scale.x),abs(transform.scale.y))
            rect.center=(transform.position.x+0,transform.position.y+0)
            pygame.draw.rect(self.window,color,rect)
    def drawRectBorder(self,transform,color,border,borderSize=1):
        if self.inCam(transform):
            w=abs(transform.scale.x)
            h=abs(transform.scale.y)
            if color!=None:
                pygame.draw.rect(self.window,color,[transform.position.x-self.cam["x"],transform.position.y-self.cam["y"],w,h])
            if border!=None:
                pygame.draw.rect(self.window,border,[transform.position.x-self.cam["x"],transform.position.y-self.cam["y"],w,h],borderSize)
    def inCam(self,transform):
        if transform.position.x+abs(transform.scale.x)>self.cam["x"] and transform.position.x<self.cam["x"]+self.width and transform.position.y+abs(transform.scale.y)>self.cam["y"] and transform.position.y<self.cam["y"]+self.height:
            return True
        return False
    def Run(self):
        self.isRun=True
        start_new_thread(self.thread,())
        while self.isRun:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    self.event("QUIT")
                    self.isRun=False
            self.window.fill(self.bgColor)
            self.Update()
            self.Draw()
            pygame.display.flip()
            self.frames+=1
            self.clock.tick(60)
        pygame.quit()
        exit()
class KivyGame(Game):
    def rgb(self,color):
        c=getrgb(color)
        return (c[0]/255,c[1]/255,c[2]/255,1)
    def get_y(self,transform):
        return self.app.root.size[1]-(transform.position.y+transform.scale.y)
    def __init__(self,width=500,height=500,componentsSrc={},bgColor="#0ff",InitialScene="") -> None:
        from kivy.app import App
        from kivy.uix.widget import Widget
        from kivy.graphics import Rectangle as KivyRectangle
        from kivy.graphics import Color as KivyColor
        from kivy.core.image import Image as KivyImage
        from kivy.clock import Clock
        from kivy.config import Config
        from kivy.core.window import Window
        class KivyAppGame(App):
            def __init__(self,**kwargs):
                App.__init__(self,**kwargs)
            def build(self):
                return KivyWidget()
        class KivyWidget(Widget):
            class KeyKV(Key):
                Kp={
                    ord("a"):False,
                    ord("b"):False,
                    ord("c"):False,
                    ord("d"):False,
                    ord("e"):False,
                    ord("f"):False,
                    ord("g"):False,
                    ord("h"):False,
                    ord("i"):False,
                    ord("j"):False,
                    ord("k"):False,
                    ord("l"):False,
                    ord("m"):False,
                    ord("n"):False,
                    ord("o"):False,
                    ord("p"):False,
                    ord("q"):False,
                    ord("r"):False,
                    ord("s"):False,
                    ord("t"):False,
                    ord("u"):False,
                    ord("v"):False,
                    ord("w"):False,
                    ord("x"):False,
                    ord("y"):False,
                    ord("z"):False,
                    ord(" "):False
                }
                def pressed(self, key=ord("w")):
                    return self.Kp.get(key,None)
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.key=self.KeyKV()
                self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
                self._keyboard.bind(on_key_down=self._on_keyboard_down)#,on_key_up=self._on_keyboard_up)
            def _keyboard_closed(self):
                self._keyboard.unbind(on_key_down=self._on_keyboard_down)#,on_key_up=self._on_keyboard_up)
                self._keyboard = None
            def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
                self.key.Kp[keycode[0]]=True
                print(modifiers,text)
            def _on_keyboard_up(self, keyboard, keycode, text, modifiers):
                print(keycode)
                super().__init__(componentsSrc)
                class LoaderS(Loader):
                    def getSurface(self,src,color=[],width=50,height=50):
                        global imgKivy
                        if isinstance(src,str):
                            img=KivyImage(src).texture
                            img.wrap="repeat"
                            return img
                        else:
                            print("por enquanto não e possivel ser outra coisa")
        self.Loader=LoaderS
        class Key:
            pass
        self.bgColor=self.rgb(bgColor)
        self.key=Key()
        self.width=width
        self.height=height
        self.cam={"x":0,"y":0}
        self.clock=pygame.time.Clock()
        self.frames=0
        self.fps=60
        self.app=KivyAppGame()
        self.initScene=InitialScene
        Config.set('graphics', 'width', str(self.width))
        Config.set('graphics', 'height', str(self.height))
        Config.write()
    def run(self):
        self.LoadScene(self.initScene)
        start_new_thread(self.thread,())
        Clock.schedule_interval(self.wheel,1/60)
    def drawImage(self,transform,img):
        if img.currentImg!=None:
            with self.app.root.canvas:
                KivyColor(1,1,1,1,mode="rgba")
                KivyRectangle(texture=img.currentImg,pos=(transform.position.x,self.get_y(transform)),size=(transform.scale.x,transform.scale.y))
    def drawRect(self,transform,color=(0,0,0)):
        with self.app.root.canvas:
            KivyColor(color[0],color[1],color[2],color[3],mode="rgba")
            KivyRectangle(pos=(transform.position.x,self.get_y(transform)),size=(transform.scale.x,transform.scale.y))
    def thread(self):
        while self.isRun:
            pygame.time.wait(1000)
            self.fps=self.frames
            self.frames=0
    def Run(self):
        self.isRun=True
        self.app.on_start=self.run
        self.app.run()
        self.isRun=False
    def wheel(self,*args):
        self.Update()
        self.Draw()
        self.frames+=1
    def Draw(self):
        self.app.root.canvas.clear()
        with self.app.root.canvas:
            KivyColor(self.bgColor[0],self.bgColor[1],self.bgColor[2],1,mode="rgba")
            KivyRectangle(pos=(0,0),size=(self.app.root.size[0],self.app.root.size[1]))
        for i in range(len(self.layers)):
            if self.layers[i]["type"]=="objects":
                for obj in range(len(self.layers[i]["objs"])):
                    self.layers[i]["objs"][obj].Draw()
    def event(self,e):
        for i in range(len(self.layers)):
            if self.layers[i]["type"]=="objects":
                for obj in range(len(self.layers[i]["objs"])):
                    self.layers[i]["objs"][obj].Event(e)

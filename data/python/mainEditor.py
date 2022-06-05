from tkinter import ACTIVE, CENTER, END, NW, BooleanVar, Checkbutton,Tk,Frame,Canvas,Menu,Toplevel,Label,Button,Entry,Listbox,Text
from tkinter.font import Font
from tkinter.ttk import Notebook
from json import loads,dumps
from copy import copy
from subprocess import Popen,PIPE
from _thread import start_new_thread
from PIL import Image,ImageTk
config={"python":"python3","scale":83}
cc=None
def run():
    cmd=f"cd {projectDir}"
    shell=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
    output,error=shell.communicate()
    cmd=config["python"]+" init.py"
    shell=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
    output,error=shell.communicate()
    consoleTE.delete("1.0",END)
    consoleTE.insert("1.0",output)
    consoleTE.insert("1.0",error)
def runScene():
    if not isfile(sceneSrc):
        showerror("erro","a cena não existe")
        return
    cmd=f"cd {projectDir}"
    shell=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
    output,error=shell.communicate()
    cmd=config["python"]+f' runScene.py -l "{sceneSrc}"'
    shell=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
    output,error=shell.communicate()
    consoleTE.delete("1.0",END)
    consoleTE.insert("1.0",output)
    consoleTE.insert("1.0",error)
def runOtherScene():
    srcSu=askopenfilename(defaultextension=".scene",filetypes=[("Scene File","*.scene")])
    if srcSu==() or srcSu=="":
        return
    cmd=f"cd {projectDir}"
    shell=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
    output,error=shell.communicate()
    cmd=config["python"]+f' runScene.py -l "{srcSu}"'
    shell=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
    output,error=shell.communicate()
    consoleTE.insert("1.0",output)
    consoleTE.insert("1.0",error)
def module(txt,scope):
    exec(txt,scope)
def getFileTxt(src=""):
    file=open(src,"r+")
    file.seek(0)
    txt=file.read()
    file.close()
    return txt
def getJson(src):
    return loads(getFileTxt(src))
def writeFile(src,value):
    file=open(src,"w+")
    file.seek(0)
    file.write(value)
    file.close()
#module(getFileTxt("data/python/sceneEditor.py"),globals())
window=Tk()
window.geometry("1000x500")
ab=""
cd=True
def getTxt(txt):
    w=Toplevel(window)
    w.resizable(False,False)
    l=Label(w,text=txt)
    l.pack()
    e=Entry(w)
    e.pack()
    def func():
        global ab,cd
        ab=e.get()
        cd=False
        w.destroy()
    btn=Button(w,text="Enter",command=func)
    btn.pack()
    global ab,cd
    w.grab_set()
    while cd:
        window.update()
    cd=True
    return ab
project=getJson("projectBase/project.kep")
#module(getFileTxt("data/python/menu.py"),globals())
#init menu module
from shutil import copytree
from tkinter.filedialog import askdirectory,askopenfilename,asksaveasfilename
from tkinter.messagebox import showerror
from os import chdir, listdir
from os.path import isfile,dirname,abspath
path=dirname(abspath(__file__))[:-12]
def newScene():
    if project!=None:
        global game
        game.LoadScene(Scene([]))
        game.AddLayer("walls")
        loadLayers()
        sceneED()
        SceneEditorCanvas.xview("scroll",game.cam2["x"],"units")
        SceneEditorCanvas.yview("scroll",
        game.cam2["y"],"units")
        game.cam2["x"]=0
        game.cam2["y"]=0
def CreateProject(dir="",name="",width=0,height=0):
    if dir!="" and name!="" and width!=0 and height!=0:
        copytree(path+"/projectBase",dir+"/"+name)
        j=getJson(path+"/projectBase/project.kep")
        j["name"]=name
        j["width"]=width
        j["height"]=height
        writeFile(dir+"/"+name+"/project.kep",dumps(j))
        return True
    else:
        showerror("error","não deu pra criar o projeto")
        return False
def loadProject(dir=""):
    if dir!="":
        global project,projectDir,folder
        projectDir=dir
        chdir(dir)
        if isfile("project.kep"):
            project=getJson("project.kep")
            game.mudar(project["components"],project["width"],project["height"])
            folder="assets"
            updateFileM()
            loadScene(project["start scene"])
            SceneEditorCanvas.config(background=project["background color"])
        else:
            project=None
def newP(dir="",name="",width=0,height=0):
    t=CreateProject(dir,name,width,height)
    if t:
        loadProject(dir+"/"+name)
        newScene()
def loadScene(src=""):
    global selectLayer,sceneSrc,mouseMove
    if src!="":
        if not isfile(src):
            return
        game.LoadScene(src,False)
        loadLayers()
        selectLayer=None
        loadObject()
        sceneSrc=src
        loadComponents()
        sceneED()
        SceneEditorCanvas.xview("scroll",-game.cam2["x"],"units")
        SceneEditorCanvas.yview("scroll",-game.cam2["y"],"units")
        game.cam2["hspeed"]=0
        game.cam2["vspeed"]=0
        game.cam2["x"]=0
        game.cam2["y"]=0
        """SceneEditorCanvas.xview("scroll",-mouseMove[0],"units")
        SceneEditorCanvas.yview("scroll",-mouseMove[1],"units")
        mouseMove=[0,0]"""
mouseMotion=[0,0]
sceneSrc=""
def saveScene():
    global sceneSrc
    if sceneSrc==()or sceneSrc=="":
        sceneSrc=asksaveasfilename(defaultextension=".scene",filetypes=[("Scene File","*.scene")])
        if not sceneSrc.endswith(".scene"):
            sceneSrc+=".scene"
    if sceneSrc==()or sceneSrc=="":
        return
    else:
        Loader().exportScene(sceneSrc,game)
def saveAsScene():
    sceneSrc=asksaveasfilename(defaultextension=".scene",filetypes=[("Scene File","*.scene")])
    if not sceneSrc.endswith(".scene"):
        sceneSrc+=".scene"
    if sceneSrc!=()or sceneSrc!="":
        Loader().exportScene(sceneSrc,game)
def newImage():
    global image
    image={"anims":[],"colors":[],"size":{"width":32,"height":32}}
def loadImage():
    global image
    file=askopenfilename(defaultextension=".ki",filetypes=[("KEngine Image",".ki")])
    if file==() or file=="":
        return
    try:
        image=Loader().getJson(file)
    except:
        showerror("erro","o arquivo tem um erro em seu codigo")
menubar=Menu(window,tearoff=0,background="#222",foreground="#fff")
fileMenu=Menu(menubar,tearoff=0,background="#222",foreground="#fff")
fileMenu.add_command(label="New Scene",command=newScene)
fileMenu.add_command(label="Load Scene",command=lambda:loadScene(askopenfilename(defaultextension=".scene",filetypes=[("Scene File","*.scene")])))
fileMenu.add_command(label="Save Scene",command=saveScene)
fileMenu.add_command(label="SaveAs Scene",command=saveAsScene)
fileMenu.add_separator()
fileMenu.add_command(label="New Project",command=lambda:newP(askdirectory(),getTxt("project name"),int(getTxt("width")),int(getTxt("height"))))
fileMenu.add_command(label="Load Project",command=lambda:loadProject(askdirectory()))
fileMenu.add_separator()
fileMenu.add_command(label="New Image",command=newImage)
fileMenu.add_command(label="Load Image")
menubar.add_cascade(menu=fileMenu,label="File")
runMenu=Menu(menubar,tearoff=0,background="#222",foreground="#fff")
runMenu.add_command(label="Run Game",command=lambda:start_new_thread(run,()))
runMenu.add_command(label="Run This Scene",command=lambda:start_new_thread(runScene,()))
runMenu.add_command(label="Run Other Scene",command=lambda:start_new_thread(runOtherScene,()))
menubar.add_cascade(label="Run",menu=runMenu)
window.config(menu=menubar)
#end menu module
#module(getFileTxt("data/python/customGame.py"),globals())
#init customGame module
from projectBase.engine import Game, GameObject,Transform,Vector2,Scene,Loader,getrgb,Key,Mouse
from projectBase.engine import Image as ImagePygame
def rgb_to_hex(rgb):
    if rgb[0]==None:
        return ""
    return '#{:02X}{:02X}{:02X}'.format(rgb[0],rgb[1],rgb[2])
class SceneEditorGame(Game):
    cam2={"x":0,"y":0,"hspeed":0,"vspeed":0}
    cam={"x":0,"y":0}
    width=500
    height=500
    def __init__(self, componentsSrc=...) -> None:
        super().__init__(componentsSrc)
        self.inEditor=True
        self.rgb=getrgb
        self.key=Key()
        self.mouse=Mouse()
    def mudar(self,componentsSrc={},width=500,height=500):
        self.compsSrc=componentsSrc
        self.width=width
        self.height=height
    def drawKI(self,transform,img,frame=0):
        y=0
        i=0
        if transform.scale.x==0 or transform.scale.y==0 or img==None:
            return
        for col in range(img["size"]["height"]):
            x=0
            for row in range(img["size"]["width"]):
                color=img["frames"][frame][i]
                x2=x+transform.position.x
                y2=y+transform.position.y
                SceneEditorCanvas.create_rectangle(x2,y2,x2+transform.scale.x,y2+transform.scale.y,fill=img["colors"][color],outline="")
                i+=1
                x+=transform.scale.x
            y+=transform.scale.x
    def drawImage(self,transform,img):
        global imgN
        if isfile(img) and transform.scale.x>0 and transform.scale.y>0:
            imgN2=Image.open(img)
            imgN2=imgN2.resize((transform.scale.x,transform.scale.y),Image.ANTIALIAS)
            imgN2=imgN2.rotate(transform.rotation)
            imgN=ImageTk.PhotoImage(imgN2)
            SceneEditorCanvas.create_image(transform.position.x,transform.position.y,image=imgN,anchor="nw")
    def drawRect(self,transform,color):
        if isinstance(color,list) or isinstance(color,tuple):
            color=rgb_to_hex((color[0],color[1],color[2]))
        SceneEditorCanvas.create_rectangle(transform.position.x,transform.position.y,transform.position.x+transform.scale.x,transform.position.y+transform.scale.y,fill=color,outline="")
    def drawCenterRect(self,transform,color):
        if isinstance(color,list) or isinstance(color,tuple):
            color=rgb_to_hex((color[0],color[1],color[2]))
        SceneEditorCanvas.create_rectangle(transform.position.x,transform.position.y,transform.position.x+transform.scale.x,transform.position.y+transform.scale.y,fill=color,outline="")
    def drawRectBorder(self,transform,color,border,borderSize):
        if color!=None:
            if isinstance(color,list) or isinstance(color,tuple):
                color=rgb_to_hex((color[0],color[1],color[2]))
        else:
            color=""
        if border!=None:
            if isinstance(border,list) or isinstance(border,tuple):
                border=rgb_to_hex((border[0],border[1],border[2]))
        else:
            border=""
        SceneEditorCanvas.create_rectangle(transform.position.x,transform.position.y,transform.position.x+transform.scale.x,transform.position.y+transform.scale.y,fill=color,outline=border,width=borderSize)
#end cutomGame module
def addLayer(name=""):
    if name!="":
        game.AddLayer(name)
        loadLayers()
def deleteLayer(name=""):
    global selectLayer
    if name!=""and name!=None:
        game.DeleteLayer(name)
        loadLayers()
        if name==selectLayer:
            selectLayer=None
            loadObject()
            loadComponents()
        sceneED()
def renameLayer(name=""):
    global selectLayer
    atn=selectLayer
    game.renameLayer(selectLayer,name)
    if atn!=name:
        selectLayer=None
        loadObject()
    loadLayers()
comps=[]
comps2=[]
def loadComponents():
    global selectObject,selectLayer,comps,comps2
    i=0
    while len(comps)>0:
        comps[0].destroy()
        comps.pop(0)
    while len(comps2)>0:
        comps2[0]["value"].destroy()
        if "btn" in comps2[0]:
            comps2[0]["btn"].destroy()
        comps2[0]["l"].destroy()
        comps2.pop(0)
    del i
    window.update()
    if selectObject!=None:
        l=game.getLayer(selectLayer)
        if l!=None:
            window.update()
            tl=Label(componentsEditorF,text="transform:",background="#000",foreground="#fff",anchor=NW)
            tl.place(x=0,y=0)
            window.update()
            comps.append(copy(tl))
            tpl=Label(componentsEditorF,text="position:",background="#000",foreground="#fff",anchor=NW)
            tpl.place(x=10,y=tl.winfo_y()+tl.winfo_height())
            window.update()
            comps.append(copy(tpl))
            tpxl=Label(componentsEditorF,text="x:",background="#000",foreground="#fff",anchor=NW)
            tpxl.place(x=20,y=tpl.winfo_y()+tpl.winfo_height())
            window.update()
            comps.append(copy(tpxl))
            tpxe=Entry(componentsEditorF)
            tpxe.insert(END,str(game.layers[l]["objs"][selectObject].transform.position.x))
            tpxe.place(x=tpxl.winfo_x()+tpxl.winfo_width(),y=tpxl.winfo_y())
            window.update()
            comps.append(copy(tpxe))
            tpyl=Label(componentsEditorF,text="y:",background="#000",foreground="#fff",anchor=NW)
            tpyl.place(x=20,y=tpxl.winfo_y()+tpxl.winfo_height())
            comps.append(copy(tpyl))
            window.update()
            tpye=Entry(componentsEditorF)
            tpye.insert(END,str(game.layers[l]["objs"][selectObject].transform.position.y))
            tpye.place(x=tpyl.winfo_x()+tpyl.winfo_width(),y=tpyl.winfo_y())
            comps.append(copy(tpye))
            window.update()
            tsl=Label(componentsEditorF,text="scale:",background="#000",foreground="#fff",anchor=NW)
            tsl.place(x=10,y=tpye.winfo_y()+tpye.winfo_height())
            window.update()
            comps.append(copy(tsl))
            tsxl=Label(componentsEditorF,text="x:",background="#000",foreground="#fff",anchor=NW)
            tsxl.place(x=20,y=tsl.winfo_y()+tsl.winfo_height())
            window.update()
            comps.append(copy(tsxl))
            tsxe=Entry(componentsEditorF)
            tsxe.place(x=tsxl.winfo_x()+tsxl.winfo_width(),y=tsxl.winfo_y())
            window.update()
            comps.append(copy(tsxe))
            tsyl=Label(componentsEditorF,text="y:",background="#000",foreground="#fff",anchor=NW)
            tsxe.insert(END,str(game.layers[l]["objs"][selectObject].transform.scale.x))
            tsyl.place(x=20,y=tsxl.winfo_y()+tsxl.winfo_height())
            window.update()
            tsye=Entry(componentsEditorF)
            tsye.insert(END,str(game.layers[l]["objs"][selectObject].transform.scale.y))
            tsye.place(x=tsyl.winfo_x()+tsyl.winfo_width(),y=tsyl.winfo_y())
            window.update()
            comps.append(copy(tsye))
            comps.append(copy(tsyl))
            trl=Label(componentsEditorF,text="rotation:",background="#000",foreground="#fff",anchor=NW)
            trl.place(x=10,y=tsye.winfo_y()+tsye.winfo_height())
            window.update()
            tre=Entry(componentsEditorF)
            tre.place(x=trl.winfo_x()+trl.winfo_width(),y=trl.winfo_y())
            tre.insert(END,str(game.layers[l]["objs"][selectObject].transform.rotation))
            comps.append(copy(trl))
            comps.append(copy(tre))
            window.update()
            i=0
            def DelComp(i):
                if selectObject!=None:
                    l=game.getLayer(selectLayer)
                    if l!=None:
                        game.layers[l]["objs"][selectObject].delComp(i)
                        loadComponents()
            for i in range(len(game.layers[l]["objs"][selectObject].components)):
                game.layers[l]["objs"][selectObject].components[i]["Editor"]()
                label=Label(componentsEditorF,text=game.layers[l]["objs"][selectObject].componentsName[i],background="#000",foreground="#fff",anchor=NW)
                btnr=Button(componentsEditorF,text="x",background="#000",foreground="#fff",command=lambda:DelComp(int(i)+0),width=1,height=1)
                x=0
                y=0
                if i==0:
                    y=comps[len(comps)-1].winfo_y()+comps[len(comps)-1].winfo_height()
                else:
                    y=comps2[len(comps2)-1]["value"].winfo_y()+comps2[len(comps2)-1]["value"].winfo_height()
                label.place(x=x,y=y)
                window.update()
                btnr.place(x=x+label.winfo_width(),y=y,anchor=NW)
                comps.append(copy(label))
                comps.append(copy(btnr))
                window.update()
                j=0
                for p in game.layers[l]["objs"][selectObject].components[i]["publics"]:
                    value={"value":None,"type":"","l":Label(componentsEditorF,text=p,background="#000",foreground="#fff",anchor=NW)}
                    y=0
                    if j==0:
                        y=comps[len(comps)-1].winfo_y()+comps[len(comps)-1].winfo_height()
                    else:
                        y=comps2[len(comps2)-1]["value"].winfo_y()+comps2[len(comps2)-1]["value"].winfo_height()
                    value["l"].place(x=10,y=y)
                    window.update()
                    if isinstance(game.layers[l]["objs"][selectObject].components[i]["publics"][p],bool):
                        value.setdefault("bV",BooleanVar())
                        value["bV"].set(game.layers[l]["objs"][selectObject].components[i]["publics"][p])
                        value["value"]=Checkbutton(componentsEditorF,variable=value["bV"],background="#000",borderwidth=0)
                        value["value"].place(x=value["l"].winfo_x()+value["l"].winfo_width(),y=value["l"].winfo_y())
                        value["type"]="bool"
                    elif isinstance(game.layers[l]["objs"][selectObject].components[i]["publics"][p],str):
                        value["value"]=Entry(componentsEditorF)
                        value["value"].place(x=value["l"].winfo_x()+value["l"].winfo_width(),y=value["l"].winfo_y())
                        value["type"]="str"
                        value["value"].insert(END,str(game.layers[l]["objs"][selectObject].components[i]["publics"][p]))
                    elif isinstance(game.layers[l]["objs"][selectObject].components[i]["publics"][p],int):
                        value["value"]=Entry(componentsEditorF)
                        value["value"].place(x=value["l"].winfo_x()+value["l"].winfo_width(),y=value["l"].winfo_y())
                        value["type"]="int"
                        value["value"].insert(END,str(game.layers[l]["objs"][selectObject].components[i]["publics"][p]))
                    elif isinstance(game.layers[l]["objs"][selectObject].components[i]["publics"][p],float):
                        value["value"]=Entry(componentsEditorF)
                        value["value"].place(x=value["l"].winfo_x()+value["l"].winfo_width(),y=value["l"].winfo_y())
                        value["type"]="float"
                        value["value"].insert(END,str(game.layers[l]["objs"][selectObject].components[i]["publics"][p]))
                    elif isinstance(game.layers[l]["objs"][selectObject].components[i]["publics"][p],ImagePygame):
                        value["value"]=Entry(componentsEditorF)
                        value["value"].place(x=value["l"].winfo_x()+value["l"].winfo_width(),y=value["l"].winfo_y())
                        value["type"]="str"
                        window.update()
                        def cmdToAdd():
                            cs=fileMLB2.curselection()
                            if cs==None or cs==():
                                return
                            selectF=fileMLB2.get(cs)
                            value["value"].delete(0,END)
                            value["value"].insert(folder+"/"+selectF)
                        value.setdefault("btn",Button(componentsEditorF,command=cmdToAdd,text="find",background="#000",foreground="#fff"))
                        value["btn"].place(x=value["value"].winfo_x()+value["value"].winfo_width(),y=value["value"].winfo_y())
                    window.update()
                    comps2.append(copy(value))
                    j+=1
            def addComp():
                if selectObject!=None:
                    l=game.getLayer(selectLayer)
                    if l!=None:
                        game.layers[l]["objs"][selectObject].addComp(getTxt("comp name"),None)
                        game.layers[l]["objs"][selectObject].components[len(game.layers[l]["objs"][selectObject].components)-1]["inEditor"]=True
                loadComponents()
            btn=Button(componentsEditorF,text="add",command=addComp)
            y=0
            if len(comps2)>0:
                y=comps2[len(comps2)-1]["value"].winfo_y()+comps2[len(comps2)-1]["value"].winfo_height()
            else:
                y=comps[len(comps)-1].winfo_y()+comps[len(comps)-1].winfo_height()
            btn.place(x=0,y=y)
            comps.append(copy(btn))
    sceneED()
game=SceneEditorGame(project["components"])
mainNb=Notebook(window)
mainNb.place(anchor=CENTER,relx=0.5,rely=0.3,relwidth=0.5,relheight=0.6)
calcF=Frame(mainNb,background="#000")
calcTE=Text(calcF)
calcTE.place(relx=0.5,rely=0.1,relwidth=1,relheight=0.2,anchor=CENTER)
calcR=Label(calcF,background="#000",foreground="#fff",text='0')
calcR.place(relx=0.5,rely=0.3,relwidth=0.2,relheight=0.2,anchor=CENTER)
calcBtns=[
    Button(calcF,text="1",background="#000",foreground="#fff"),Button(calcF,text="2",background="#000",foreground="#fff"),Button(calcF,text="3",background="#000",foreground="#fff"),
    Button(calcF,text="4",background="#000",foreground="#fff"),Button(calcF,text="5",background="#000",foreground="#fff"),Button(calcF,text="6",background="#000",foreground="#fff"),
    Button(calcF,text="7",background="#000",foreground="#fff"),Button(calcF,text="8",background="#000",foreground="#fff"),Button(calcF,text="9",background="#000",foreground="#fff"),
    Button(calcF,text="0",background="#000",foreground="#fff"),Button(calcF,text="+",background="#000",foreground="#fff"),Button(calcF,text="-",background="#000",foreground="#fff"),
    Button(calcF,text="*",background="#000",foreground="#fff"),Button(calcF,text="/",background="#000",foreground="#fff"),Button(calcF,text=".",background="#000",foreground="#fff"),
    Button(calcF,text="(",background="#000",foreground="#fff"),Button(calcF,text=")",background="#000",foreground="#fff"),Button(calcF,text="entry",background="#000",foreground="#fff")
]
calcBtnsS=0
y=0.4
for row in range(6):
    x=0.4
    for collum in range(3):
        def cmd():
            pass
        if calcBtnsS==0:
            def cmd():
                calcTE.insert(END,"1")
        elif calcBtnsS==1:
            def cmd():
                calcTE.insert(END,"2")
        elif calcBtnsS==2:
            def cmd():
                calcTE.insert(END,"3")
        elif calcBtnsS==3:
            def cmd():
                calcTE.insert(END,"4")
        elif calcBtnsS==4:
            def cmd():
                calcTE.insert(END,"5")
        elif calcBtnsS==5:
            def cmd():
                calcTE.insert(END,"6")
        elif calcBtnsS==6:
            def cmd():
                calcTE.insert(END,"7")
        elif calcBtnsS==7:
            def cmd():
                calcTE.insert(END,"8")
        elif calcBtnsS==8:
            def cmd():
                calcTE.insert(END,"9")
        elif calcBtnsS==9:
            def cmd():
                calcTE.insert(END,"0")
        elif calcBtnsS==10:
            def cmd():
                calcTE.insert(END,"+")
        elif calcBtnsS==11:
            def cmd():
                calcTE.insert(END,"-")
        elif calcBtnsS==12:
            def cmd():
                calcTE.insert(END,"*")
        elif calcBtnsS==13:
            def cmd():
                calcTE.insert(END,"/")
        elif calcBtnsS==14:
            def cmd():
                calcTE.insert(END,".")
        elif calcBtnsS==15:
            def cmd():
                calcTE.insert(END,"(")
        elif calcBtnsS==16:
            def cmd():
                calcTE.insert(END,")")
        elif calcBtnsS==17:
            def cmd():
                try:
                    calcR.config(text=eval(calcTE.get("1.0",END)))
                except:
                    showerror("calc error","não deu para fazer a conta")
        calcBtns[calcBtnsS].config(command=cmd)
        calcBtns[calcBtnsS].place(relx=x,rely=y,relwidth=0.1,relheight=0.1,anchor=CENTER)
        calcBtnsS+=1
        x+=0.1
    y+=0.10
del calcBtnsS
mainNb2=Notebook(window)
mainNb2.place(anchor=CENTER,relx=0.5,rely=0.8,relwidth=0.5,relheight=0.4)
folder="assets"
def updateFileM():
    f=listdir(folder)
    fileMLB.delete(0,END)
    fileMLB2.delete(0,END)
    for i in f:
        if isfile(folder+"/"+i):
            if i.endswith(".py"):
                fileMLB.insert(END,"Script")
            elif i.endswith(".ki"):
                fileMLB.insert(END,"KEngine Image")
            elif i.endswith(".ka"):
                fileMLB.insert(END,"KEngine Animation")
            elif i.endswith(".png"):
                fileMLB.insert(END,"Image")
            elif i.endswith(".scene"):
                fileMLB.insert(END,"KEngine Scene")
            elif i.endswith(".prefab"):
                fileMLB.insert(END,"KEngine Prefab")
        else:
            fileMLB.insert(END,"Folder")
        fileMLB2.insert(END,i)
selectPrefab=None
def oFolder(e):
    global folder,fileMLB2,selectPrefab
    cs=fileMLB2.curselection()
    if cs==None or cs==():
        return
    selectF=fileMLB2.get(cs)
    if selectF!=None and selectF !="":
        selectF2=fileMLB.get(cs)
        if selectF2=="Folder":
            folder+="/"+selectF
            selectF=None
            updateFileM()
        elif selectF2=="KEngine Scene":
            loadScene(folder+"/"+selectF)
        elif selectF2=="KEngine Prefab":
            selectPrefab=folder+"/"+selectF
def retToNext():
    global folder
    n=folder.split("/")
    if len(n)==1:
        return
    else:
        folder=folder[:-(1+len(n[len(n)-1]))]
        updateFileM()
fileMF=Frame(mainNb2,background="#000")
fileMLB=Listbox(fileMF,background="#000",foreground="#fff")
fileMLB.place(relwidth=0.2,relheight=1)
fileMLB2=Listbox(fileMF,background="#000",foreground="#fff")
fileMLB2.place(relx=0.2,relwidth=0.7,relheight=1)
fileMLB2.bind("<Button-1>",oFolder)
fileMBtn=Button(fileMF,text="<=",background="#000",command=retToNext,foreground="#fff",activebackground="#333")
fileMBtn.place(relx=0.9,relwidth=1,relheight=1)
mainNb2.add(fileMF,text="File Manager")
consoleF=Frame(mainNb2,background="#000")
consoleTE=Text(consoleF,background="#000",foreground="#fff")
consoleTE.place(relwidth=1,relheight=1,anchor=NW)
mainNb2.add(consoleF,text="Console")
leftNb=Notebook(window)
leftNb.place(anchor=CENTER,relx=0.125,rely=0.5,relheight=1,relwidth=0.25)
rightNb=Notebook(window)
rightNb.place(anchor=CENTER,relx=0.875,rely=0.5,relheight=1,relwidth=0.25)
componentsEditorF=Frame(rightNb,background="#000")
rightNb.add(componentsEditorF,text="Components Editor")
layerEditorF=Frame(leftNb,background="#000")
layerEditorLB=Listbox(layerEditorF,background="#000",foreground="#fff")
layerEditorLB.place(anchor=CENTER,relx=0.5,rely=0.5,relwidth=1,relheight=1)
layerEditorLBM=Menu(window,tearoff=0,background="#000",foreground="#fff")
layerEditorLBM.add_command(label="Add Layer",command=lambda:addLayer(getTxt("Layer Name")))
layerEditorLBM.add_command(label="Delete Layer",command=lambda:deleteLayer(layerEditorLB.get(ACTIVE)))
layerEditorLBM.add_separator()
layerEditorLBM.add_command(label="Rename Layer",command=lambda:renameLayer(getTxt("Layer Name")))
def do_popup(event):
    try:
        layerEditorLBM.tk_popup(event.x_root, event.y_root)
    finally:
        layerEditorLBM.grab_release()
selectLayer=None
def loadObject():
    global selectLayer
    objectEditorLB.delete(0,END)
    if selectLayer!=None:
        l=game.getLayer(selectLayer)
        if l!=None:
            for i in range(len(game.layers[l]["objs"])):
                objectEditorLB.insert(END,game.layers[l]["objs"][i].name)
        else:
            selectLayer=None
def sl(e):
    txt=layerEditorLB.get(ACTIVE)
    if txt!="":
        global selectLayer
        selectLayer=txt
        loadObject()
def saveComponents():
    if selectObject!=None:
        l=game.getLayer(selectLayer)
        if l!=None:
            game.layers[l]["objs"][selectObject].transform=Transform(Vector2(int(comps[3].get()),int(comps[5].get())),Vector2(int(comps[8].get()),int(comps[9].get())),int(comps[12].get()))
            j=0
            for i in range(len(game.layers[l]["objs"][selectObject].components)):
                game.layers[l]["objs"][selectObject].components[i]["Editor"]()
                for p in game.layers[l]["objs"][selectObject].components[i]["publics"]:
                    if comps2[j]["type"]=="str":
                        game.layers[l]["objs"][selectObject].components[i]["publics"][p]=str(comps2[j]["value"].get())
                    elif comps2[j]["type"]=="int":
                        game.layers[l]["objs"][selectObject].components[i]["publics"][p]=int(comps2[j]["value"].get())
                    elif comps2[j]["type"]=="float":
                        game.layers[l]["objs"][selectObject].components[i]["publics"][p]=float(comps2[j]["value"].get())
                    elif comps2[j]["type"]=="bool":
                        game.layers[l]["objs"][selectObject].components[i]["publics"][p]=comps2[j]["bV"].get()
                    j+=1
            sceneED()
setas=None
def sceneED():
    SceneEditorCanvas.delete("all")
    game.drawRectBorder(Transform(Vector2(game.cam["x"]-3,game.cam["y"]-3),Vector2(game.width+5,game.height+5),0),"","#000",5)
    game.UpComps()
    game.Draw()
    if selectObject!=None and selectLayer!=None:
        l=game.getLayer(selectLayer)
        global setas
        setas=[]
        setas.append([game.layers[l]["objs"][selectObject].transform.position.x+game.layers[l]["objs"][selectObject].transform.scale.x+20,game.layers[l]["objs"][selectObject].transform.position.y+(game.layers[l]["objs"][selectObject].transform.scale.y/2-10),100,20])
        setas.append([game.layers[l]["objs"][selectObject].transform.position.x-120,game.layers[l]["objs"][selectObject].transform.position.y+(game.layers[l]["objs"][selectObject].transform.scale.y/2-10),100,20])
        setas.append([game.layers[l]["objs"][selectObject].transform.position.x+(game.layers[l]["objs"][selectObject].transform.scale.x/2-10),game.layers[l]["objs"][selectObject].transform.position.y+game.layers[l]["objs"][selectObject].transform.scale.y+20,20,100])
        setas.append([game.layers[l]["objs"][selectObject].transform.position.x+(game.layers[l]["objs"][selectObject].transform.scale.x/2-10),game.layers[l]["objs"][selectObject].transform.position.y-120,20,100])
        game.drawRect(Transform(Vector2(setas[0][0],setas[0][1]),Vector2(setas[0][2],setas[0][3])),(255,0,0))
        game.drawRect(Transform(Vector2(setas[1][0],setas[1][1]),Vector2(setas[1][2],setas[1][3])),(255,0,0))
        game.drawRect(Transform(Vector2(setas[2][0],setas[2][1]),Vector2(setas[2][2],setas[2][3])),(0,255,0))
        game.drawRect(Transform(Vector2(setas[3][0],setas[3][1]),Vector2(setas[3][2],setas[3][3])),(0,255,0))
layerEditorLB.bind("<Button-3>",do_popup)
layerEditorLB.bind("<Button-1>",sl)
leftNb.add(layerEditorF,text="Layer Editor")
objectEditorF=Frame(leftNb,background="#000")
objectEditorLB=Listbox(objectEditorF,background="#000",foreground="#fff")
objectEditorLB.place(anchor=CENTER,relx=0.5,rely=0.45,relwidth=1,relheight=0.9)
objectEditorBtn=Button(objectEditorF,background="#000",foreground="#fff",text="Save Components",command=saveComponents)
objectEditorBtn.place(anchor=CENTER,relx=0.5,rely=0.95,relwidth=1,relheight=0.15)
objectEditorLBM=Menu(window,tearoff=0,background="#000",foreground="#fff")
objectEditorLBM2=Menu(window,tearoff=0,background="#000",foreground="#fff")
def createNone(name=""):
    if name!="":
        if selectLayer==None:
            return
        game.InstantiatePro(name=name,comps=[],layer=selectLayer,tag="None",compsP=[],chamarStart=False)
        global selectObject
        if selectObject!=None:
            if selectObject>=len(game.layers[game.getLayer(selectLayer)]["objs"])-1:
                selectObject=None
                loadComponents()
        loadObject()
def createRect(name=""):
    if name!="":
        if selectLayer==None:
            return
        game.InstantiatePro(Transform(scale=Vector2(50,50)),["Rectangle"],selectLayer,"Rect",name,[None],chamarStart=False)
        global selectObject
        if selectObject!=None:
            if selectObject>=len(game.layers[game.getLayer(selectLayer)]["objs"])-1:
                selectObject=None
                loadComponents()
        loadObject()
        sceneED()
def createBPP(name=""):
    if name!="":
        if selectLayer==None:
            return
        game.InstantiatePro(Transform(scale=Vector2(50,50)),["Rectangle","BasicPlatformPlayer","BoxCollision"],selectLayer,"Player",name,[None,None,None],chamarStart=False)
        global selectObject
        if selectObject!=None:
            if selectObject>=len(game.layers[game.getLayer(selectLayer)]["objs"])-1:
                selectObject=None
                loadComponents()
        loadObject()
        sceneED()
def createImage(name=""):
    if name!="":
        if selectLayer==None:
            return
        game.InstantiatePro(Transform(scale=Vector2(64,64)),["Image"],selectLayer,"Image",name,[None],chamarStart=False)
        global selectObject
        if selectObject!=None:
            if selectObject>=len(game.layers[game.getLayer(selectLayer)]["objs"])-1:
                selectObject=None
                loadComponents()
        loadObject()
        sceneED()
def createPrefab():
        if selectLayer==None:
            return
        if selectPrefab==None:
            return
        game.InstantiatePro(Transform(scale=Vector2(64,64)),[],selectLayer,prefab=selectPrefab,chamarStart=False)
        global selectObject
        if selectObject!=None:
            if selectObject>=len(game.layers[game.getLayer(selectLayer)]["objs"])-1:
                selectObject=None
                loadComponents()
        loadObject()
        sceneED()
def createCam(name=""):
    if name!="":
        if selectLayer==None:
            return
        game.InstantiatePro(Transform(scale=Vector2(50,50)),["Camera"],selectLayer,"Player",name,[None])
        global selectObject
        if selectObject!=None:
            if selectObject>=len(game.layers[game.getLayer(selectLayer)]["objs"])-1:
                selectObject=None
                loadComponents()
        sceneED()
def deleteObj():
    global selectObject
    if selectObject!=None and selectLayer!=None:
        l=game.getLayer(selectLayer)
        if l!=None:
            game.layers[l]["objs"].pop(selectObject)
            selectObject=None
            loadComponents()
            loadObject()
            sceneED()
def renameObject():
    txt=objectEditorLB.get(ACTIVE)
    if txt!="" and selectLayer!=None:
        cur=objectEditorLB.curselection()[0]
        if cur!=None:
            game.renameObj(cur,selectLayer,getTxt("Name"))
            loadObject()
def savePrefab():
    txt=objectEditorLB.get(ACTIVE)
    if txt!="" and selectLayer!=None:
        l=game.getLayer(selectLayer)
        if l!=None:
            file=asksaveasfilename(defaultextension=".prefab",filetypes=[("KEngine pre fabricate object",".prefab")])
            if file=="" or file==():
                return
            Loader().savePrefab(game.layers[l]["objs"][selectObject],file)
            loadObject()
            sceneED()
objectEditorLBM2.add_command(label="None",command=lambda:createNone(getTxt("Name")))
objectEditorLBM2.add_command(label="Rectangle",command=lambda:createRect(getTxt("Name")))
objectEditorLBM2.add_command(label="Basic Plataform Player",command=lambda:createBPP(getTxt("Name")))
objectEditorLBM2.add_command(label="Image",command=lambda:createImage(getTxt("Name")))
objectEditorLBM2.add_command(label="Prefab",command=createPrefab)
objectEditorLBM.add_cascade(menu=objectEditorLBM2,label="Create Object")
objectEditorLBM.add_command(label="Delete Object",command=deleteObj)
objectEditorLBM.add_command(label="Rename Object",command=renameObject)
objectEditorLBM.add_separator()
objectEditorLBM.add_command(label="Save Prefab",command=savePrefab)
def do_popup2(event):
    try:
        objectEditorLBM.tk_popup(event.x_root, event.y_root)
    finally:
        objectEditorLBM.grab_release()
objectEditorLB.bind("<Button-3>",do_popup2)
selectObject=None
def so(e):
    global selectObject
    global selectLayer
    txt=objectEditorLB.get(ACTIVE)
    if txt!="" and selectLayer!=None and len(objectEditorLB.curselection())>0:
        cur=objectEditorLB.curselection()[0]
        selectObject=cur
        loadComponents()
objectEditorLB.bind("<Button-1>",so)
leftNb.add(objectEditorF,text="Objects Editor")
sceneEditor=Frame(mainNb,background="#000")
after=""
def UpdateAnims():
    animsLB.delete(0,END)
    for i in range(len(image["anims"])):
        animsLB.insert(END,i+1)
def addAnim():
    global image
    image["anims"].append({"frames":[],"delay":30})
    UpdateAnims()
def imAnim():
    file=askopenfilename(defaultextension=".ka",filetypes=[("Animation File",".ka")])
    if file==() or file=="":
        return
    txt=""
    with open(file,"r+") as f:
        try:
            txt=loads(f.read())
        except:
            showerror("erro","animação tem um erro no arquivo")
    colors=[]
    if "colors" in txt:
        colors=txt["colors"]
        txt.pop("colors")
    image["anims"].append(txt)
    image["colors"]+=colors
    UpdateAnims()
def do_popup(event):
    try:
        animsLBM.tk_popup(event.x_root, event.y_root)
    finally:
        animsLBM.grab_release()
def do_popup1(event):
    try:
        framesLBM.tk_popup(event.x_root, event.y_root)
    finally:
        framesLBM.grab_release()
def doP(event):
    global selectAnim
    s=animsLB.get(ACTIVE)
    if s==None or s=="":
        selectAnim=None
    else:
        selectAnim=int(s)-1
def DelAnim():
    global selectAnim
    if selectAnim!=None:
        image["anims"].pop(selectAnim)
        selectAnim=None
        UpdateAnims()
def UpdateFrames():
    framesLB.delete(0,END)
    if selectAnim!=None:
        for i in range(len(image["anims"][selectAnim]["frames"])):
            framesLB.insert(END,i+1)
def addFrames():
    files=askopenfilename(defaultextension=".png",filetypes=[("Image PNG",".png")])
    if files=="" or files==None or selectAnim==None:
        return
    else:
        files=list(files)
        for i in files:
            image["anims"][selectAnim].append(i)
        UpdateFrames()
selectAnim=None
image={"anims":[],"colors":[],"size":{"width":32,"height":32}}
animsF=Frame(leftNb,background="#000")
animsLB=Listbox(animsF,background="#000",foreground="#fff")
animsLBM=Menu(window,tearoff=0,background="#000",foreground="#fff")
animsLBM.add_command(command=addAnim,label="Add")
animsLBM.add_command(label="Import",command=imAnim)
animsLBM.add_separator()
animsLBM.add_command(label="Delete",command=DelAnim)
animsLB.bind("<Button-3>",do_popup)
animsLB.bind("<Button-1>",doP)
animsLB.place(relwidth=1,relheight=1)
framesF=Frame(leftNb)
framesLBM=Menu(window,tearoff=0,background="#000",foreground="#fff")
framesLBM.add_command(label="Import",command=addFrames)
framesLB=Listbox(framesF,background="#000",foreground="#fff")
framesLB.place(relwidth=1,relheight=1)
framesLB.bind("<Button-3>",do_popup1)
leftNb.add(animsF,text="animations")
leftNb.add(framesF,text="frames")
"""canvas=Canvas(mainNb,background="#000",borderwidth=0)
canvas.pack()"""
utimaMotion=[0,0]
mouseMove=[0,0]
speed=1
def Wheel():
    global after
    after=window.after(30,Wheel)
def Motion(e):
    global utimaMotion,mouseMotion,rightP,movePress,mouseMove
    mouseMove=[e.x,e.y]
    mouseMotion[0]=int(e.x-utimaMotion[0])
    mouseMotion[1]=int(e.y-utimaMotion[1])
    window.update()
    if rightP:
        game.cam2["hspeed"]=mouseMotion[0]*speed
        game.cam2["vspeed"]=mouseMotion[1]*speed
    if leftP:
        if selectObject==None:
            return
        if selectLayer==None:
            return
        i=0
        for j in setas:
            if j[0]+j[2]-game.cam2["x"]>=e.x and j[0]-game.cam2["x"]<e.x and j[1]+j[3]-game.cam2["y"]>=e.y and j[1]-game.cam2["y"]<e.y:
                l=game.getLayer(selectLayer)
                if l==None:
                    return
                if i==0 or i==1:
                    if sPress:
                        game.layers[l]["objs"][selectObject].transform.scale.x+=mouseMotion[0]*speed
                    else:
                        game.layers[l]["objs"][selectObject].transform.position.x+=mouseMotion[0]*speed
                    sceneED()
                elif i==2 or i==3:
                    if sPress:
                        game.layers[l]["objs"][selectObject].transform.scale.y+=mouseMotion[1]*speed
                    else:
                        game.layers[l]["objs"][selectObject].transform.position.y+=mouseMotion[1]*speed
                    sceneED()
                break
            i+=1
    utimaMotion[0]=e.x
    utimaMotion[1]=e.y
def loadLayers():
    layerEditorLB.delete(0,END)
    for i in range(len(game.layers)):
        layerEditorLB.insert(END,game.layers[i]["name"])
#init module sceneEditor
def SceneEditorWheel():
    game.cam2["x"]+=game.cam2["hspeed"]
    game.cam2["y"]+=game.cam2["vspeed"]
    SceneEditorCanvas.xview("scroll",game.cam2["hspeed"],"units")
    SceneEditorCanvas.yview("scroll",game.cam2["vspeed"],"units")
    #SceneEditorCanvas.xview_moveto(float(game.cam2["x"]))
    #SceneEditorCanvas.xview_moveto(float(50))
    #SceneEditorCanvas.yview_moveto(float(game.cam2["y"]))
    game.cam2["hspeed"]=0
    game.cam2["vspeed"]=0
    window.after(30,SceneEditorWheel)
rightP=False
leftP=False
def wb3(e):
    global rightP
    rightP=True
def wb3r(e):
    global rightP
    rightP=False
def wb1(e):
    global leftP
    leftP=True
def wb1r(e):
    global leftP
    leftP=False
def SECKP(e):
    global sPress,cPress,cc,selectObject
    if e.keycode==39:
        sPress=True
    elif e.keycode==37:
        cPress=True
    elif e.keycode==54:
        if cPress:
            l=game.getLayer(selectLayer)
            if l==None:
                return
            if selectObject==None:
                return
            ccc=game.layers[l]["objs"][selectObject]
            cc=ccc
            del ccc
    elif e.keycode==55:
        if cPress:
            if cc!=None:
                v=game.Instantiate(cc,Transform(Vector2(cc.transform.position.x,cc.transform.position.y),Vector2(cc.transform.scale.x,cc.transform.scale.y),int(cc.transform.rotation)),selectLayer)
                if v==0:
                    loadObject()
                    sceneED()
                    #selectObject=len(game.layers[game.getLayer(selectLayer)]["objs"])-1
                    #print(cc)
    elif e.keycode==119:
            deleteObj()
def SECKR(e):
    global sPress,cPress
    if e.keycode==39:
        sPress=False
    elif e.keycode==37:
        cPress=False
sPress=False
cPress=False
movePress=False
SceneEditorCanvas=Canvas(sceneEditor,background="#0ff")
SceneEditorCanvas.pack(fill="both",expand=True)
#end module
mainNb.add(sceneEditor,text="Scene Editor")
mainNb.add(calcF,text="Cauculadora")
SceneEditorCanvas.bind('<Motion>', Motion)
SceneEditorCanvas.bind("<Button-3>",wb3)
SceneEditorCanvas.bind("<Button-1>",wb1)
SceneEditorCanvas.bind("<ButtonRelease-3>",wb3r)
SceneEditorCanvas.bind("<ButtonRelease-1>",wb1r)
window.bind("<KeyPress>",SECKP)
window.bind("<KeyRelease>",SECKR)
SceneEditorCanvas["xscrollincrement"] = 1
SceneEditorCanvas["yscrollincrement"] = 1
def Start():
    Wheel()
    SceneEditorWheel()
    def func():
        window.after_cancel(after)
        window.destroy()
    window.protocol("WM_WINDOW_CLOSE",func)
    window.mainloop()
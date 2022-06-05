publics={"src":Image(),"draw in editor":False}
img=None
def loadImg():
    global img
    img=Loader.getImage(publics["src"])
    if img!=None:
        img.playAnim(0)
def Start():
    loadImg()
def Update():
    if img!=None:
        img.Update()
def Draw():
    if not inEditor:
        if img!=None:
            game.drawImage(transform,img)
    else:
        if publics["draw in editor"]:
            game.drawImage(transform,img)
        else:
            game.drawRectBorder(transform,(255,255,255),(0,0,0),5)

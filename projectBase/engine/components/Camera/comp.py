from turtle import pu


publics={"target layer":"","obj":0,"follow":False}
def updateCam():
    if publics["follow"]:
        l=game.getLayer(publics["target layer"])
        if l==None:
            return
        trans=game.layers[l]["objs"][publics["obj"]].transform
        transform.position.x=trans.position.x+(trans.scale.x/2)
        transform.position.y=trans.position.y+(trans.scale.y/2)
    game.cam["x"]=transform.position.x-(game.width/2)
    game.cam["y"]=transform.position.y-(game.height/2)
def Editor():
    updateCam()
def Update():
    updateCam()
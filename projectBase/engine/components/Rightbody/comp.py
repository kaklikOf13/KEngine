from copy import copy
publics={"gravityx":0.0,"gravityy":0.5,"comp":0,"collide layer":"walls","select comp":True,"hspeed":0.0,"vspeed":0.0}
vspeed,hspeed=0,0
def CollideInLayer(layer=""):
    l=game.getLayer(layer)
    objsC=[]
    if l!=None:
        objs=game.getLayerObjects(l)
        for i in range(len(objs)):
            objH=objs[i].getComponent("BoxCollision")
            if objH==None:
                continue
            tx=transform.position.x+gameObject.components[publics["comp"]]["publics"]["x"]
            ox=objs[i].transform.position.x+objs[i].components[objH]["publics"]["x"]
            ty=transform.position.y+gameObject.components[publics["comp"]]["publics"]["y"]
            oy=objs[i].transform.position.y+objs[i].components[objH]["publics"]["y"]
            if tx<=ox+objs[i].components[objH]["publics"]["width"] and tx+gameObject.components[publics["comp"]]["publics"]["width"]>=ox and ty<=oy+objs[i].components[objH]["publics"]["height"] and ty+gameObject.components[publics["comp"]]["publics"]["height"]>=oy:
                objsC.append(copy(game.layers[l]["objs"][i]))
    return objsC
def Start():
    global vspeed,hspeed
    if publics["select comp"]:
        pass
    else:
        publics["comp"]=gameObject.getComponent("BoxCollision")
    hspeed=publics["hspeed"]
    vspeed=publics["vspeed"]
def Update():
    global vspeed,hspeed
    hspeed+=publics["gravityx"]
    vspeed+=publics["gravityy"]
    transform.position.x+=hspeed
    transform.position.y+=vspeed
    if publics["collide layer"]!="":
        l=game.getLayer(publics["collide layer"])
        if l!=None:
            objs=game.getLayerObjects(l)
            for i in range(len(objs)):
                objH=objs[i].getComponent("BoxCollision")
                if objH==None:
                    continue
                distX=((transform.position.x+gameObject.components[publics["comp"]]["publics"]["x"])+gameObject.components[publics["comp"]]["publics"]["width"]/2)-((objs[i].transform.position.x+objs[i].components[objH]["publics"]["x"])+objs[i].components[objH]["publics"]["width"]/2)
                distY=((transform.position.y+gameObject.components[publics["comp"]]["publics"]["y"])+gameObject.components[publics["comp"]]["publics"]["height"]/2)-((objs[i].transform.position.y+objs[i].components[objH]["publics"]["y"])+objs[i].components[objH]["publics"]["height"]/2)
                sumWidth=(gameObject.components[publics["comp"]]["publics"]["width"]+objs[i].components[objH]["publics"]["width"])/2
                sumHeight=(gameObject.components[publics["comp"]]["publics"]["height"]+objs[i].components[objH]["publics"]["height"])/2
                if abs(distX)<sumWidth and abs(distY)<sumHeight:
                    overlapX=sumWidth-abs(distX)
                    overlapY=sumHeight-abs(distY)
                    if overlapX>overlapY:
                        transform.position.y=transform.position.y+overlapY if distY>0 else transform.position.y-overlapY
                        vspeed=0
                    else:
                        transform.position.x=transform.position.x+overlapX if distX>0 else transform.position.x-overlapX
                        hspeed=0

publics={"speed":5.0,"collide layer":"walls","gravity":1,"jump force":15.0,"comp":2}
hspeed=0
vspeed=0
okJump=True
def Update():
    global hspeed,vspeed,okJump
    vspeed+=publics["gravity"]
    if(Key.pressed(Key.code.d)):
        hspeed=publics["speed"]
        if transform.scale.x<0:
            transform.scale.x=-transform.scale.x
    elif(Key.pressed(Key.code.a)):
        hspeed=-publics["speed"]
        if transform.scale.x>0:
            transform.scale.x=-transform.scale.x
    if not Key.pressed(Key.code.a) and not Key.pressed(Key.code.d):
        hspeed=0
    if Key.pressed(Key.code.space):
        if okJump:
            vspeed-=publics["jump force"]
    transform.position.x+=hspeed
    transform.position.y+=vspeed
    ok=False
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
                        transform.position.y=transform.position.y+overlapY if distY>0 else transform.position.y-overlapY;ok=True;okJump=True
                        vspeed=0
                    else:
                        transform.position.x=transform.position.x+overlapX if distX>0 else transform.position.x-overlapX
                        hspeed=0
    if not ok:
        okJump=False
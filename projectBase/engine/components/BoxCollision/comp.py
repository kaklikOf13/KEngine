publics={"x":0,"y":0,"width":50,"height":50,"regulamento automatico":False}
def Regular():
    publics["width"]=transform.scale.x
    publics["height"]=transform.scale.x
def Start():
    if publics["regulamento automatico"]:
        Regular()
def Editor():
    if publics["regulamento automatico"]:
        Regular()
def Draw():
    if inEditor:
        game.drawRectBorder(Transform(Vector2(publics["x"]+transform.position.x,publics["y"]+transform.position.y),Vector2(publics["width"],publics["height"]),0),None,(0,255,0),5)

publics={
    "color":"#000",
    "center draw":False
}
def Draw():
    """if publics["center draw"]:
        game.drawCenterRect(transform,hex_to_rgb(publics["color"]))
    else:"""
    game.drawRect(transform,hex_to_rgb(publics["color"]))
from engine import KivyGame,Loader
g=Loader().getJson("project.kep")
game=KivyGame(g["width"],g["height"],g["components"],g["start scene"])
del g
game.Run()
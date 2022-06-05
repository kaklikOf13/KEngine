from engine import PygameGame,Loader
g=Loader().getJson("project.kep")
game=PygameGame(g["width"],g["height"],g["components"],g["background color"])
game.LoadScene(g["start scene"])
del g
game.Run()
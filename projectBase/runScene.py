from engine import PygameGame,Loader
from sys import argv
g=Loader().getJson("project.kep")
game=PygameGame(g["width"],g["height"],g["components"])
i2=0
for i in argv:
    if i=="-l":
        game.LoadScene(argv[i2+1])
        break
    i2+=1
game.Run()
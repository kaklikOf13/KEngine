class LineTypes:
    int="int"
    float="float"
    input="input"
    all="all"
class Block:
    def __init__(self) -> None:
        self.name=""
        self.ba=False
        self.input={"value":LineTypes.all}
        self.output={}
        self.re={}
    def reOutput(self,id,value):
        self.re.setdefault(id,value)
    def code(args):
        pass
class PrintBlock(Block):
    def __init__(self) -> None:
        Block.__init__(self)
        self.ba=True
    def code(args):
        print(args["value"])
def epb(code={}):
    

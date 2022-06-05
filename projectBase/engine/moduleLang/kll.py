#indev
class Token:
    def __init__(self,type,value=None) -> None:
        self.value=value
        self.type=type
    def __repr__(self) -> str:
        st=str(self.type)
        if self.value!=None:
            st+=":"+str(self.value)
        return st
class TokenType:
    string="str"
    int="int"
    float="float"
def Lexer(code):
    tok=""
    cc=0
    v=None
    tokens=[]
    while cc<len(code):
        if code[cc]==" ":
            cc+=1
            continue
        if code[cc]=="'":
            tok=""
            v=""
            while True:
                cc+=1
                if cc>=len(code):
                    break
                elif code[cc]=="'":
                    tokens.append(Token(TokenType.string,v))
                    v=None
                    break
                v+=code[cc]
        tok+=code[cc]
        cc+=1
    return tokens
t=Lexer("'aaaa'")
print(t)
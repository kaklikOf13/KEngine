from _thread import start_new_thread
publics={"ip":"localhost","port":8000,"maximum number of players":2}
server=None
def OnRecvMessage(conn,msg,id):
    conn.send(50+50)
def Wheel():
    pass
def thread():
    while game.isRun:
        server.update()
def initServer():
    global server,OnRecvMessage
    server=Server(publics["ip"],publics["port"],publics["maximum number of players"],OnRecvMessage)
    server.start()
    start_new_thread(thread,())
def OnEvent(e):
    if e=="QUIT":
        server.stop()
        exit(0)
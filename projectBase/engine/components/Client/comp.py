publics={"ip":"localhost","port":8000}
def connect():
    client=Client(publics["ip"],publics["port"])
    client.connect()
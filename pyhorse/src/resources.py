class Resources:
    __instance = None

    def __new__(cls):

        if Resources.__instance is None:
            total_s = 6
            Resources.__instance = object.__new__(cls)
            Resources.__instance.ipfile = "../res/ip.txt"
            Resources.__instance.ip = Resources.__instance.loadip()

        return Resources.__instance

    def loadip(self):
        f = open(Resources.__instance.ipfile, "r")
        ip = f.read().split("\n")
        f.close()
        return ip

    def saveip(self, text):
        f = open(Resources.__instance.ipfile, "w")
        f.write(text)
        f.close()

from os import system
ROWS=7
COLS=19


class DisplayManager:
    def __init__(self):
        pass
    
    def _volume(self):
        return "V  ========      ]"
    
    def _playing(self):
        return ">  Martha Reeves "
    
    def _artists(self):
        o = ""
        o += "   Artist 1\n"
        o += "   Artist 2\n"
        o += "*  Artist 3\n"
        o += "   Artist 4\n"
        o += "   Artist 5\n"
        return o
x=DisplayManager()

system('clear')
print("")
print(x._artists())
print(x._volume())

print("")

print(x._artists())
print(x._playing())

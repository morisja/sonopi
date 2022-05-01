class TextDisplay:
    def __init__(self, lines=9):
        self.n=0
        self.lines=lines
        self.x=0
        self.y=0
        self.s=0
        self.px=1
        self.py=1
    def get_buffer(self):
        out=[]
        for x in range(self.n, self.n+self.lines):
            p=str(x).zfill(3)
            out.append(f"{p}_abcdefghijklmno")
        self.n=self.n+1
        return out

    def get_sprite(self):
        xmax=19
        ymax=8
        out=[]
        
        for y in range(1,ymax):
            xrow=[]
            for x in range(1,xmax):
                if self.px == x and self.py==y:
                    print(f"{self.s} {x} {y}")
                    xrow.append("X")
                    self.px=x
                    self.py=y
                else:
                    xrow.append(" ")
            out.append("".join(xrow))
            x=0
        return out

x=TextDisplay()
for n in range(0, (18*9)):
    print("get")
    x.get_sprite()
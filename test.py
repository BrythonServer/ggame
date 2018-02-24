from ggmath import Timer, MathApp

def timehandler(t):
    print(id(t))

app = MathApp()
app.run()

t = Timer()
t.callEvery(0.02, timehandler)
    

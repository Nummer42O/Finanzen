from tkinter import *

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.state('zoomed')
        Frame(self,width=5).pack(side=LEFT,anchor=N)
        for i in range(7): Frame(self,width=100,height=30,bg='red').pack(side=LEFT,anchor=N,padx=(0,5))
        self.widget=None
        self.ghost=Frame(width=100)
        self.bind('<Button-1>',self.select)
        self.bind('<Button1-Motion>',self.drag)
        self.bind('<ButtonRelease-1>',self.drop)
    def select(self,event):
        if event.widget==self: return
        self.widget=widget=event.widget
        self.dx=event.x
        self.ghost.pack(after=widget,side=LEFT,anchor=N,padx=(0,5))
        widget.place(x=widget.winfo_x(),y=widget.winfo_y())
        widget.lift(self.ghost)
        widget.config(bg='green')
    def drag(self,event):
        if not self.widget: return
        newx=self.winfo_pointerx()-self.dx
        self.widget.place(x=newx)
        if newx>=self.ghost.winfo_x()+50:
            slaves=self.pack_slaves()
            try: self.ghost.pack(after=slaves[slaves.index(self.ghost)+1])
            except IndexError: return
        elif newx<self.ghost.winfo_x()-50:
            slaves=self.pack_slaves()[1:]
            try: self.ghost.pack(before=slaves[slaves.index(self.ghost)-1])
            except IndexError: return
    def drop(self,event):
        if not self.widget: return
        self.widget.pack(before=self.ghost,side=LEFT,anchor=N,padx=(0,5))
        self.widget.config(bg='red')
        self.ghost.pack_forget()
        self.widget=None

if __name__=='__main__': App().mainloop()
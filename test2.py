from tkinter import *
import random

bg='#ef6950'
r=10
d=2*r

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.state('zoomed')
        self.top=Frame(self,bg=bg)
        self.top.pack(side=TOP,fill=X)
        Frame(self.top,width=5,bg=bg).pack(side=LEFT,anchor=N)
        for i in range(7): self.create_new()
        self.widget=None
        self.focused.l.grid(row=0,column=0,sticky=NS+W)
        self.focused.r.grid(row=0,column=3,sticky=NS+E)
        self.changecolor('SystemButtonFace')
        self.ghost=Frame(self.top,bg=bg)
        self.bind('<Button-1>',self.select)
        self.bind('<Button1-Motion>',self.drag)
        self.bind('<ButtonRelease-1>',self.drop)
    def create_new(self):
        tab=Frame(self.top,bg=bg)
        tab.columnconfigure((0,3),uniform='roundings',weight=1,minsize=r/2)
        tab.columnconfigure(1,weight=1)
        tab.l=left=Canvas(tab,highlightthickness=0,width=d,height=1)
        tab.r=right=Canvas(tab,highlightthickness=0,width=d,height=1)
        Label(tab,text=f'Tab {random.randrange(10000)+1}',justify=LEFT,anchor=W,bg=bg).grid(row=0,column=1,sticky=NSEW)
        Button(tab,text='X',bg=bg,activebackground=bg,bd=0,command=lambda widget=tab: self.remove(widget)).grid(row=0,column=2,sticky=NSEW)
        tab.pack(side=LEFT)
        self.update()
        height=tab.winfo_height()
        left.create_arc(-r,height-d,r,height,width=0,fill=bg,outline=bg,start=-90) #bottom
        left.move(1,-1,0)
        left.create_polygon(0,0,d,0,d,r,r,r,r,height-r,0,height-r,width=0,fill=bg) #bg
        left.create_arc(r,0,r+d,d,width=0,fill='SystemButtonFace',outline='SystemButtonFace',start=90) #top
        right.create_arc(r,height-d,d+r,height,width=0,fill=bg,outline=bg,start=180) #bottom
        right.create_polygon(0,0,d,0,d,height-r,r,height-r,r,r,0,r,width=1,fill=bg) #bg
        right.create_arc(-r,0,r,d,width=0,fill='SystemButtonFace',outline='SystemButtonFace') #top
        right.move(3,-1,0)
        self.focused=tab
    def remove(self,tab):
        if self.focused==tab:
            all=self.top.pack_slaves()[1:]
            i=all.index(tab)
            if tab==all[-1]:
                try: focus=all[i-1]
                except IndexError: focus=self
            else: focus=all[i+1]
            self.focused=None
            self.select(Store(widget=focus,x_root=0))
            self.drop(None)
        tab.destroy()
    def changecolor(self,color):
        for child in self.focused.children.values():
            if not isinstance(child,Canvas): child.config(bg=color,activebackground=color)
        self.focused.config(bg=color)
    def select(self,event):
        if isinstance(event.widget,Button) or event.widget.master not in self.top.pack_slaves(): return
        else: self.widget=widget=event.widget.master
        if widget!=self.focused:
            if self.focused:
                self.focused.l.grid_forget()
                self.focused.r.grid_forget()
                self.changecolor(bg)
            self.focused=widget
            self.focused.l.grid(row=0,column=0,sticky=NS+W)
            self.focused.r.grid(row=0,column=3,sticky=NS+E)
            self.changecolor('SystemButtonFace')
            self.update()
        self.dx=event.x_root-widget.winfo_rootx()
        self.ghost.pack(after=widget,side=LEFT,anchor=N)
        width=self.widget.winfo_width()
        self.ghost.config(width=width)
        self.ghost.treshold=width//2
        widget.pack_forget()
        self.update()
        widget.place(x=self.ghost.winfo_x(),y=self.ghost.winfo_y())
        widget.lift()
    def drag(self,event):
        if not self.widget: return
        newx=self.winfo_pointerx()-self.dx
        if newx<5: newx=5
        self.widget.place(x=newx)
        if newx>=self.ghost.winfo_x()+self.ghost.treshold:
            slaves=self.top.pack_slaves()
            try: self.ghost.pack(after=slaves[slaves.index(self.ghost)+1])
            except IndexError: return
        elif newx<self.ghost.winfo_x()-self.ghost.treshold:
            slaves=self.top.pack_slaves()[1:]
            try: self.ghost.pack(before=slaves[slaves.index(self.ghost)-1])
            except IndexError: return
    def drop(self,event):
        if not self.widget: return
        self.widget.pack(before=self.ghost,side=LEFT,anchor=N)
        self.ghost.pack_forget()
        self.widget=None

if __name__=='__main__': App().mainloop()
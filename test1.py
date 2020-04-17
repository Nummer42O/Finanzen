from tkinter import *

bg='#ef6950'
r=10
d=2*r

t=Tk()
top=Frame(t,padx=10,bg=bg,height=40)
top.pack(side=TOP,fill=X)

def create_new():
    tab=Frame(top)
    tab.columnconfigure((0,3),uniform='roundings',weight=1,minsize=r/2)
    tab.columnconfigure(1,weight=1)
    tab.l=left=Canvas(tab,highlightthickness=0,width=d,height=1)
    #left.grid(row=0,column=0,sticky=NS+W)
    tab.r=right=Canvas(tab,highlightthickness=0,width=d,height=1)
    #right.grid(row=0,column=3,sticky=NS+E)
    Label(tab,text=f'Tab {len(top.pack_slaves())+1}',width=6,justify=LEFT,anchor=W).grid(row=0,column=1,sticky=NSEW)
    Label(tab,text='X').grid(row=0,column=2,sticky=NSEW)
    tab.pack(side=LEFT)

    t.update()

    height=tab.winfo_height()
    left.create_arc(-r,height-d,r,height,width=0,fill=bg,outline=bg,start=-90) #bottom
    left.move(1,-1,0)
    left.create_polygon(0,0,d,0,d,r,r,r,r,height-r,0,height-r,width=0,fill=bg) #bg
    left.create_arc(r,0,r+d,d,width=0,fill='SystemButtonFace',outline='SystemButtonFace',start=90) #top
    right.create_arc(r,height-d,d+r,height,width=0,fill=bg,outline=bg,start=180) #bottom
    right.create_polygon(0,0,d,0,d,height-r,r,height-r,r,r,0,r,width=1,fill=bg) #bg
    right.create_arc(-r,0,r,d,width=0,fill='SystemButtonFace',outline='SystemButtonFace') #top
    right.move(3,-1,0)
    t.focused=tab

def changecolor(color):
    for child in t.focused.children.values():
        if isinstance(child,Label): child.config(bg=color)
    t.focused.config(bg=color)

for i in range(5): create_new()

t.focused.l.grid(row=0,column=0,sticky=NS+W)
t.focused.r.grid(row=0,column=3,sticky=NS+E)

def changefocus(event):
    if event.widget==t: return
    elif event.widget!=t.focused:
        t.focused.l.grid_forget()
        t.focused.r.grid_forget()
        changecolor(bg)
        t.focused=event.widget.master if not event.widget.master==top else event.widget
        t.focused.l.grid(row=0,column=0,sticky=NS+W)
        t.focused.r.grid(row=0,column=3,sticky=NS+E)
        changecolor('SystemButtonFace')

t.bind('<Button-1>',changefocus)
t.bind('<Button1-Motion>',changefocus)

t.geometry('700x400')
t.mainloop()
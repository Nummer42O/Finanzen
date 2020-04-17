from extras import *

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.container=Frame(self,container=True)
        self.container.pack(fill=BOTH,expand=True,padx=10,pady=10)
        self.cid=self.container.winfo_id()

        self.toplevel=Toplevel(t,bg='red',use=self.cid)
        self.iswindow=False

        self.bind('<Button-1>',self.select)
        self.bind('<Button1-Motion>',self.drag)
        self.bind('<ButtonRelease-1>',self.drop)
    def select(self,event):

if __name__=='__main__':
    App().mainloop()
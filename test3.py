from extras import *

<<<<<<< HEAD
class App(Tk): #top height: 45
=======
class App(Tk):
>>>>>>> combined-tests
    def __init__(self):
        Tk.__init__(self)
        self.container=Frame(self,container=True)
        self.container.pack(fill=BOTH,expand=True,padx=10,pady=10)
        self.cid=self.container.winfo_id()

<<<<<<< HEAD
        self.toplevel=Toplevel(self,bg='red')
        self.update()
        self.x,self.y=self.toplevel.winfo_x(),self.toplevel.winfo_y()
        self.width=self.toplevel.winfo_width()
        self.dy=22
        self.toplevel.config(use=self.cid)
        self.iswindow=False
        self.dx=None
        self.update()
        self.update_idletasks()

        self.toplevel.bind('<Button-1>',self.select)
        self.toplevel.bind('<Button1-Motion>',self.drag)
        self.toplevel.bind('<ButtonRelease-1>',self.drop)
        self.toplevel.bind('<Configure>',self.adopt)
    def select(self,event):
        if not self.iswindow: self.dx=self.width//2
    def drag(self,event):
        if self.dx is not None and self.iswindow:
            self.toplevel.geometry('+{x}+{y}'.format(x=event.x_root-self.dx,y=event.y_root-self.dy))
        elif self.dx is not None and not pointer_over(self.container):
            self.iswindow=True
            self.toplevel.config(use='')
    def drop(self,event):
        if self.dx is not None: self.dx=None
    def adopt(self,event):
        if (event.x!=self.x or event.y!=self.y) and self.iswindow:
            if pointer_over(self.container) and self.iswindow:
                self.iswindow=False
                self.width=self.toplevel.winfo_width()
                self.toplevel.config(use=self.cid)
=======
        self.toplevel=Toplevel(t,bg='red',use=self.cid)
        self.iswindow=False

        self.bind('<Button-1>',self.select)
        self.bind('<Button1-Motion>',self.drag)
        self.bind('<ButtonRelease-1>',self.drop)
    def select(self,event):

>>>>>>> combined-tests
if __name__=='__main__':
    App().mainloop()
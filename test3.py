from extras import *

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.container=Frame(self,container=True)
        self.container.pack(fill=BOTH,expand=True,padx=10,pady=10)
        self.cid=self.container.winfo_id()

        self.toplevel=Toplevel(self,bg='red',use=self.cid)
        self.iswindow=False
        self.dx=None

        self.toplevel.bind('<Button-1>',self.select)
        self.toplevel.bind('<Button1-Motion>',self.drag)
        self.toplevel.bind('<ButtonRelease-1>',self.drop)
    def select(self,event):
        self.dx,self.dy=event.x,event.y
    def drag(self,event):
        if self.dx is not None:
            over=pointer_over(self.container)
            print(self.iswindow,over)
            if self.iswindow and over:
                self.iswindow=False
                self.toplevel.config(use=self.cid)
            elif self.iswindow:
                self.toplevel.geometry('+{x}+{y}'.format(x=event.x_root-self.dx,y=event.y_root-self.dy))
            elif not over:
                self.iswindow=True
                self.toplevel.config(use='')
                self.toplevel.geometry('{width}x{height}+{x}+{y}'.format(width=self.container.winfo_width(),height=self.container.winfo_height(),x=event.x_root-self.dx,y=event.y_root-self.dy))
    def drop(self,event):
        if self.dx is not None:
            self.dx=None
if __name__=='__main__':
    App().mainloop()
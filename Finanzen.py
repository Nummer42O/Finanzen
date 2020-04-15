#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter.messagebox import askyesnocancel,showerror,showwarning
from shutil import copy2 as copyfile
from datetime import datetime
from tkinter import *
from extras import *
import subprocess
import webbrowser
#from os import remove as delfile,rename as renfile,path
import sys
import os

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

argv=sys.argv.copy()
PATH=os.path.dirname(argv.pop(0))+'\\'

class App(Toplevel):
    def __init__(self,master,path,darkmode):

        Toplevel.__init__(self,master)
        self.title('Finanzen')
        self.iconbitmap(PATH+'ausgaben.ico')
        self.protocol('WM_DELETE_WINDOW',self.close)

        self.darkmode=darkmode
        self.filepath=path
        self.sum=0.0
        self.contents={}
        self.undoqueque=[]
        self.confirm=BooleanVar(self,True)
        self.changing=False
        self.catched=None

        self.bcnf={'ipadx': 2, 'ipady': 2, 'ratio': False, 'anchor': CENTER, 'movewidth': 2, 'bd': 2, 'highlightthickness': 0, 'height': 30, 'width': 30, 'bg': 'SystemButtonFace',
             'irelheight': .65, 'irelwidth': .65, 'relief': FLAT, 'activerelief': SUNKEN, 'color' : 'red', 'activecolor': 'red', 'form': CustomButton.CROSS}
        sbcnf={'elementborderwidth': 0, 'bd': 0, 'highlightthickness': 0}
        self.activebg='gainsboro'
        if self.darkmode:
            self.config(bg='#2d2d30')
            self.option_add('*Background','#2d2d30')
            self.option_add('*Foreground','#dcdcdc')
            self.option_add('*activeForeground','#dcdcdc')
            self.option_add('*activeBackground','#2d2d30')
            self.option_add('*Entry.Background','#333337')
            self.option_add('*Entry.disabledBackground','#333337')
            self.option_add('*Button.borderWidth',0)
            self.option_add('*Button.activeBackground','#2d2d30')
            self.bcnf.update({'activebackground': '#2d2d30', 'disabledcolor': '#656565', 'bg': '#2d2d30'})
            sbcnf.update({'activebackground': '#999999', 'troughcolor': '#3e3e42', 'bg': '#3e3e42', 'fg': '#999999', 'activeforeground': '#3e3e42',
                         'disabledforeground': '#8f8f8f', 'slidercolor': '#1e1e1e'})
            self.config(bg='#2d2d30')
            self.activebg='#3e3e40'

        self.about=Frame(self)
        self.about.destroy() #to create Tk Widget on self.about

        mainframe=Frame(self)
        mainframe.pack(side=BOTTOM,fill=BOTH,expand=True,padx=10,pady=10)
        mainframe.rowconfigure(1,weight=1)
        mainframe.columnconfigure(0,weight=1)
        
        topbg='#252526' if self.darkmode else 'gainsboro'
        top=Frame(mainframe,bg=topbg,padx=10,height=40)
        top.columnconfigure(0,weight=1)
        top.columnconfigure(1,minsize=97)
        top.columnconfigure(2,minsize=79)
        top.columnconfigure(3,minsize=94)
        top.columnconfigure(4,minsize=35)
        Label(top,text='Zahlungsempfänger/-sender:',bg=topbg).grid(row=0,column=0,sticky=W)
        Label(top,text='Gesamt: ',bg=topbg).grid(row=0,column=2,sticky=EW)
        self.sum_label=Label(top,text='0.00€',bg=topbg)
        self.sum_label.grid(row=0,column=3,sticky=EW)
        top.grid(row=0,column=0,sticky=EW)

        easteregg=Frame(mainframe)
        easteregg.grid(row=0,column=1,sticky=NSEW)
        InfoBox(easteregg,'Ich bin gaaaaaaanz bestimmt kein Easteregg. :3 ^^',fg='black')

        self.main=hvFrame(mainframe,sticky=EW,bg='#333337' if self.darkmode else 'white',bd=1,relief=SUNKEN,padx=10)
        self.main.grid(row=1,column=0,sticky=NSEW,pady=5)
        MouseMove(self,self.main.yview,over=self.main,sleep=500,scrollfactor=1/5)
        Frame(self.main.mf,height=5).pack() #5 pixel spacer
        sb=CustomScrollbar(mainframe,sbcnf,command=self.main.yview)
        sb.grid(row=1,column=1,sticky=NSEW,pady=5)
        self.main.config(yscrollcommand=sb.set)

        bottom=Frame(mainframe,padx=10)
        bottom.columnconfigure(0,weight=1)
        bottom.columnconfigure(1,minsize=97)
        bottom.columnconfigure(2,minsize=208)
        self.src=dtEntry(bottom,text='Zahlungsempfänger/-sender',color='#aaaaaa' if self.darkmode else '#555555',justify=CENTER)
        self.src.grid(row=0,column=0,sticky=NSEW)
        self.earning=BooleanVar(self,False)
        Checkbutton(bottom,text='Einnahme',var=self.earning).grid(row=0,column=1,sticky=NSEW,padx=5)
        self.value=dtEntry(bottom,text='Betrag',color='#aaaaaa' if self.darkmode else '#555555',justify=CENTER)
        self.value.grid(row=0,column=2,sticky=NSEW)
        InfoBox(self.value,'Eingabe mit "," und "." möglich.\nEin Eurozeichen (€) ist nicht drigend nötig.',fg='black',justify=LEFT)
        bottom.grid(row=2,column=0,sticky=EW)
        Button(mainframe,text='Ok',command=self.append).grid(row=2,column=1,sticky=NSEW)

        self.menu=Menu(self,tearoff=False)
        self.menu.add_command(label='Typ ändern',command=self.change_type,accelerator='Strg+Tab',)
        self.menu.add_command(label='Absender/Empfänger ändern',command=self.change_src,accelerator='Alt+1')
        self.menu.add_command(label='Betrag ändern',command=self.change_value,accelerator='Alt+2')
        self.menu.add_separator()
        self.menu.add_command(label='Eintrag löschen',command=self.remove,accelerator='Entf')

        change_theme = lambda event: self.restart(not self.darkmode,self.filepath)

        menucnf={'bg':'#3c3c3f' if self.darkmode else 'white'}
        menubar=Frame(self,menucnf)
        file_button=Menubutton(menubar,menucnf,text='Datei')
        file_button.pack(side=LEFT,fill=Y)
        file=Menu(file_button,tearoff=False)
        file.add_command(label='Öffnen',command=self.openfile,accelerator='Strg+O')
        file.add_command(label='In neuem\nFenster öffnen',command=self.opennewfile,accelerator='Strg+Umschalt+O')
        file.add_separator()
        file.add_command(label='Speichern',command=self.save,accelerator='Strg+S')
        file.add_command(label='Speichern unter',command=self.save_as,accelerator='Strg+Umschalt+S')
        file.add_separator()
        file.add_command(label='Schließen',command=self.close,accelerator='Alt+F4')
        file_button.config(menu=file)
        config_button=Menubutton(menubar,menucnf,text='Bearbeiten')
        config_button.pack(side=LEFT,fill=Y)
        config=Menu(config_button,tearoff=False,postcommand=self.postcommand)
        config.add_command(label='Undo',command=self.undo,accelerator='Strg+Z')
        config.add_separator()
        config.add_command(label='Quelle ändern',command=self.change_src,accelerator="Alt-1")
        config.add_command(label='Wert ändern',command=self.change_value,accelerator="Alt-2")
        config.add_command(label='Typ ändern',command=self.change_type,accelerator="Strg+Tab")
        config.add_separator()
        config.add_command(label='Theme ändern',command=change_theme,accelerator="Strg+T")
        config_button.config(menu=config)
        self.about_button=Button(menubar,menucnf,text='Über',command=self.display_about,bd=0,activebackground=menucnf['bg'])
        self.about_button.bind('<Enter>',Callback(self.about_button.config,{'bg':'#2d2d30' if self.darkmode else 'SystemButtonFace'}))
        self.about_button.bind('<Leave>',Callback(self.about_button.config,{'bg':menucnf['bg']}))
        self.about_button.pack(side=LEFT,fill=Y)
        menubar.pack(side=TOP,fill=X)

        self.bind('<Button-1>',self.click_left)
        self.bind('<Button-3>',self.click_right)
        self.bind('<Control-Tab>',self.change_type)
        self.bind('<Alt-Key-1>',self.change_src)
        self.bind('<Alt-Key-2>',self.change_value)
        self.bind('<Delete>',self.remove)
        self.bind('<Control-z>',self.undo)
        self.bind('<Control-t>',change_theme)
        self.src.bind('<Return>',self.append)
        self.value.bind('<Return>',self.append)
        self.bind('<MouseWheel>',self.main.yview)

        self.bind('<Control-s>',self.save)
        self.bind('<Control-S>',self.save_as)
        self.bind('<Control-o>',self.openfile)
        self.bind('<Control-O>',self.opennewfile)
        
        self.minsize(672,645)

        #self.bind('<x>',lambda e: print(self.geometry()))

        self.open()
    def append(self,*args,do_sum=True):
        if args and not isinstance(args[0],Event): src,value,istaking=args
        else:
            src=self.src.get()
            self.src.delete(0,END)
            if not src:
                showerror('Error','Kein Zahlungsempfänger/-sender festgelegt.')
                self.src.focus()
                return
            try: value=abs(float(self.value.get().replace(',','.').replace('€','')))
            except ValueError:
                self.value.delete(0,END)
                showerror('Error','Eingegebener Wert ist invalid.')
                self.value.focus()
                return
            if not value:
                self.value.delete(0,END)
                showerror('Error','Kein Wert festgelegt.')
                self.value.focus()
                return
            self.value.delete(0,END)
            istaking=1 if self.earning.get() else -1
            self.earning.set(False)
        if do_sum:
            self.sum+=istaking*value
            self.sum_label.config(text=self.format())
        support=Frame(self.main.mf,padx=2,pady=2,highlightthickness=3,highlightcolor='#007acc',highlightbackground=self.bcnf['bg'],takefocus=True)
        support.columnconfigure(0,weight=1)
        support.columnconfigure(1,minsize=97)
        support.columnconfigure(2,minsize=173)
        support.columnconfigure(3,minsize=35)
        support.src=Label(support,text=src,anchor=W)
        support.src.grid(row=0,column=0,sticky=EW)
        support.src.bind('<Configure>',lambda event: support.src.config(wraplength=support.src.winfo_width()-10))
        if istaking>0: support.earning=Label(support,text='Einnahme',bg='#8bff8c',fg='#740073',padx=3)
        else: support.earning=Label(support,text='Ausgabe',bg='#ff474c',fg='#00b8b3')
        support.earning.grid(row=0,column=1,sticky=EW,padx=5)
        support.value=Label(support,text=self.format(value))
        support.value.grid(row=0,column=2,sticky=E)
        btn=CustomButton(support,self.bcnf,command=self.remove,args=(support,))
        btn.grid(row=0,column=3,padx=(5,0))
        btn.bind('<Enter>',Callback(btn.config,kwargs={'bg':self.activebg}))
        btn.bind('<Leave>',Callback(btn.config,kwargs={'bg':self.bcnf['bg']}))
        self.contents[support]=[src,value,istaking]
        support.pack(fill=X,pady=(0,5))
        self.main._adopt()
    def remove(self,input=None,reset=True):
        self.menu.unpost()
        if isinstance(input,Event) or not input: input=self.focus_get()
        if input in (self,self.src,self.value): return
        input.destroy()
        content=self.contents.pop(input)
        if reset:
            self.sum-=content[2]*content[1]
            self.sum_label.config(text=self.format())
            self.undoqueque.append(Callback(self.append,content))
        self.update()
        self.main.update()
        self.main._adopt()
    def click_left(self,event):
        if isinstance(event.widget,str): return
        if event.widget in self.contents:
            event.widget.focus()
            self.menu.entryconfig(0,state=NORMAL)
            self.menu.entryconfig(1,state=NORMAL)
            self.menu.entryconfig(2,state=NORMAL)
            self.menu.entryconfig(4,state=NORMAL)
        elif event.widget.master in self.contents:
            event.widget.master.focus()
            self.menu.entryconfig(0,state=NORMAL)
            self.menu.entryconfig(1,state=NORMAL)
            self.menu.entryconfig(2,state=NORMAL)
            self.menu.entryconfig(4,state=NORMAL)
        elif isinstance(event.widget,dtEntry):
            event.widget.focus()
            self.menu.entryconfig(0,state=DISABLED)
            self.menu.entryconfig(1,state=DISABLED)
            self.menu.entryconfig(2,state=DISABLED)
            self.menu.entryconfig(4,state=DISABLED)
        else:
            self.focus()
            self.menu.entryconfig(0,state=DISABLED)
            self.menu.entryconfig(1,state=DISABLED)
            self.menu.entryconfig(2,state=DISABLED)
            self.menu.entryconfig(4,state=DISABLED)
    def click_right(self,event):
        self.click_left(event)
        if self.main in masterhistory(event.widget): self.menu.post(event.x_root,event.y_root)
    def change_type(self,event=None):
        if self.catched:
            widget=self.catched
            self.catched=None
        else: widget=self.focus_get()
        if widget in (self,self.src,self.value):
            self.bell()
            return
        value,type=self.contents[widget][1:]
        if type>0:
            widget.earning.config(text='Ausgabe',bg='#ff474c',fg='#00b8b3')
            self.contents[widget][2]=-1
            self.sum+=-2*value
        else:
            widget.earning.config(text='Einnahme',bg='#8bff8c',fg='#740073')
            self.contents[widget][2]=1
            self.sum+=2*value
        self.sum_label.config(text=self.format())
        widget.focus()
        return 'break' #for the event case
    def change_src(self,event=None):
        self.menu.unpost()
        if self.catched:
            widget=self.catched
            self.catched=None
        else: widget=self.focus_get()
        if widget in (self,self.src,self.value):
            self.bell()
            return
        if not self.changing:
            self.changing=True
            widget.config(highlightbackground='#007acc')
            widget.src.grid_forget()
            newsrc=dEntry(widget)
            newsrc.grid(row=0,column=0,sticky=EW,padx=(0,5))
            newsrc.focus()
            newsrc.bind('<Return>',self.confirm_input)
            newsrc.bind('<FocusOut>',self.confirm_input)
            newsrc.bind('<Escape>',self.confirm_input)
            newsrc.wait_variable(self.confirm)
            text=newsrc.get()
            newsrc.destroy()
            if text:
                widget.src.config(text=text)
                self.contents[widget][0]=text
            widget.src.grid(row=0,column=0,sticky=EW)
            widget.config(highlightbackground=self.bcnf['bg'])
            widget.focus()
            self.changing=False
    def change_value(self,event=None):
        self.menu.unpost()
        if self.catched:
            widget=self.catched
            self.catched=None
        else: widget=self.focus_get()
        if widget in (self,self.src,self.value):
            self.bell()
            return
        if not self.changing:
            self.changing=True
            widget.config(highlightbackground='#007acc')
            widget.value.grid_forget()
            newval=dEntry(widget,width=10)
            newval.grid(row=0,column=2,sticky=E,padx=(5,0))
            newval.focus()
            newval.bind('<Return>',self.confirm_input)
            newval.bind('<FocusOut>',self.confirm_input)
            newval.bind('<Escape>',self.confirm_input)
            newval.wait_variable(self.confirm)
            try: text=abs(float(newval.get().replace(',','.').replace('€','')))
            except ValueError: text=0
            newval.destroy()
            if text>0:
                widget.value.config(text=self.format(text))
                self.sum-=self.contents[widget][2]*(self.contents[widget][1]-text)
                self.contents[widget][1]=text
                self.sum_label.config(text=self.format())
            widget.value.grid(row=0,column=2,sticky=E)
            widget.config(highlightbackground=self.bcnf['bg'])
            widget.focus()
            self.changing=False
    def confirm_input(self,event):
        self.confirm.set(True)
    def undo(self,event=None):
        try: self.undoqueque.pop()()
        except IndexError: self.bell()
    def load(self,values):
        for widget in self.contents: self.remove(widget,False)
        for inst,val,istaking in values: self.append(inst,float(val.replace('€','')),1 if istaking=='Einnahme' else -1,do_sum=False)
        self.sum_label.config(text=self.format())
    def open(self,path=None):
        if path: self.filepath=path
        try:
            with open(self.filepath,mode='r',encoding='utf-8-sig') as file: data=file.read()
            data=data.split('\n')
            try: self.sum=float(data[-1][9:-1])
            except Exception as error:
                showerror('Error',f'Wrong or corrupted file: {self.filepath}\nError message: {error}')
                self.title('Finanzen')
                #self.debug+='\n  {now.hour}:{now.minute}:{now.second} - Error in open (sum):\n\tfile: {fp}\n\tdata: {d}\n\terror: {err}'.format(now=datetime.now(),fp=self.filepath,d=data[-1],err=str(error))
                self.filepath=''
                return
            values=[]
            for line in data[:-1]:
                try: values.append(line.split(';'))
                except Exception as error:
                    showerror('Error',f'Wrong or corrupted file: {self.filepath}\nError message: {error}')
                    self.title('Finanzen')
                    #self.debug+='\n  {now.hour}:{now.minute}:{now.second} - Error in open (entries):\n\tfile: {fp}\n\tdata: {d}\n\terror: {err}'.format(now=datetime.now(),fp=self.filepath,d=data[:-1],err=str(error))
                    self.filepath=''
                    return
            self.title(f'Finanzen - {self.filepath}')
            self.load(values)
        except FileNotFoundError:
            open(self.filepath,'w',encoding='utf-8-sig').close()
            self.title(f'Finanzen - {self.filepath}')
            self.sum=0.0
            self.load(())
    def openfile(self,event=None):
        inidir,inifile=os.path.split(self.filepath)
        path=askopenfilename(parent=self,initialdir=inidir,initialfile=inifile,filetypes=[('CSV-Datei','*.csv'),('Alle Dateien','*.*')],defaultextension='csv')
        if path:
            self.save()
            self.open(path)
    def opennewfile(self,event=None):
        inidir,inifile=os.path.split(self.filepath)
        path=askopenfilename(parent=self,initialdir=inidir,initialfile=inifile,filetypes=[('CSV-Datei','*.csv'),('Alle Dateien','*.*')],defaultextension='csv')
        if path: self.opennew(path)
    def save_as(self,event=None):
        inidir,inifile=os.path.split(self.filepath)
        path=asksaveasfilename(parent=self,initialdir=inidir,initialfile=inifile,filetypes=[('CSV-Datei','*.csv'),('Alle Dateien','*.*')],defaultextension='csv')
        if path: self.save(path=path)
    def save(self,event=None,path=None):
        if path: filepath=path
        else: filepath=self.filepath
        data=''
        for inst,val,istaking in self.contents.values(): data+=inst+';'+self.format(val)+(';Einnahme\n' if istaking>0 else ';Ausgabe\n')
        data+=';;Summe: '+self.format()
        tempfile=PATH+'tempcopy.csv'
        try: copyfile(filepath,tempfile)
        except FileNotFoundError:
            open(filepath,mode='x',encoding='utf-8-sig').close()
            copyfile(filepath,tempfile)
        with open(filepath,mode='w+',encoding='utf-8-sig') as file: file.write(data)
        with open(filepath,mode='r',encoding='utf-8-sig') as file: txt=file.read()
        if txt=='' or txt=='\n':
            copyfile(tempfile,filepath)
            showerror('Error','Datei konnte nicht korrekt gespeichert werden.')
            #self.debug+='\n {now.hour}:{now.minute}:{now.second} - Error in save:\n\tfile: {fp}\n\terror causing data: {d}'.format(now=datetime.now(),fp=filepath,d=data)
        os.remove(tempfile)
    def close(self):
        self.save()
        with open(PATH+'Finanzen.config','w') as file: file.write(str(self.darkmode))
        self.finalize(self)
    def format(self,price=None):
        if not price: price=self.sum
        val=str(round(price,2))
        return val+('€' if len(val.split('.')[1])==2 else '0€')
    def display_about(self):
        if self.about.winfo_exists(): self.about.destroy()
        else:
            self.about=Toplevel(self,padx=10,pady=10)
            self.about.attributes('-toolwindow',True)
            self.about.geometry('458x248')
            self.about.resizable(False,False)
            self.about.title('Über')
            self.about.columnconfigure(1,weight=1)
            Label(self.about,text='Author:',padx=4).grid(row=0,column=0,sticky=NW)
            Label(self.about,text='Johannes Kohl',padx=4,anchor=W).grid(row=0,column=1,sticky=EW)
            Label(self.about,text='Kontakt:',padx=4).grid(row=1,column=0,sticky=NW)
            support=Frame(self.about)
            support.pack_propagate(False)
            support.grid(row=1,column=1,sticky=NSEW)
            mail=Text(support,bd=0,bg='#2d2d30' if self.darkmode else 'SystemButtonFace',font='TkDefaultFont')
            hyperlinkmanager=HyperlinkManager(mail,foreground='#25a7d2' if self.darkmode else 'blue')
            mail.insert(0.0,'kohl.johannes.2k1@gmail.com',hyperlinkmanager.add(Callback(webbrowser.open_new_tab,('mailto:kohl.johannes.2k1@gmail.com',))))
            mail.grid_propagate(True)
            mail.pack(fill=BOTH,expand=True,padx=4)
            Label(self.about,text='Version:',padx=4).grid(row=2,column=0,sticky=NW)
            Label(self.about,text='2.irgendwas',padx=4,anchor=W).grid(row=2,column=1,sticky=EW)
            Label(self.about,text='Copyright:',padx=4).grid(row=3,column=0,sticky=NW)
            Label(self.about,text=' - ',padx=4,anchor=W).grid(row=3,column=1,sticky=EW)
            Label(self.about,text='Achtung:',padx=4).grid(row=4,column=0,sticky=NW)
            warning=Label(self.about,text='Dies ist ein Projekt auf Basis einer Open-Source-Programmiersprache. Von kommerziellem Vertrieb ist abzusehen, da dieser rechtlich geahndet werden kann.',padx=4,anchor=W,justify=LEFT)
            warning.bind('<Configure>',lambda event: warning.config(wraplength=warning.winfo_width()-8))
            warning.grid(row=4,column=1,sticky=EW)
            Button(self.about,text='Ok',command=self.about.destroy).grid(row=4,column=0,sticky=SW,padx=(5,0),pady=(0,5))

            callback=Callback(self.about.destroy)
            self.about.bind('<Escape>',callback)
            self.about.bind('<FocusOut>',callback)

            self.about.geometry('+%i+%i'%(self.winfo_rootx()+(self.winfo_width()-458)//2,
                                          self.winfo_rooty()+(self.winfo_height()-248)//2))
            self.about.focus()
    def postcommand(self):
        self.catched=self.focus_get()

class AppWrapper(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.iconbitmap(PATH+'ausgaben.ico')
        self.state('withdrawn')
        with open(PATH+'Finanzen.config','r') as file: self.darkmode=eval(file.read())
        if '-D' in argv:
            self.darkmode=True
            argv.remove('-D')
        elif '--darkmode' in argv:
            self.darkmode=True
            argv.remove('-darkmode')
        elif '-L' in argv:
            self.darkmode=False
            argv.remove('-L')
        elif '--lightmode' in argv:
            self.darkmode=False
            argv.remove('-lightmode')
        self.subwidgets=[]
        App.finalize,App.restart,App.opennew=self.remove,self.restart,self.opennew
        if argv:
            for path in argv.copy():
                if not (os.path.isfile(path) and path.endswith('.csv')): continue
                else: path=path.replace('\\','/')
                self.opennew(path)
                argv.remove(path)
            if argv: showwarning('Achtung!',f'{len(argv)} Pfade konnten nicht aufgelöst werden:\n'+'\n - '.join(argv))
        else:
            self.opennew(PATH+'files\\file-{now.month}-{now.year}.csv'.format(now=datetime.now()))
        self.subwidgets[0].focus_force()
        self.mainloop()
    def remove(self,subwidget):
        self.subwidgets.remove(subwidget)
        subwidget.destroy()
        if not self.subwidgets: self.destroy()
    def restart(self,darkmode,firstpath):
        paths=[subwidget.filepath for subwidget in self.subwidgets if subwidget.filepath!=firstpath]
        command=[sys.argv[0],'-D' if darkmode else '-L',firstpath]+paths
        subprocess.Popen(command)
        for subwidget in self.subwidgets.copy(): subwidget.close()
    def opennew(self,path):
        subwidget=App(self,path,self.darkmode)
        self.subwidgets.append(subwidget)


if __name__=='__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print('usage:',os.path.basename(sys.argv[0]),'[options]','...')
        print('Options:')
        print(' -D --darkmode  Activate darkmode and override settings.')
        print(' -L --lightmode Activate darkmode and override settings.')
        print(' -h --help      Show this information page.')
    else: AppWrapper()
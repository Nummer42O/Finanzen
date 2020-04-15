#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter.messagebox import askyesnocancel,showerror,showwarning
from tkinter.filedialog import askopenfilename,asksaveasfilename
from shutil import copy2 as copyfile
from datetime import datetime
from tkinter.ttk import *
#from tkinter import *
from extras import *
import subprocess
#import webbrowser
import sys
import os

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

PATH=os.path.dirname(sys.argv[0])+'/'

class App(Tk):
    def __init__(self): #needs coloring #needs menu
        '''Create main window and initialize necessary variables'''
        Tk.__init__(self)

    def close(self):
        '''Close window and save file(s).'''
    #----------------------------------------------------------------------------------------------
    def append(self,src: str,cat: str,type: int,value: float):
        '''Append one item to the current tabs table.
        
        @src: from/to
        @cat: categorie
        @type: in/out
        @value: transferred ammount'''
    def remove(self,widget: Frame):
        '''Remove one item from current tabs table
        
        @widget: widget on wich postcommand was called'''
    def load(self,values: tuple):
        '''Load all values from file into current tab.\nCheck if given sums equals newly calculated sum else show warning.
        
        @values: all values from the opened file'''
    def ok_wrapper(self,event: Event =None):
        '''Check if inputted values for new obj are valid or not.
        
        @event: buffer for tkinter Events that may be given trough event binding'''
    #--------------------------------------------
    def open(self,event: Event =None):
        '''Open new/recent file\nWill even create a new file upon first usage in a new month.
        
        @event: buffer for tkinter Events that may be given trough event binding'''
    def new(self,values: tuple):
        '''Create new tab, initalize new table, etc.
        
        @values: all values from the opened file to pass to load'''
    #--------------------------------------------
    def save(self,event: Event =None,path=''):
        '''Save current file on original path or given path.
        
        @event: buffer for tkinter Events that may be given trough event binding
        @path: alternative path to original for current file'''
    def save_as(self,event: Event =None):
        '''Save current file under new filename at a possibly new location.
        
        @event: buffer for tkinter Events that may be given trough event binding'''
    def save_all(self,event: Event =None):
        '''Save all opened files on their last defined paths.
        
        @event: buffer for tkinter Events that may be given trough event binding'''
    #----------------------------------------------------------------------------------------------
    def undo(self,event: Event =None):
        '''Undo previous events.
        
        Handles: removal, editing of objs
        @event: buffer for tkinter Events that may be given trough event binding'''
    def redo(self,event: Event =None):
        '''redo undone events.
        
        Handles: removal, editing of objs
        @event: buffer for tkinter Events that may be given trough event binding'''
    #----------------------------------------------------------------------------------------------
    def postcommand(self,widget: Frame):
        '''Post menu on widget wich should get configured.
        
        @widget: widget on wich postcommand is getting called'''
    def make_changeable(self,widget: Frame):
        '''Change widgets appearence so it can be edited completely.
        
        @widget: widget on wich postcommand was called'''
    def save_changes(self,widget: Frame):
        '''Save all changes made to widget and change its appearenc to make it ineditable.
        
        @widget: widget on wich postcommand was called'''
    #----------------------------------------------------------------------------------------------
    def switch_tab(self,event: Event =None):
        '''Change current working tab and all according variables.
        
        @event: buffer for tkinter Events that may be given trough event binding'''
    def settings(self,event: Event =None):
        '''Create settings window.
        
        @event: buffer for tkinter Events that may be given trough event binding'''
    #def about(self,event: Event =None):
    #    '''Create about window.
    #    
    #    @event: buffer for tkinter Events that may be given trough event binding'''
    @classmethod
    def format(cls,value: float) -> str:
        '''Format value to string in a visual pleasing money (€) value.
        
        @value: ammount of money'''

if __name__=='__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print('usage:',os.path.basename(sys.argv[0]),'[options]','...')
        print('Options:')
        print(' -D --darkmode  Activate darkmode and override settings.')
        print(' -L --lightmode Activate darkmode and override settings.')
        print(' -h --help      Show this information page.')
    else: App()
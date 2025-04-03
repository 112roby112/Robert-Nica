####################################################################################################################################
# CONFIGURATION ATTRIBUTES UPDATER
#
# WHAT: 
# - This tool is reading all the existing attributes from a TPT file, then, when you have a new release and need to change some attributes.
# - The script will update them on all platforms.
# 
# WHY: 
# - Each user has to update each attribute manually, by row, for all platforms...saves a lot of time/effort 
# 
# AUTHOR:
# - Andrei Dragoi/Robert Nica/Falamas Ovidiu
# 
# INPUT:
# - TPT file 
# 
# OUTPUT:
# - An updated TPT file with new attributes
###################################################################################################################################

import re
import string 
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from xml.dom import minidom
from tkinter.messagebox import showerror
import xml.etree.ElementTree as ET
from tkinter.filedialog import askopenfilename
import stat
import os
from interface import *
from xml.etree import ElementTree
from xml.etree.ElementTree import tostring

tpt_path = tk.StringVar()
tpt_file = ''

class Tab3():
    
    def __init__(self, tab):

        #color of background labels    
        fg_col = "#291b47"
        bg_col = "#fcfcfc"
        bt_col = "#f6f6f6"
        gold_color = "#f05e53"

        #set margin right (in all scripts use these lines)
        self.lable0 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable0.grid(row=0, column=4, padx=100)  

        # set margin left (in all scripts use these lines)
        self.lable1 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable1.grid(row=0, column=0, padx=80)

        self.lable2 = tk.Label(tab, cursor="hand2", text="Execution Attributes Updater", fg = fg_col, font = "Calibri 18 bold", bg = bg_col)
        self.lable2.bind ('<1>', lambda self: bt3_msgbox())
        self.lable2.grid(row=1, column=2)

        self.lable3 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable3.grid(row=2, column=0, pady=10)

        self.btn_open = Button(tab, text="Open TPT file", activebackground=gold_color, width=25, height=2, command=self.open_attributes, bg = bt_col)
        self.btn_open.grid(row=3, column=2, sticky=W)

        self.update_attrib = Button(tab,state=DISABLED ,text='Update Attributes', activebackground=bt_col, command = self.update_attributes, width=25, height=2, bg = bt_col)
        self.update_attrib.grid(row=3, column=2, sticky=E)

        self.lable4 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable4.grid(row=4, column=0)

        self.lableTPT = tk.Label(tab, text = "TPT path:  ", bg = bg_col)
        self.lableTPT.grid(row=5, column=1)

        self.labletpt = tk.Entry(tab, textvariable=tpt_path, width="75")
        self.labletpt.grid(row=5, column=2)

        self.lable5 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable5.grid(row=6, column=0)

    def update_attributes(self):
    
        tpt_file = tpt_path.get()

        if not os.path.isfile(tpt_file):
            showerror("ALERT","The TPT file does not exist !")
            return 0

        if '.tpt' not in tpt_file:
            showerror("ALERT","First, please select a TPT file !")
            return 0
        try:
            os.chmod(tpt_file, stat.S_IWRITE )
            element = ElementTree.parse(tpt_file)
            xml = element.getroot()

            value_text = []
            key_text = []

            # valorile acestor 2 variabile trebuie sa fie valoarea count din functia tb3_open_attributes - 1
            count_value = 6
            count_key = 6
            for attrb in tab3.children:
                if 'label' in attrb:
                    count_value = count_value + 1
                    try:
                        exec('text_value = value{}.get()'.format(count_value)) 
                        exec('value_text.append(text_value)')
                    except:
                        continue
                elif 'entry' in attrb:
                    count_key = count_key + 1
                    try:
                        exec('text_key = key{}.get()'.format(count_key)) 
                        exec('key_text.append(text_key)')
                    except:
                        continue

            dictionary = dict(zip(key_text, value_text))

            for elem in xml.iter('execconfigattr'):
                elem.set('value', dictionary.get(elem.get('key')))

            tree = ET.ElementTree(xml)
            tree.write(tpt_file,encoding="UTF-8",xml_declaration=True)
            
            messagebox.showinfo("Info","DONE! The attributes were updated.")
        
            self.btn_openExp.config(state=ACTIVE)

        except Exception as e:
            messagebox.showerror('Error',e)
            
    def open_attributes(self):

        global tpt_file
        
        try:

            tpt_file = askopenfilename(title = "Select TPT file", filetypes=[("TPT file","*.tpt")]) 
            
        except NameError:
            messagebox.showerror("NameError","No TPT file was found")
        except FileNotFoundError:
            messagebox.showerror("FileNotFoundError","No TPT file was selected")
        except:
            messagebox.showerror("Unexpected error:", sys.exc_info()[0])

        try:
            if os.path.isfile(tpt_file):
                mydoc = minidom.parse(tpt_file)
                execonfig = mydoc.getElementsByTagName('execconfigattr')
            else:
                return None

            lista_key=[]
            count = 7
      
            for elem in execonfig:
                elem_key = elem.attributes['key'].value
                
                if elem_key in lista_key:
                    continue

                lista_key.append(elem_key.strip())

                globals()['key%d'%count] = StringVar()
                exec('Label(tab3, textvariable=key{}, bg = "#fcfcfc").grid(row={}, column=2, sticky=W, padx=30)'.format(count,count+1))
                exec("key{}.set('{}')".format(int(count),str(elem_key)))

                elem_value = elem.attributes['value'].value
                globals()['value%d'%count] = StringVar()
                exec('Entry(tab3, textvariable=value{}, width='"45"').grid(row={}, column=2, sticky=E, padx=30)'.format(count,count+1))
                elem_value = elem_value.replace('"',"'")
                exec('value{}.set("{}")'.format(count,elem_value))
                count = count + 1

            tpt_path.set(tpt_file)

            self.update_attrib.config(state=ACTIVE)

            self.lable19 = tk.Label(tab3, text = "      ", bg = "#fcfcfc")
            self.lable19.grid(row=19, column=0)

            self.btn_openExp = Button(tab3, text="Open TPT file", state = DISABLED, activebackground="#f6f6f6", width=25, height=2, command=self.openTPT, bg = "#f6f6f6")
            self.btn_openExp.grid(row=20, column=2, sticky=W) 

            self.btn_quit = Button(tab3, text="Quit", activebackground="#f05e53", width=25, height=2, command=tb_call_quit, bg = "#f6f6f6")
            self.btn_quit.grid(row=20, column=2, sticky=E)

        except Exception as e:
            messagebox.showerror('Error',e)

    def openTPT(self):

        tpt_dir = tpt_path.get()

        if not tpt_path:
            messagebox.showerror("FileNotFoundError","No TPT file was selected")
        else:    
            os.startfile(tpt_dir)
#-----------------------START: Import libraries---------------------------
import os
import csv
import sys
import xml.etree.ElementTree as ET 
import tkinter as tk
import string 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk 
import uuid
import webbrowser
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from math import sqrt
import datetime

# import file py for every tab
from interface import *
from tab1_equivalence_class import *
from tab2_assesslet_creator import *
from tab3_attributes_xml import *
from tab4_req_linker import *
from tab5_scripts_updater import *
from tab6_b2b_tol_updater import *
from tab7_spec_delta import *
#------------------------END: Import libraries----------------------------



#----------------------------------START: TABS----------------------------
def main_init():

    #color of background labels
    bg_col = "#fcfcfc"     
    fg_col = "#291b47"
    bt_col = "#f05e53"
    btn_col = "#f6f6f6"

    #set margin right (in all scripts use these lines)
    tk.Label(main, text = "      ", bg = bg_col).grid(row=0, column=4, padx=90)  

    #set margin left (in all scripts use these lines)
    tk.Label(main, text = "      ", bg = bg_col).grid(row=0, column=0, padx=100)
        
    tk.Label(main, text = "                                                                                                                                                                     ", bg = bg_col).grid(row=0, column=1)
    tk.Label(main, text = "      ", bg = bg_col).grid(row=0, column=2)

    tk.Label(main, text="TPT ToolBox", fg = fg_col, font = "Calibri 32 bold", bg = bg_col).grid(row=1, column=1)
    tk.Label(main, text = "Simplicity is the key, therefore required for reliability",font = "Calibri 12 bold", fg = fg_col, bg = bg_col).grid(row=2, pady=10, column=1)

    tk.Label(main, text = "", bg = bg_col).grid(row=5, column=0)

    #begin of list of tools  
    group = LabelFrame(main, bg= btn_col)
    group.grid(row=6, column=1)
    tk.Label(group, text = "                                                                  ", font = "Fixedsys 8", bg= btn_col).grid(row=0, column=0)

    tk.Label(group, text = "1. Equivalence Classes Creator", bg= btn_col, font = "Calibri 12").grid(row=1, column=0, sticky=W, padx=10)
    btn_t1 = Button(group, text="?", cursor="hand2",  font = "Fixedsys 14", fg = "#dddddd", bg = bt_col, activebackground=bg_col,  width=2, borderwidth=1, command=bt1_msgbox)
    btn_t1.grid(row=1, column=0, sticky=E, padx=15, pady=3) 

    tk.Label(group, text = "2. Stub Assesslet Generator", bg= btn_col, font = "Calibri 12").grid(row=2, column=0, sticky=W, padx=10)
    btn_t2 = Button(group, text="?", cursor="hand2",  font = "Fixedsys 14", fg = "#dddddd", bg = bt_col, activebackground=bg_col,  width=2, borderwidth=1,  command=bt2_msgbox)
    btn_t2.grid(row=2, column=0, sticky=E, padx=15, pady=3) 
    
    tk.Label(group, text = "3. Configuration Attributes Updater", bg= btn_col, font = "Calibri 12").grid(row=3, column=0, sticky=W, padx=10)
    btn_t3 = Button(group, text="?", cursor="hand2",  font = "Fixedsys 14", fg = "#dddddd", bg = bt_col, activebackground=bg_col,  width=2, borderwidth=1,  command=bt3_msgbox)
    btn_t3.grid(row=3, column=0, sticky=E, padx=15, pady=3) 
    
    tk.Label(group, text = "4. Automatic Requirements Linker", bg= btn_col, font = "Calibri 12").grid(row=4, column=0, sticky=W, padx=10)
    btn_t4 = Button(group, text="?", cursor="hand2",  font = "Fixedsys 14", fg = "#dddddd", bg = bt_col, activebackground=bg_col,  width=2, borderwidth=1,  command=bt4_msgbox)
    btn_t4.grid(row=4, column=0, sticky=E, padx=15, pady=3) 

    tk.Label(group, text = "5. Execution Scripts Updater", bg= btn_col, font = "Calibri 12").grid(row=5, column=0, sticky=W, padx=10)
    btn_t4 = Button(group, text="?", cursor="hand2",  font = "Fixedsys 14",  fg = "#dddddd", bg = bt_col, activebackground=bg_col, width=2, borderwidth=1,  command=bt5_msgbox)
    btn_t4.grid(row=5, column=0, sticky=E, padx=15, pady=3) 

    tk.Label(group, text = "6. B2B Tolerance Updater", bg= btn_col, font = "Calibri 12").grid(row=6, column=0, sticky=W, padx=10)
    btn_t4 = Button(group, text="?", cursor="hand2",  font = "Fixedsys 14", fg = "#dddddd", bg = bt_col, activebackground=bg_col,  width=2, borderwidth=1,  command=bt6_msgbox)
    btn_t4.grid(row=6, column=0, sticky=E, padx=15, pady=3) 

    tk.Label(group, text = "7. Test Specification Delta", bg= btn_col, font = "Calibri 12").grid(row=7, column=0, sticky=W, padx=10)
    btn_t4 = Button(group, text="?", cursor="hand2", font = "Fixedsys 14", fg = "#dddddd", bg = bt_col, activebackground=bg_col, width=2, borderwidth=1,  command=bt7_msgbox)
    btn_t4.grid(row=7, column=0, sticky=E, padx=15, pady=3) 

    tk.Label(group, text = "                                                                  ", font = "Fixedsys 8", bg= btn_col).grid(row=8, column=0)
    #end of list of tools 
    
    tk.Label(main, text = " ", bg = bg_col).grid(row=9, column=0)
    tk.Label(main, text = " ", bg = bg_col).grid(row=10, column=0)
    tk.Label(main, text = " ", bg = bg_col).grid(row=11, column=0)

    lab_vers = tk.Label(main, text=revision, cursor="hand2", fg = "#291b47", bg = bg_col, font = "Calibri 12 bold")
    lab_vers.bind("<Button-1>", tb_call_vers)  
    lab_vers.grid(row=12, column=1, sticky=W)   

    lab_vers2 = tk.Label(main, text="  |  ", fg = "#ee4c40", bg = bg_col, font = "Calibri 12 bold")
    lab_vers2.grid(row=12, column=1, sticky=W, padx=40)  

    lab_vers3 = tk.Label(main, text="TPT 17 compatible", fg = "#839515", bg = bg_col, font = "Calibri 12 bold")
    lab_vers3.grid(row=12, column=1, sticky=W, padx=65)  

    lab_mail = tk.Label(main, text="Ask for help!", cursor="hand2", fg = "#ee4c40", bg = bg_col, font = "Calibri 12 bold underline")
    lab_mail.bind("<Button-1>", tb_call_mail)
    lab_mail.grid(row=12, column=1, sticky=E)   

    tk.Label(main, text = " ", bg = bg_col).grid(row=13, column=0)
    tk.Label(main, text = " ", bg = bg_col).grid(row=14, column=0)
    tk.Label(main, text = " ", bg = bg_col).grid(row=15, column=0)
#-----------------------------------END: TABS-----------------------------



#---------------------------START: Drawing interface-----------------------------------
createMenu(root)

main_init()

Tab1(tab1)

Tab2(tab2)

Tab3(tab3)

Tab4(tab4)

Tab5(tab5)

Tab6(tab6)

Tab7(tab7)

root.mainloop()
#---------------------------END: Drawing interface-----------------------------------
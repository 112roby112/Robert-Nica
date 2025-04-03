####################################################################################################################################
# B2B TOLERANCE UPDATER FOR MODULES
#
# WHAT: 
# - This tool is populating for all Back 2 Back configurations the absolute tolerance and the time tolerance for all output signals. 
# - Optionally you can set 1 sample time deviation for all outputs. 
# - Be aware that the script is working only on module level, not on SWC level.
# 
# WHY: 
# - To reduce time for the testers when complete the tolerances by hand
# 
# AUTHOR:
# - Cioban Marcel/Falamas Ovidiu
# 
# INPUT:
# - TPT file
# 
# OUTPUT:
# - An updated TPT file with all the B2B signals updated with tolerances
###################################################################################################################################

import os
import re
import sys
import csv
import stat
import string
import tkinter
import os.path
import platform
from shutil import copyfile
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk 
from tkinter import *
from interface import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import xml.etree.ElementTree as xml

tpt_path = tk.StringVar()
tpt_file = ''
tick1 = IntVar()

class Tab6():
    
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
        
        self.lable2 = tk.Label(tab, cursor="hand2", text="B2B Tolerance Updater For Modules", fg = fg_col, font = "Calibri 18 bold", bg = bg_col)
        self.lable2.bind ('<1>', lambda self: bt6_msgbox())
        self.lable2.grid(row=1, column=2)

        self.lable3 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable3.grid(row=2, column=0, pady=10)

        self.btn_openTPT = Button(tab6, text="Select Module TPT file", activebackground=gold_color, width=30, height=2, command=self.open_files, bg = bt_col)
        self.btn_openTPT.grid(row=3, column=2) 

        self.lable4 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable4.grid(row=4, column=0)

        self.lbl_text = tk.Label(tab6, text = "TPT path:   ", bg = bg_col)
        self.lbl_text.grid(row=5, column=1)

        self.lbl_tpt = Entry(tab6, textvariable=tpt_path, width="75")
        self.lbl_tpt.grid(row=5, column=2)

        self.lable5 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable5.grid(row=6, column=0)

        self.check1 = Checkbutton(tab, state = DISABLED, text="Click on checkbox for setting 1 sample time deviation for all outputs", activebackground=bg_col, variable=tick1, bg = bg_col)
        self.check1.grid(row=7, column=2, pady=10, sticky=W, ipadx = 50)

        self.lable6 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable6.grid(row=8, column=0)

        self.btn_UpdateB2B = Button(tab6,state = DISABLED, text="Update B2B Tolerances", activebackground=bt_col, width=30, height=2, command=self.start, bg = bt_col)
        self.btn_UpdateB2B.grid(row=9, column=2) 

        self.lable6 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable6.grid(row=10, column=0, pady=30)

        self.btn_openExp = Button(tab, state = DISABLED, text="Open TPT file", activebackground=bt_col, width=20, height=2, command=self.openTPT, bg = bt_col)
        self.btn_openExp.grid(row=11, column=2, sticky=W) 

        self.btn_quit = Button(tab, text="Quit", activebackground=gold_color, width=20, height=2, command=tb_call_quit, bg = bt_col)
        self.btn_quit.grid(row=11, column=2, sticky=E)
        
    def open_files(self):

        global tpt_file 

        try:
            if os.path.isdir('C:\Work'):
                initialdir_fav = 'C:\Work'
            elif os.path.isdir('D:\Work'):
                initialdir_fav = 'D:\Work'
            else:
                initialdir_fav = os.path.dirname(__file__)
            
            tpt_file = askopenfilename(title = "Select TPT file", initialdir = initialdir_fav, filetypes=[("TPT file","*.tpt")]) 

            if len(tpt_file) > 1:
                tpt_path.set(tpt_file)

                self.check1.config(state = ACTIVE)
                self.btn_UpdateB2B.config(state = ACTIVE) 

            return tpt_path

        except NameError:
            messagebox.showerror("NameError","No TPT file was found")
        except FileNotFoundError:
            messagebox.showerror("FileNotFoundError","No TPT file was selected")
        except:
            messagebox.showerror("Unexpected error:", sys.exc_info()[0])

    #backup TPT 
    def create_backup(self):

        tpt_dir = tpt_path.get()

        if not tpt_path:
            messagebox.showerror("FileNotFoundError","No TPT file was selected")
        else:    
            original = tpt_dir
            intermed = original[:-4]
            target = intermed + "_backup.tpt"

            copyfile(original, target)

        return 1

    #this function extracts every Float and Double type Output from the Declaration editor.
    def B2BUpdate(self):
        
        tpt_dir = tpt_path.get()
        ct = 0
        p1 = tick1.get()


        try:
            os.chmod(tpt_dir, stat.S_IWRITE )
            tptXML = xml.parse(tpt_dir.encode("UTF-8"))
            tptRoot = tptXML.getroot()
        except:
            messagebox.showerror("Error","Can't parse TPT file! First, please close it!")
            return 0   

        #read DeclarationEditor Outputs 
        try:
            #Indent to find Outputs
            print("Find Outputs in TPT Declaration editor structure")
            DeState1 = tptRoot.find('header')
            DeState2 = DeState1.find('declarations')
            DeState3 = DeState2.find('channels')
            channels = DeState3.findall("channel")
            OutputList = []
            OutputListArray = []
            OutputListRest = []

            for channel in channels:
                role = channel.get("role")
                type = channel.get("type")
                if role == "input" and (type == "float" or type == "double" ):
                    OutputList.append(channel.get("name"))
                
                if role == "input" and (type == "float[]" or type == "double[]" ):
                    OutputListArray.append(channel.get("name"))

                if role == "input" and (type == "boolean[]" or type == "boolean" or type == "uint8[]" or type == "uint8" or type == "uint16[]" or type == "uint16" or type == "uint32[]" or type == "uint32"  or type == "int8[]" or type == "int8" or type == "int16[]" or type == "int16" or type == "int32[]" or type == "int32"  or type == "int64[]" or type == "int64"):
                    OutputListRest.append(channel.get("name"))


        except AttributeError as error:
            messagebox.showerror("Warning","Couldn't find any valid signal in the TPT file.")
            return 0
        
        #find B2B Reference Directory for every setup

        back2backname = []
        EcState1 = tptRoot.find("execspec")
        EcState2 = EcState1.find("execconfigs")
        for execconfig in EcState2.findall("execconfig"):
            nameconfig = execconfig.get("name")
            if "B2B" in nameconfig :
                #print (nameconfig)
                EcState3 = execconfig.findall("execconfigitem")
                EcState4 = EcState3[-1].find("assesslet_back2back")
                if EcState4 is not(None):
                    for back2backrow in EcState4.findall("back2backrow") : 
                        back2backname = back2backrow.get("name")

                        if p1:
                            string_value_timetol = "@"
                        else:
                            string_value_timetol = "0"

                        if (back2backname in OutputListArray):
                            string_value_tolerance  = 'SPE_Dict["'+back2backname+'_001"]['+"'tolerance']"
                            back2backrow.set("value-tolerance", string_value_tolerance)
                            back2backrow.set("time-tolerance", string_value_timetol)
                            
                        elif (back2backname in OutputList):
                            string_value_tolerance  = 'SPE_Dict["'+back2backname+'"]['+"'tolerance']"
                            back2backrow.set("value-tolerance", string_value_tolerance)
                            back2backrow.set("time-tolerance", string_value_timetol)

                        elif (back2backname in OutputListRest):
                            string_value_tolerance  = 'SPE_Dict["'+back2backname+'"]['+"'tolerance']"
                            back2backrow.set("value-tolerance", '0')
                            back2backrow.set("time-tolerance", string_value_timetol)  

                        else:
                            back2backrow.set("value-tolerance", '0')
                            back2backrow.set("time-tolerance", '0')

                    ct += 1
  
        if ct == 0:
                messagebox.showerror("Warning","No Back 2 Back configuration found.")
                return 0    
        else:
            try:
                tptXML.write(tpt_dir, encoding='UTF-8', xml_declaration=True, default_namespace=None, method="xml")
                messagebox.showinfo("Info","DONE! Your tolerances were updated.")
                self.btn_openExp.config(state = ACTIVE) 

            except Exception as e:
                messagebox.showerror("Error","Can't write in TPT file. Be sure the .tpt file is closed!")

    def start(self):
        tpt_dir = tpt_path.get()

        if not tpt_path:
            messagebox.showerror("FileNotFoundError","No TPT file was selected!")
        else:    
            backup_return = self.create_backup()
            if backup_return:
                self.B2BUpdate()
            else:
                messagebox.showerror("Error","Backup could not be done!")

    def openTPT(self):

        tpt_dir = tpt_path.get()

        if not tpt_path:
            messagebox.showerror("FileNotFoundError","No TPT file was selected!")
        else:    
            os.startfile(tpt_dir)

    
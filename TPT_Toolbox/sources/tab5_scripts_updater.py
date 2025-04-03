####################################################################################################################################
# EXECUTION SCRIPTS UPDATER
#
# WHAT: 
# - This tool is updating the following scripts inside TPT: Original Model, Model Load, Test Run and Assesslet Dictionary_SPE
# - Before using it, be sure that your TPT file and TI_Project_Module.tpt is closed
# 
# WHY: 
# - Ensure that your .tpt file conforms with the template
# 
# AUTHOR:
# - Falamas Ovidiu
# 
# INPUT:
# - TPT file and TI_Project_Module.tpt 
# 
# OUTPUT:
# - An updated TPT file with desired scripts updated
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

#global variables used in all functions
tpt1_path = tk.StringVar()
tpt2_path = tk.StringVar()
tick1 = IntVar()
tick2 = IntVar()
tick3 = IntVar()
tick4 = IntVar()
tick5 = IntVar()
tick6 = IntVar()

class Tab5():
    
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
        
        self.lable2 = tk.Label(tab, cursor="hand2", text="Test Scripts Updater", fg = fg_col, font = "Calibri 18 bold", bg = bg_col)
        self.lable2.bind ('<1>', lambda self: bt5_msgbox())
        self.lable2.grid(row=1, column=2)

        self.lable3 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable3.grid(row=2, column=0, pady=10)

        self.btn_open = Button(tab, text="Open TPT files", activebackground=gold_color, width=30, height=2, command=self.open_files, bg = bt_col)
        self.btn_open.grid(row=3, column=2)

        self.lable4 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable4.grid(row=4, column=0)

        self.lableTPT1 = tk.Label(tab, text = "Your TPT file: ", bg = bg_col)
        self.lableTPT1.grid(row=5, column=1)

        self.labletpt1 = tk.Entry(tab, textvariable=tpt1_path, width="75")
        self.labletpt1.grid(row=5, column=2)

        self.lableTPT2 = tk.Label(tab, text = "TI Pj. Module: ", bg = bg_col)
        self.lableTPT2.grid(row=6, column=1)

        self.labletpt2 = tk.Entry(tab, textvariable=tpt2_path, width="75")
        self.labletpt2.grid(row=6, column=2)

        self.lable4 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable4.grid(row=7, column=0)

        self.check1 = Checkbutton(tab, state = DISABLED, text="Original Model", activebackground=bg_col, variable=tick1, bg = bg_col)
        self.check1.grid(row=8, column=2, pady=10, sticky=W, ipadx = 50)

        self.check2 = Checkbutton(tab, state = DISABLED, text="Model Load Script", activebackground=bg_col, variable=tick2, bg = bg_col)
        self.check2.grid(row=9, column=2, pady=10, sticky=W, ipadx = 50)

        self.check3 = Checkbutton(tab, state = DISABLED, text="Test Run Script", activebackground=bg_col, variable=tick3, bg = bg_col)
        self.check3.grid(row=8, column=2, pady=10, sticky=E, ipadx = 50)

        self.check4 = Checkbutton(tab, state = DISABLED, text="Dictionary_SPE", activebackground=bg_col, variable=tick4, bg = bg_col)
        self.check4.grid(row=9, column=2, pady=10, sticky=E, ipadx = 50)    

        self.check5 = Checkbutton(tab, state = DISABLED, text="Post Processing", activebackground=bg_col, variable=tick5, bg = bg_col)
        self.check5.grid(row=10, column=2, pady=10, sticky=W, ipadx = 50)

        self.check6 = Checkbutton(tab, state = DISABLED, text="Update all        ", activebackground=bg_col, variable=tick6, bg = bg_col)
        self.check6.grid(row=10, column=2, pady=10, sticky=E, ipadx = 50)   

        self.lable5 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable5.grid(row=11, column=0)

        self.btn_run = Button(tab,state = DISABLED ,text="Update selected options", activebackground=bt_col, width=30, height=2, command=self.run_general, bg = bt_col)
        self.btn_run.grid(row=12, column=2, pady=13)

        self.lable6 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable6.grid(row=13, column=0)

        self.btn_openExp = Button(tab, state = DISABLED ,text="Open TPT file", activebackground=bt_col, width=20, height=2, command=self.openTPT, bg = bt_col)
        self.btn_openExp.grid(row=14, column=2, sticky=W) 

        self.btn_quit = Button(tab, text="Quit", activebackground=gold_color, width=20, height=2, command=tb_call_quit, bg = bt_col)
        self.btn_quit.grid(row=14, column=2, sticky=E)

    def open_files(self):
        try:

            tpt1_dir = askopenfilename(title = "Select TPT file", filetypes=[("TPT file","*.tpt")]) 
            
            if tpt1_dir.find('TI_Project_Module') > 0:

                tpt1_dir = ''
                tpt2_dir = ''

                tpt1_path.set(tpt1_dir)
                tpt2_path.set(tpt2_dir)

                self.check1.config(state = DISABLED, bg = "#fcfcfc")
                self.check2.config(state = DISABLED, bg = "#fcfcfc")
                self.check3.config(state = DISABLED, bg = "#fcfcfc")
                self.check4.config(state = DISABLED, bg = "#fcfcfc")
                self.check5.config(state = DISABLED, bg = "#fcfcfc")
                self.check6.config(state = DISABLED, bg = "#fcfcfc")                
                self.btn_run.config(state = DISABLED, bg = "#fcfcfc") 

                messagebox.showerror("NameError","First select the desired TPT file, not the TI_Project_Module")
                return None
            else:

                go_up1 = tpt1_dir
                go_up2 = tpt1_dir

                for _ in range(4):
                    parentDir1 = os.path.dirname(go_up1) 
                    go_up1 = parentDir1 

                preferredPath1 = parentDir1 + '/TstTools/LIB/TPT_LIB'

                for _ in range(8):
                    parentDir2 = os.path.dirname(go_up2) 
                    go_up2 = parentDir2 
                    if go_up2 == "C:/Work" or go_up2 == "D:/Work":
                        break    

                preferredPath2 = parentDir2 + '/ChassisControl_Process/01_Engineering_Process/03_Test/06_TPT_LIB'
                
                if os.path.isdir(preferredPath1): 
                    tpt2_dir = askopenfilename(title = "Select TI_Project_Module file", initialdir = preferredPath1, filetypes=[("TPT file","*.tpt")]) 
                elif os.path.isdir(preferredPath2): 
                    tpt2_dir = askopenfilename(title = "Select TI_Project_Module file", initialdir = preferredPath2, filetypes=[("TPT file","*.tpt")]) 
                else:
                    tpt2_dir = askopenfilename(title = "Select TI_Project_Module file", filetypes=[("TPT file","*.tpt")]) 
                
                if len(tpt1_dir) > 1 and len(tpt2_dir) > 1: 
                    tpt1_path.set(tpt1_dir)
                    tpt2_path.set(tpt2_dir)

                    self.check1.config(state = ACTIVE, bg = "#fcfcfc")
                    self.check2.config(state = ACTIVE, bg = "#fcfcfc")
                    self.check3.config(state = ACTIVE, bg = "#fcfcfc")
                    self.check4.config(state = ACTIVE, bg = "#fcfcfc")
                    self.check5.config(state = ACTIVE, bg = "#fcfcfc")
                    self.check6.config(state = ACTIVE, bg = "#fcfcfc")                
                    self.btn_run.config(state = ACTIVE, bg = "#fcfcfc") 

                return tpt1_path, tpt2_path

        except NameError:
            messagebox.showerror("NameError","No TPT file was found")
        except FileNotFoundError:
            messagebox.showerror("FileNotFoundError","No TPT file was selected")
        except:
            messagebox.showerror("Unexpected error:", sys.exc_info()[0])

    def run_general(self):
        p1 = tick1.get()
        p2 = tick2.get()
        p3 = tick3.get()
        p4 = tick4.get()
        p5 = tick5.get()
        p6 = tick6.get()

        tptpath_1 = tpt1_path.get()
        tptpath_2 = tpt2_path.get()

        if not(p1 or p2 or p3 or p4 or p5 or p6):
            messagebox.showinfo("Info","Please select an option!")

            return None
        else:
            if p6: 
                self.thick6_all()             
                self.thick1_org_model(tptpath_1, tptpath_2)
                self.thick2_mod_load(tptpath_1, tptpath_2)
                self.thick3_tst_run(tptpath_1, tptpath_2)   
                self.thick4_dict_spe(tptpath_1, tptpath_2)
                self.thick5_post(tptpath_1, tptpath_2) 

                messagebox.showinfo("Info","DONE! The test scripts were updated accordingly.")
                self.btn_openExp.config(state = ACTIVE) 

                return None

            else:
                if p1:
                    self.thick1_org_model(tptpath_1, tptpath_2)
                if p2:
                    self.thick2_mod_load(tptpath_1, tptpath_2)
                if p3:
                    self.thick3_tst_run(tptpath_1, tptpath_2)
                if p4:
                    self.thick4_dict_spe(tptpath_1, tptpath_2)
                if p5:
                    self.thick5_post(tptpath_1, tptpath_2)

                messagebox.showinfo("Info","DONE! The test scripts were updated accordingly.")
                self.btn_openExp.config(state = ACTIVE) 

    def thick1_org_model(self, tpt1_file, tpt2_file):
    
        if not os.path.isfile(tpt1_file):
            showerror("ALERT","The TPT file does not exist !")
            return 0

        if '.tpt' not in tpt1_file:
            showerror("ALERT","First, please select a TPT file !")
            return 0
        try:
            mydoc = minidom.parse(tpt2_file)

            platfrm_list = []
            origm_list = []

            platform_config = mydoc.getElementsByTagName('platformconfig')
            for config in platform_config:
                platform_name = config.getAttribute("name")
                platfrm_list.append(platform_name)

                platform_specific = config.getElementsByTagName('platformspecific')
                for specific in platform_specific:
                    platform_key = specific.getAttribute('key')
                    platform_value = specific.getAttribute("value")

                    if platform_key == "originalModelLoadScript":
                        origm_list.append(platform_value)

            dictionary = dict(zip(platfrm_list, zip(origm_list)))
                        
            os.chmod(tpt1_file, stat.S_IWRITE )
            element = ElementTree.parse(tpt1_file)
            xml = element.getroot()

            for elem in xml.iter('platformconfig'):
                name = elem.get('name')
                for subelem in elem:
                    if subelem.get('key') == "originalModelLoadScript":
                        subelem.set('value', dictionary.get(name)[0])

            tree = ET.ElementTree(xml)
            tree.write(tpt1_file)
            
        except Exception as e:
            messagebox.showerror('Error',e)

    def thick2_mod_load(self, tpt1_file, tpt2_file):
    
        if not os.path.isfile(tpt1_file):
            showerror("ALERT","The TPT file does not exist !")
            return 0

        if '.tpt' not in tpt1_file:
            showerror("ALERT","First, please select a TPT file !")
            return 0
        try:
            mydoc = minidom.parse(tpt2_file)

            platfrm_list = []
            modload_list = []

            platform_config = mydoc.getElementsByTagName('platformconfig')
            for config in platform_config:
                platform_name = config.getAttribute("name")
                platfrm_list.append(platform_name)

                platform_specific = config.getElementsByTagName('platformspecific')
                for specific in platform_specific:
                    platform_key = specific.getAttribute('key')
                    platform_value = specific.getAttribute("value")

                    if platform_key == "execModelLoadScript":
                        modload_list.append(platform_value)

            dictionary = dict(zip(platfrm_list, zip(modload_list)))
                        
            os.chmod(tpt1_file, stat.S_IWRITE )
            element = ElementTree.parse(tpt1_file)
            xml = element.getroot()

            for elem in xml.iter('platformconfig'):
                name = elem.get('name')
                for subelem in elem:
                    if subelem.get('key') == "execModelLoadScript":
                        subelem.set('value', dictionary.get(name)[0])
                    
            tree = ET.ElementTree(xml)
            tree.write(tpt1_file)
            
        except Exception as e:
            messagebox.showerror('Error',e)

    def thick3_tst_run(self, tpt1_file, tpt2_file):
    
        if not os.path.isfile(tpt1_file):
            showerror("ALERT","The TPT file does not exist !")
            return 0

        if '.tpt' not in tpt1_file:
            showerror("ALERT","First, please select a TPT file !")
            return 0
        try:
            mydoc = minidom.parse(tpt2_file)

            platfrm_list = []
            testrun_list = []

            platform_config = mydoc.getElementsByTagName('platformconfig')
            for config in platform_config:
                platform_name = config.getAttribute("name")
                platfrm_list.append(platform_name)

                platform_specific = config.getElementsByTagName('platformspecific')
                for specific in platform_specific:
                    platform_key = specific.getAttribute('key')
                    platform_value = specific.getAttribute("value")

                    if platform_key == "execRunTestScript":
                        testrun_list.append(platform_value)

            dictionary = dict(zip(platfrm_list, zip(testrun_list)))
                        
            os.chmod(tpt1_file, stat.S_IWRITE )
            element = ElementTree.parse(tpt1_file)
            xml = element.getroot()

            for elem in xml.iter('platformconfig'):
                name = elem.get('name')
                for subelem in elem:
                    if subelem.get('key') == "execRunTestScript":
                        subelem.set('value', dictionary.get(name)[0])
                    
            tree = ET.ElementTree(xml)
            tree.write(tpt1_file)
            
        except Exception as e:
            messagebox.showerror('Error',e)

    def thick4_dict_spe(self, tpt1_file, tpt2_file):
    
        if not os.path.isfile(tpt1_file):
            showerror("ALERT","The TPT file does not exist !")
            return 0

        if '.tpt' not in tpt1_file:
            showerror("ALERT","First, please select a TPT file !")
            return 0
        try:
            mydoc = minidom.parse(tpt2_file)

            assesslet = mydoc.getElementsByTagName('assesslet')
            for asses in assesslet:
                assesslet_name = asses.getAttribute("name")

                if assesslet_name == "TPT_LIB_Dictionary_SPE" or assesslet_name == "Dictionary_SPE":
                    scripts = asses.getElementsByTagName('assesslet_script')
                    my_n_node = scripts[0]
                    my_child = my_n_node.firstChild
                    my_text = my_child.data 
           
            os.chmod(tpt1_file, stat.S_IWRITE )
            element = ElementTree.parse(tpt1_file)
            xml = element.getroot()

            for elem in xml.iter('assesslet'):
                name = elem.get('name')

                if name == "TPT_LIB_Dictionary_SPE" or name == "Dictionary_SPE":
                    for subelem in elem.iter('assesslet_script'):   
                        subelem.text = my_text

            tree = ET.ElementTree(xml)
            tree.write(tpt1_file)

        except Exception as e:
            messagebox.showerror('Error',e)

    def thick5_post(self, tpt1_file, tpt2_file):
    
        if not os.path.isfile(tpt1_file):
            showerror("ALERT","The TPT file does not exist !")
            return 0

        if '.tpt' not in tpt1_file:
            showerror("ALERT","First, please select a TPT file !")
            return 0
        try:
            mydoc = minidom.parse(tpt2_file)

            platfrm_list = []
            testrun_list = []

            platform_config = mydoc.getElementsByTagName('platformconfig')
            for config in platform_config:
                platform_name = config.getAttribute("name")
                platfrm_list.append(platform_name)

                platform_specific = config.getElementsByTagName('platformspecific')
                for specific in platform_specific:
                    platform_key = specific.getAttribute('key')
                    platform_value = specific.getAttribute("value")

                    if platform_key == "testFramePostProcessScript":
                        testrun_list.append(platform_value)

            dictionary = dict(zip(platfrm_list, zip(testrun_list)))
                        
            os.chmod(tpt1_file, stat.S_IWRITE )
            element = ElementTree.parse(tpt1_file)
            xml = element.getroot()

            for elem in xml.iter('platformconfig'):
                name = elem.get('name')
                for subelem in elem:
                    if subelem.get('key') == "testFramePostProcessScript":
                        subelem.set('value', dictionary.get(name)[0])
                    
            tree = ET.ElementTree(xml)
            tree.write(tpt1_file)
            
        except Exception as e:
            messagebox.showerror('Error',e)

    def thick6_all(self):
        
        tick1.set(value=False)
        tick2.set(value=False)
        tick3.set(value=False)
        tick4.set(value=False)
        tick5.set(value=False)

        return None


    def openTPT(self):

        tpt_path = tpt1_path.get()

        if not tpt_path:
            messagebox.showerror("FileNotFoundError","No TPT file was selected")
        else:    
            os.startfile(tpt_path)

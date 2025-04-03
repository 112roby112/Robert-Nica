####################################################################################################################################
# AUTOMATIC REQUIREMENTS LINKER
#
# WHAT: 
# - This tool is creating the linkage inside TPT, between requirements and assesslets and between requirements and test cases as well
# - Before using it, be sure that all requirements are imported and the TPT file is closed, otherwise you'll receive an error message
# 
# WHY: 
# - Each user has to link the assesslets and the test cases manually...saves a lot of time/effort 
# 
# AUTHOR:
# - Bogdan Turean/Niocale Siderias/Falamas Ovidiu
# 
# INPUT:
# - TPT file 
# 
# OUTPUT:
# - An updated TPT file with links between test cases, asseslets and requirements
###################################################################################################################################


import os
import re
import sys
import stat
import tkinter as tk
from tkinter import *
import os.path
import platform
from shutil import copyfile
from tkinter import filedialog
import xml.etree.ElementTree as xml
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename
from interface import *
from pathlib import Path

#global variables used in all functions
tpt_string = tk.StringVar()
tc_miss_id = []
assess_miss_id = []

class Tab4():
    
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
        
        self.lable2 = tk.Label(tab, cursor="hand2", text="Automatic Requirements Linker", fg = fg_col, font = "Calibri 18 bold", bg = bg_col)
        self.lable2.bind ('<1>', lambda self: bt4_msgbox())
        self.lable2.grid(row=1, column=2)

        self.lable2 = tk.Label(tab, text="Under development", fg = "#839515", font = "Calibri 10 bold", bg = bg_col)
        self.lable2.grid(row=2, column=2)

        self.lable3 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable3.grid(row=2, column=0, pady=10)

        self.btn_open = Button(tab, text="Select TPT file", activebackground=gold_color, width=30, height=2, command=self.select_tpt, bg = bt_col)
        self.btn_open.grid(row=3, column=2)

        self.lable4 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable4.grid(row=4, column=0)

        self.lable4 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable4.grid(row=5, column=0)

        self.lableTPT = tk.Label(tab, text = "TPT path:  ", bg = bg_col)
        self.lableTPT.grid(row=6, column=1)

        self.labletpt = tk.Entry(tab, textvariable=tpt_string, width="75")
        self.labletpt.grid(row=6, column=2)

        self.lable5 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable5.grid(row=7, column=0)

        self.lable6 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable6.grid(row=8, column=0)

        self.btn_run = Button(tab,state = DISABLED ,text="Run", activebackground=bt_col, width=30, height=2, command=self.req_link, bg = bt_col)
        self.btn_run.grid(row=9, column=2, pady=13)

        self.lable7 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable7.grid(row=10, column=0)  

        self.lable8 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable8.grid(row=11, column=0)  

        self.lable8 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable8.grid(row=12, column=0, pady=10)  

        self.btn_openExp = Button(tab, text="Open TPT file", state = DISABLED, activebackground=bt_col, width=20, height=2, command=self.open_tpt, bg = bt_col)
        self.btn_openExp.grid(row=13, column=2, sticky=W) 

        self.btn_quit = Button(tab, text="Quit", activebackground=gold_color, width=20, height=2, command=tb_call_quit, bg = bt_col)
        self.btn_quit.grid(row=13, column=2, sticky=E)

    def select_tpt(self):
        try:
            path =""

            #make different initialDir depending on the platform used
            if "Windows-7" in platform.platform():
                path = r'D:\Work'
            else:
                path = r'C:\Work'

            if os.path.isdir(path):
                tpt_path = askopenfilename(title = "Select TPT file", initialdir = path , filetypes=[("TPT file","*.tpt")]) 
            else:
                tpt_path = askopenfilename(title = "Select TPT file", initialdir = os.path.dirname(__file__) , filetypes=[("TPT file","*.tpt")])    

            tpt_string.set(tpt_path)
            self.btn_run.config(state = ACTIVE)

            return tpt_path

        except NameError:
            messagebox.showerror("NameError","No TPT file was found")
        except FileNotFoundError:
            messagebox.showerror("FileNotFoundError","No TPT file was selected")
        except:
            messagebox.showerror("Unexpected error:", sys.exc_info()[0])

    #backup function
    def create_backup(self):

        TPT_FILE_PATH = tpt_string.get()

        PROJ_PATH = re.findall('.*[\\\/]', TPT_FILE_PATH)
        PROJ_PATH = PROJ_PATH[0].rstrip("")

        TPT_NAME = re.findall('[^\/]+$', TPT_FILE_PATH)
        TPT_NAME = TPT_NAME[0].rstrip(".tpt")

        backup_name = PROJ_PATH + TPT_NAME + '_backup.tpt'
        copyfile(TPT_FILE_PATH, backup_name)

        return 1

    def req_link(self):

        TPT_FILE_PATH = tpt_string.get()

        if TPT_FILE_PATH != "":
            if self.create_backup() == 1:
                print("Backup done")
            else:
                print("Can't create backup")

        try:
            tptXML = xml.parse(TPT_FILE_PATH.encode("UTF-8"))
            tptRoot = tptXML.getroot()
        except:
            print("###Error: Can't open TPT file")
            return 0
        
        statinfo = os.stat(TPT_FILE_PATH)[0]
        if (not statinfo & stat.S_IWRITE):
            messagebox("TPT is READ-ONLY")
            return 0

        #fint TC
        #create a dictionary with all TC. The key is the Path and the values will be the TestCases name
        TestCases = {}
        def folder_scan(folder, key):
            scenario_tp = folder.findall('scenario_tp')
            if len(scenario_tp)>0:
                for child in scenario_tp:
                    name = child.get("name")
                    if name != None:
                        if key not in TestCases.keys():
                            TestCases[key] = []
                        TestCases[key].append(name)
            for child in folder.findall('scenario_group'):
                scenario_group_name = child.get("name")
                scenario_group_name = scenario_group_name.replace('/', "\/")
                next_key = key+scenario_group_name+"/"
                folder_scan(child, next_key)
        try:
            #find the FunctionalTest folder
            tcTree1 = tptRoot.find('body')
            tcTree2 = tcTree1.find('testlet')
            tcTree3 = tcTree2.find('./scenario_group[@name="TestCases"]')
            folder_scan(tcTree3, "TestCases:/")     
        except AttributeError as error:
            print("Error in TC structure!!")
            return 0
    

        #find assesslets
        #create a dictionary with all Assesslets. The key is the Path and the values will be the Assesslets name
        assesslets = {}
        def find_assesslets(folder,key):
            assess = folder.findall("assesslet")
            if len(assess)>0:
                for child in assess:
                    name = child.get("name")
                    if name != None:
                        if re.match("Req_[0-9][0-9][0-9][0-9][0-9][0-9][0-9]", name) != None:
                            if key not in assesslets.keys():
                                assesslets[key]=[]
                            assesslets[key].append(name)
            for group in folder.findall('assessletgroup'):
                assesslet_group_name = group.get("name")   
                next_key = key+assesslet_group_name+"/"
                find_assesslets(group,next_key)
        
        try:
            #find the Assesslets in Assesslets folder
            assesslet1 = tptRoot.find('body')
            assesslet2 = assesslet1.find("assesslets")
            assesslet3 = assesslet2.find('./assessletgroup[@name="Assesslets"]')
            find_assesslets(assesslet3,"Assesslets/")
        except AttributeError as error:
            print("Error in Assesslets structure!!")
            return 0
                
        #find requirements link
        try:
            #find the Requirements in XML structure
            req1 = tptRoot.find('./extension[@name="rm"]')
            requirements = req1.find('rm-module')
            
        except AttributeError as error:
            print("Can't find requirements! There is a problem with xml TAG")
            return 0
        
        #remove existent link
        for dict_keys in TestCases:
            for test_scenario_name in TestCases[dict_keys]:
                regex_find = re.search("_[0-9][0-9][0-9][0-9][0-9][0-9][0-9]_",test_scenario_name)
                if regex_find is not None:
                    tc_req_id = test_scenario_name[regex_find.start():regex_find.end()]
                    tc_req_id = str(tc_req_id).replace( "_", "")
                    current_req = requirements.find('./rm-object[@id="{}"]'.format(tc_req_id))
                    if current_req is not None:
                        for req_old in current_req.findall("rm-link"):
                            if req_old.get("linked-type") == "Scenario" or req_old.get("linked-type") == "Assesslet":
                                current_req.remove(req_old)
        
        #link Tc-Req
        tc_number = 0
        tc_miss_number = 0
        for dict_keys in TestCases:
            if "Deferred" not in dict_keys:
                for test_scenario_name in TestCases[dict_keys]:
                    try:
                        regex_find = re.search("_[0-9][0-9][0-9][0-9][0-9][0-9][0-9]_",test_scenario_name)
                        if regex_find is None:
                            tc_miss_number +=1
                            path_value = dict_keys.replace("TestCases:/", "") + test_scenario_name
                            tc_miss_id.append(path_value)
                        else:
                            tc_req_id = test_scenario_name[regex_find.start():regex_find.end()]
                            tc_req_id = str(tc_req_id).replace( "_", "")
                            current_req = requirements.find('./rm-object[@id="{}"]'.format(tc_req_id))

                            path_value = dict_keys.replace("TestCases:/", "") + test_scenario_name

                            attributes = {"linked-type":"Scenario","scenario-path":path_value,"testlet-path":""}
                            XMLElement = xml.Element('rm-link', attributes) 
                            current_req.append(XMLElement)
                            tc_number += 1
                            continue 
                    except Exception as error:
                        print("Something went wrong with TC links")
        
        #link Assesslets-Req
        assesslet_number = 0
        assess_miss_number = 0
        for dict_keys in assesslets:
            if "Deferred" not in dict_keys:
                for assesslets_name in assesslets[dict_keys]:
                    try:
                        regex_find = re.search("[0-9][0-9][0-9][0-9][0-9][0-9][0-9]",assesslets_name)
                        assess_req_id = assesslets_name[regex_find.start():regex_find.end()]
                        current_req = requirements.find('./rm-object[@id="{}"]'.format(assess_req_id))
                        if current_req is None:
                            assess_miss_number +=1
                            path_value = dict_keys+assesslets_name
                            assess_miss_id.append(path_value)
                            continue
                        path_value = dict_keys+assesslets_name
                        attributes = {"linked-object":path_value, "linked-type":"Assesslet"}
                        XMLElement = xml.Element('rm-link', attributes) 
                        current_req.append(XMLElement)
                        assesslet_number += 1 
                    except Exception as error:
                        print("Something went wrong with TC links")
            
        try:
            #write in TPT file 
            tptXML.write(TPT_FILE_PATH, encoding='UTF-8', xml_declaration=True, default_namespace=None, method="xml")
            #create te final Report
            print(tc_number," test cases are linked.")
            print(assesslet_number, "assesslets are linked")
            if tc_miss_number>0:
                print("\nTC without Req: ")
                for elem in tc_miss_id:
                    print("\t-", elem)
            if assess_miss_number>0:
                print("\nAssesslet without Req: ")
                for elem in assess_miss_id: 
                    print("\t-", elem)
            print("----------Script Done----------")

        except Exception as error:
            print(error)
            print("Something went wrong with final report")
            return 0

    def open_tpt(self):

        exp_tpt = tpt_string.get()

        if not tpt_file:
            messagebox.showerror("FileNotFoundError","No TPT file was selected")
        else:    
            os.startfile(exp_tpt)
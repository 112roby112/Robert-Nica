import os
import re
import sys
import stat
import tkinter as tk
from tkinter import *
import os.path
import platform
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from math import sqrt
import csv
import sys
from xml.dom import minidom
import xml.etree.ElementTree as ET
import codecs
#from interface import *  coment adaugat pentru debug, cand va fi bagat in toolbox tr sa fie uncoment
import codecs
import webbrowser

swrs_path_T4 = ''
spe_path_T4 = ''
SPE_T4 = dict()
SPE_name_T4 = list()
SWRS_req_dict_T4 = dict()

class Tab44():
    def __init__(self):
        print('run')
        
        
    def open_files(self):
        try:
            global spe_path_T4,swrs_path_T4
            spe_path_T4 = askopenfilename(title = "Select SPE export !!", filetypes=[("TPT file","*.csv")]) 
            swrs_path_T4 = askopenfilename(title = "Select SWRS export",  filetypes=[("SPE file","*.csv")]) 
            
            if len(swrs_path_T4) < 1 or len(spe_path_T4) < 1:
                return 0
        #    tpt_string.set(tpt_path)
        #    spe_string.set(spe_path_T4)

        #    if len(swrs_path_T4) > 1 and len(spe_path_T4) > 1:
        #        self.btn_run_tab1.config(state=ACTIVE)

            return swrs_path_T4, spe_path_T4

        except NameError:
            messagebox.showerror("NameError","No SPE file found in the TC folder")
        except FileNotFoundError:
            messagebox.showerror("FileNotFoundError","No SWRS file was selected")
        except:
            messagebox.showerror("Unexpected error:", sys.exc_info()[0])
            
            
            
    def SPE_signals(self):
        global SPE_T4,SPE_name_T4,spe_path_T4
        try:
            SPE_content = list(csv.DictReader(open(spe_path_T4,"r")))
        except:
            return 0

        keys = ['name','portType','physMin','physMax','dataType']
        for key in keys:
            if key not in SPE_content[0].keys():
                return 0
        temp_dict = dict()
        
        for signal in SPE_content:
        
            # if missing physmin or physmax
            if len(signal["physMin"]) == 0 and len(signal["physMax"]) == 0:
                showerror('Error','The sigal {} do not have physMin and physMax value, please check'.format(str(signal["name"])))
                return 0
            elif len(signal["physMin"]) == 0 and len(signal["physMax"]) > 0:
                showerror('Error','The sigal {} do not have physMin  value, please check'.format(str(signal["name"])))
                return 0
            elif len(signal["physMin"]) > 0 and len(signal["physMax"]) == 0:
                showerror('Error','The sigal {} do not have physMax  value, please check'.format(str(signal["name"])))
                return 0

 #           if "Int" in signal["dataType"]:
 #               temp_dict["physMin"] = long(signal["physMin"])
 #               temp_dict["physMax"] = long(signal["physMax"])
 #           else:
 #               temp_dict["physMin"] = float(signal["physMin"])
 #               temp_dict["physMax"] = float(signal["physMax"])    
 #           temp_dict["dataType"] = signal["dataType"]            

            SPE_T4[signal["name"]] = temp_dict
            
        for name in  SPE_T4.keys():   
            SPE_name_T4.append(name)

        
    def SWRS_req(self):
        global SWRS_req_dict_T4,swrs_path_T4 
        try:
            SWRS_content = list(csv.DictReader(open(swrs_path_T4,"r")))
        except:
            return 0

        keys_swrs = ['Text','ID']
        for key in keys_swrs:
            if key not in SWRS_content[0].keys():
                return 0
        temp_dict = dict()
        
        for signal in SWRS_content:             
            SWRS_req_dict_T4[signal["ID"]] = signal["Text"].replace('\n','  ') + '  '
            
            
        
            
        

    def run(self):
        global SWRS_req_dict_T4,SPE_T4
        signal_not_swrs = list()
        nr_signal= 0
        for signal_name in SPE_T4.keys():
            flag_exist = 0
            #signal_name = signal_name + ' '
            for id_swrs in SWRS_req_dict_T4:
                if 'PRC_s_CtrAlv' == signal_name and '1153817' == id_swrs:
                    print('asdsa')
                #if signal_name in SWRS_req_dict_T4[id_swrs]:
                if signal_name  in SWRS_req_dict_T4[id_swrs]:
                   # print(signal_name + '  exist in ID: ' + id_swrs)
                    flag_exist = 1
            
            if flag_exist == 0:
                signal_not_swrs.append(signal_name)
                nr_signal += 1
                
        text_info = 'This signals from SPE are not used SWRS, ('+ str(nr_signal) + ') : '
        html_template = """
            <html>
            <head></head>
            <body>
            <p> """+ text_info + '</p>' 
        # to open/create a new html file in the write mode
        f = open('Signals_SPE_not_in_SWRS.html', 'w')    
        
        for signals in signal_not_swrs:
            # the html code which will go in the file GFG.html
            html_template = html_template + '<p>'+ signals + '</p>'
            
        # writing the code into the file
        f.write(html_template)
        
        # close the file
        f.close()
        
        # viewing html files
        # below code creates a 
        # codecs.StreamReaderWriter object
        file = codecs.open("Signals_SPE_not_in_SWRS.html", 'r', "utf-8")
        
        # using .read method to view the html 
        # code from our object
        print(file.read())
        html_template = html_template + """</body>
                                            </html>
                                            """
        webbrowser.open_new_tab('Signals_SPE_not_in_SWRS.html')
        
fnbc = Tab44()
fnbc.open_files()
fnbc.SPE_signals()
fnbc.SWRS_req()
fnbc.run()      


        
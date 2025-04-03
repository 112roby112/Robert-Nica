####################################################################################################################################
# STUB ASSESSLET GENERATOR
#
# WHAT: 
# - This tool creates an export (.txt) of all requirements in a specific format which respect the template assesslet body
# - The script will make differences between preconditions and requirements
# 
# WHY: 
# - Writes assesslets faster by copying them from .txt file in TPT
# 
# AUTHOR:
# - Falamas Ovidiu
# 
# INPUT:
# - Export of requirements (.xlsx format)
# 
# OUTPUT:
# - One .txt file
###################################################################################################################################

import tkinter as tk
from tkinter import *
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment, Font, colors
from openpyxl.styles.borders import Border, Side
import tempfile
import time
import os
from future.moves.tkinter import filedialog, messagebox
import datetime
from interface import *
import csv
import pandas as pd
import textwrap
import math
import re
import subprocess

#global variables used in all functions
xls_string = tk.StringVar()
exp_string = tk.StringVar()

class Tab2():
    
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
        
        self.lable2 = tk.Label(tab, cursor="hand2", text="Stub Assesslet Generator", fg = fg_col, font = "Calibri 18 bold", bg = bg_col)
        self.lable2.bind ('<1>', lambda self: bt2_msgbox())
        self.lable2.grid(row=1, column=2)

        self.lable3 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable3.grid(row=2, column=0, pady=10)

        self.btn_open = Button(tab, text="Open requirements export\n from Integrity", activebackground=gold_color, width=30, height=2, command=self.open_excel, bg = bt_col)
        self.btn_open.grid(row=3, column=2)

        self.lable4 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable4.grid(row=4, column=0)

        self.lableXLS = tk.Label(tab, text = "Excel path:  ", bg = bg_col)
        self.lableXLS.grid(row=5, column=1)

        self.lablexls = tk.Entry(tab, textvariable=xls_string, width="75")
        self.lablexls.grid(row=5, column=2)

        self.lable5 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable5.grid(row=6, column=0)

        self.entry1 = tk.Entry(tab, width="50")
        self.entry1.grid(row = 7, column = 2) 
        self.entry1.insert(0, 'Enter the assesslet author...')
        self.entry1.bind('<FocusIn>', self.on_entry1)
        self.entry1.bind('<FocusOut>', self.on_focusout1)
        self.entry1.config(fg = 'grey')

        self.entry2 = tk.Entry(tab, width="50")
        self.entry2.grid(row = 8, column = 2, pady=10) 
        self.entry2.insert(0, 'Enter the SWRS baseline...')
        self.entry2.bind('<FocusIn>', self.on_entry2)
        self.entry2.bind('<FocusOut>', self.on_focusout2)
        self.entry2.config(fg = 'grey')

        self.btn_run = Button(tab,state = DISABLED ,text="Run", activebackground=bt_col, width=30, height=2, command=self.call_run, bg = bt_col)
        self.btn_run.grid(row=9, column=2, pady=13)

        self.lable6 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable6.grid(row=10, column=0)  

        self.lableEXP = tk.Label(tab, text = "Export path:  ", bg = bg_col)
        self.lableEXP.grid(row=11, column=1)

        self.lableexp = tk.Entry(tab, textvariable=exp_string, width="75")
        self.lableexp.grid(row=11, column=2)

        self.lable7 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable7.grid(row=12, column=0, pady=10)  

        self.btn_openExp = Button(tab, state = DISABLED ,text="Open export file", activebackground=bt_col, width=20, height=2, command=self.open_exp, bg = bt_col)
        self.btn_openExp.grid(row=13, column=2, sticky=W) 

        self.btn_quit = Button(tab, text="Quit", activebackground=gold_color, width=20, height=2, command=tb_call_quit, bg = bt_col)
        self.btn_quit.grid(row=13, column=2, sticky=E)

    def on_entry1(self, event):
        if self.entry1.get() == 'Enter the assesslet author...':
            self.entry1.delete(0, "end") # delete all the text in the entry
            self.entry1.insert(0, '') #Insert blank for user input
            self.entry1.config(fg = 'black')

    def on_focusout1(self, event):
        if self.entry1.get() == '':
            self.entry1.insert(0, 'Enter the assesslet author...')
            self.entry1.config(fg = 'grey')

    def on_entry2(self, event):
        if self.entry2.get() == 'Enter the SWRS baseline...':
            self.entry2.delete(0, "end") # delete all the text in the entry
            self.entry2.insert(0, '') #Insert blank for user input
            self.entry2.config(fg = 'black')

    def on_focusout2(self, event):  
        if self.entry2.get() == '':
            self.entry2.insert(0, 'Enter the SWRS baseline...')
            self.entry2.config(fg = 'grey')

    def open_excel(self):
        try:
            excel_path = filedialog.askopenfilename(title = "Select export file", filetypes=[("Excel file","*.xlsx"),("Excel file", "*.xls")]) 
           
            if len(excel_path) > 1:
                xls_string.set(excel_path)
                self.btn_run.config(state = ACTIVE)

            return excel_path

        except NameError:
            messagebox.showerror("NameError","No Excel file found in the folder")
        except FileNotFoundError:
            messagebox.showerror("FileNotFoundError","No Excel file was selected")
        except:
            messagebox.showerror("Unexpected error:", sys.exc_info()[0])    

    def call_run(self):
        f_exp = self.create_stub(xls_string.get())
        exp_string.set(f_exp)
        if len(f_exp) > 1: 
            self.btn_openExp.config(state=ACTIVE)

    def create_stub(self, excel_path):

        exp_str_manip = excel_path.rsplit('.',1)
        export_path = exp_str_manip[0] + '.txt'

        req_text, req_title = '',''

        d = datetime.datetime.today()
        date_str = d.strftime('%d-%m-%Y')

        author = self.entry1.get()
        baseline = self.entry2.get()

        df = pd.read_excel (excel_path)

        m_desc = df['Description']
        m_id = df['ID'] 
        m_cat = df['Category']  

        l_desc = []
        l_id = [] 
        l_cat = []

        for x,y,z in zip(m_desc, m_id, m_cat):
            l_desc.append(x)
            l_id.append(y)
            l_cat.append(z)

        export_file = open(export_path,"w+")

        for count, category in enumerate(l_cat):
            if "Pre Condition" == category or "Functional Requirement" == category:
                if pd.isnull(l_desc[count]):
                    req_name = " "
                    req_id = l_id[count]
                    req_var = req_name.replace(" ", "_")
                    desc_text = " "
                else:
                    req_name = l_desc[count].partition("\n")[0].replace(" ", "")
                    req_id = l_id[count]
                    req_var = req_name.replace(" ", "_")
                    desc_text = l_desc[count].split("\n")

                l_print = list()

                for x,lines in enumerate(desc_text):
                    if len(lines) > 70:
                        rep_list = textwrap.wrap(lines,70)
                        for j in rep_list:
                            l_print.append(j)
                    else: 
                        lines = re.sub(' +', ' ',lines)
                        if " " != lines and "" != lines: 
                            l_print.append(lines)

                desc_line = ''
                
                for line in (l_print):
                    desc_line +='# ' + line + '\n'

                if "Pre Condition" in category:
                    req_title = 'Pre_' + str(req_id) + '_' + req_name 

                    content = '# Define the precondition variable\n' + \
                            req_var + ' = TPT.DoubleX()' + '\n\n' + \
                            '# Calculate the signal ' + req_name + '\n' + \
                            req_var + '(t) := 0' + '\n'

                elif "Functional Requirement" == category:
                    req_title = 'Req_' + str(req_id) + '_' + req_name 

                    exp = req_var + "_Exp_" + str(req_id)
                    diff = req_var + "_Diff_" + str(req_id)
                    hose = req_var + '_' + str(req_id) + '_hose_result'

                    content = '# Define the requirement caption\n' + \
                            'Req' + str(req_id) + '_Caption = ' + '\'' + req_name + '\'\n\n' + \
                            '# Define the requirement variable\n' + \
                            exp + ' = TPT.DoubleX()\n' + \
                            diff + ' = TPT.DoubleX()\n' + \
                            hose + ' = TPT.Double()\n\n' + \
                            '# Calculate reference signal\n' + \
                            exp + '(t) := 0\n\n' + \
                            '# Calculate hose result, set time and value tolerance\n' + \
                            hose + '(t) := TPT.hose(' + req_var + '(t), ' + exp + '(t), @, 0)\n\n' + \
                            '# Check the requirement\n' + \
                            'during TPT.regexp([init_time(t) and Run_State(t)]):\n' + \
                            '  ' + diff + '(t) := ' + hose + '(t)\n\n' + \
                            '# Output the difference signal graphic\n' + \
                            'TPT_LIB.Report.DiffSignalGraphic(' + req_var + ', ' + exp + ', \n' + \
                            '                                 ' + diff + ', ' + diff + '.getName() + \" - \" + Req' + str(req_id) + '_Caption)'
                            
                comment = '###########################################################################\n' + \
                            '## Assesslet name: ' + req_title + '\n' + \
                            '#\n' + \
                            '## Description:\n' + \
                            '#\n' + desc_line + \
                            '#\n' + \
                            '## AUTHOR:\n' + \
                            '#     ' + author + '\n' + \
                            '#\n' + \
                            '## BASED ON:\n' + \
                            '#     SWRS Label: ' + baseline + '\n' + \
                            '#\n' + \
                            '## DATE:' + date_str + '\n' + \
                            '#     Version: 1.1\n' + \
                            '#\n' + \
                            '## HISTORY:\n' + \
                            '#    Initial version\n' + \
                            '#    TODO: Version <x.x> <Date> <Author>\n' + \
                            '#    <Version description>\n' + \
                            '###########################################################################'

                req_text = req_title + '\n\n' + comment + '\n\n' + content + '\n\n\n\n'

                export_file.writelines(req_text) 
        
        export_file.close()
            
        return export_path

    def open_exp(self):

        exp_path = exp_string.get()
        program_files = os.environ["ProgramFiles"]
        program_filesX = os.environ["ProgramFiles(x86)"]

        notepad_path = program_files + "\\Notepad++\\notepad++.exe"
        notepad_pathX = program_filesX + "\\Notepad++\\notepad++.exe"
        notepad_pathT = "C:\\Tools\\Notepad++\\notepad++.exe"

        if not exp_path:
            messagebox.showerror("FileNotFoundError","No excel file was selected")
        else:
            try:
                if os.path.isfile(notepad_path):
                    subprocess.call([notepad_path, exp_path])
                elif os.path.isfile(notepad_pathX):
                    subprocess.call([notepad_pathX, exp_path])
                elif os.path.isfile(notepad_pathT):
                    subprocess.call([notepad_pathT, exp_path])
            except:
                os.startfile(exp_path)
        
      





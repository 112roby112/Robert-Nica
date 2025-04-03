####################################################################################################################################
# EQUIVALENCE CLASSES CREATOR
#
# WHAT: 
# - Creates equivalence classes for each input from Declaration Editor, based on physMin and physMax from SPE export
# - User can select, as well, to make the mapping between existing signals and new created equivalence classes
# 
# WHY: 
# - Each user has to create each equivalence class manually, by row, for all signals...saves a lot of time/effort 
# 
# AUTHOR:
# - Robert Nica/Falamas Ovidiu
# 
# INPUT:
# - TPT file and SPE export (format .csv)
# 
# OUTPUT:
# - An updated TPT file with equivalence classes and mapping created
###################################################################################################################################

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
from future.types.newint import long
import codecs
from interface import *

SPE_Dict = dict()
tpt_string = tk.StringVar()
spe_string = tk.StringVar()
tpt_17_on = 0
class Tab1():
    
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

        self.lable2 = tk.Label(tab, cursor="hand2", text="Equivalence Classes Creator", fg = fg_col, bg = bg_col, font = "Calibri 18 bold")
        self.lable2.bind ('<1>', lambda self: bt1_msgbox())
        self.lable2.grid(row=1, column=2)

        self.lable3 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable3.grid(row=2, column=0, pady=10)

        self.btn_open = tk.Button(tab, text="Select TPT and SPE .csv", width=30, height=2, activebackground=gold_color, bg = bt_col, command=self.open_files)
        self.btn_open.grid(row=3, column=2)

        self.lable4 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable4.grid(row=4, column=0)

        self.lbl_TPT = tk.Label(tab, text = "TPT path:  ", bg = bg_col)
        self.lbl_TPT.grid(row=5, column=1)

        self.lbl_tpt = tk.Entry(tab, textvariable=tpt_string, width="75")
        self.lbl_tpt.grid(row=5, column=2)

        self.lbl_SPE = tk.Label(tab, text = "CSV path:  ", bg = bg_col)
        self.lbl_SPE.grid(row=6, column=1)

        self.lbl_csv = tk.Entry(tab, textvariable=spe_string, width="75")
        self.lbl_csv.grid(row=6, column=2)

        self.lable4 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable4.grid(row=7, column=0)

        self.btn_run_tab1 = tk.Button(tab, text="Create equivalence class",state = DISABLED, activebackground=bt_col, width=30, height=2, command=self.call_run, bg = bt_col)
        self.btn_run_tab1.grid(row=8, column=2)

        self.lable5 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable5.grid(row=9, column=0)

        self.btn_mapping_tab1 = tk.Button(tab, text="Create mapping",state = DISABLED, activebackground=bt_col, width=30, height=2, command=self.call_mapping, bg = bt_col)
        self.btn_mapping_tab1.grid(row=10, column=2)

        self.lable6 = tk.Label(tab, text = "      ", bg = bg_col)
        self.lable6.grid(row=11, column=0, pady=25)

        self.btn_openExp = tk.Button(tab, state = DISABLED ,text="Open TPT file", activebackground=bt_col, width=20, height=2, command=self.openTPT, bg = bt_col)
        self.btn_openExp.grid(row=12, column=2, sticky=W) 

        self.btn_quit = tk.Button(tab, text="Quit", activebackground=gold_color, width=20, height=2, command=tb_call_quit, bg = bt_col)
        self.btn_quit.grid(row=12, column=2, sticky=E)

    def call_run(self):
        location_tpt_tab1 = tpt_string.get()
        location_csv_tab1 = spe_string.get()
        os.chmod( location_tpt_tab1, stat.S_IWRITE )
        if len(location_tpt_tab1) > 1 and len(location_csv_tab1) > 1: 
            self.run(location_tpt_tab1,location_csv_tab1)
            self.btn_mapping_tab1.config(state=ACTIVE)
            self.btn_openExp.config(state=ACTIVE)
        else:
            showerror("Alert","Can not found location of TPT or CSV \nPlease click Open file and select location")
            return 0

    def call_mapping(self):
        location_tpt_tab1 = tpt_string.get()
        location_csv_tab1 = spe_string.get()
        os.chmod( location_tpt_tab1, stat.S_IWRITE )
        self.mapping_signals(location_tpt_tab1,location_csv_tab1)
        self.btn_openExp.config(state=ACTIVE)

    def open_files(self):
        try:
            tpt_path = askopenfilename(title = "Select TPT file", filetypes=[("TPT file","*.tpt")]) 
            spe_path = askopenfilename(title = "Select SPE file .csv", filetypes=[("SPE file","*.csv")]) 

            tpt_string.set(tpt_path)
            spe_string.set(spe_path)

            if len(tpt_path) > 1 and len(spe_path) > 1:
                self.btn_run_tab1.config(state=ACTIVE)

            return tpt_path, spe_path

        except NameError:
            messagebox.showerror("NameError","No SPE file found in the TC folder")
        except FileNotFoundError:
            messagebox.showerror("FileNotFoundError","No TPT file was selected")
        except:
            messagebox.showerror("Unexpected error:", sys.exc_info()[0])

    def SPE_signals(self,spe_file):
        SPE = dict()
        try:
            SPE_content = list(csv.DictReader(open(spe_file,"r")))
        except:
            return 0

        keys = ['name','portType','physMin','physMax','dataType']
        for key in keys:
            if key not in SPE_content[0].keys():
                return 0

        for signal in SPE_content:
            if ('_IN'in signal["portType"]):
                temp_dict = dict()

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

                if "Int" in signal["dataType"]:
                    temp_dict["physMin"] = long(signal["physMin"])
                    temp_dict["physMax"] = long(signal["physMax"])
                else:
                    temp_dict["physMin"] = float(signal["physMin"])
                    temp_dict["physMax"] = float(signal["physMax"])    
                temp_dict["dataType"] = signal["dataType"]            

                SPE[signal["name"]] = temp_dict

        return SPE

    def run(self,tpt_file, spe_file):
        global SPE_Dict
        try:

            SPE_Dict = self.SPE_signals(spe_file)
            if SPE_Dict == 0:
                messagebox.showinfo("Execution fail","The csv file do not have correct format")
                return 0

            message = []
            f = open(tpt_file,'r',encoding='utf-8')
            message = f.readlines()
            global tpt_17_on 
            # elimina caracterele non asci si pune spatiu!!!!
            # for index,lin in enumerate(message):
            # message[index]= re.sub(r'[^\x00-\x7F]+',' ', lin)

            ec_start = 0
            ec_end = 0
            counter_equiv_create = 0
            counter_modify_class = 0

            for count,line in enumerate(message):
                if 'equivalence-class-sets seed-value="0"' in line:
                    ec_start = count 
                if '<equivalence-class-sets' in line:
                    ec_start = count   
                if '</equivalence-class-sets>' in line:
                    ec_end = count
                if 'applicationVersion=' in line:
                    tpt_17_on = re.search(r'applicationVersion="(.*?)u', line).group(1)
                    
            if ec_start < 10:
                messagebox.showerror("Error","Error equivalence class! Missing ec_sart tag \n Please contact  Nica Robert or Falamas Ovidiu !!")
                return 0

            if ec_start != 0 and tpt_17_on != "17":
                message[ec_start] = '  <equivalence-class-sets seed-value="0" use-seed="false">\n'
                
            if ec_start != 0  and tpt_17_on == "17":
                message[ec_start] = '  <equivalence-class-sets>\n'
            
            if ec_end == 0 :
                message.insert(ec_start+1, '  </equivalence-class-sets>\n') 

            for count,line in enumerate(message):
                if '<equivalence-class-sets seed-value="0"' in line:
                    ec_start = count  
                if '</equivalence-class-sets>' in line:
                    ec_end = count

            count_end = ec_start
            text_signal_search = list()

            for key in SPE_Dict:
                uuid_id_eqv = uuid.uuid1()
                # daca semnalul este de tip boolean, nu ii creaza clasa de echivalenta
                # pentru semnalele de tip boolean avem o singura clasa de echivalenta "Boolean"
                if "BOOL" in SPE_Dict[key]['dataType'].upper():
                    continue

                channel_name = ''
                channel_name = ('<channel log="true" name="{}"'.format(key))
                flag_exist_signal = 0
                flag_uint = 0

                # Search if the signal is declarate in TPT
                for signal in message:
                    if channel_name in signal:
                        flag_exist_signal = 1

                if flag_exist_signal == 0:
                    text_signal_search.append('\n < {} > - do not create equivalance class becase do not exist in TPT declaration\n'.format(key))
                    continue

                globals()['%s_physMax' % key] = (SPE_Dict[key]['physMax'])
                globals()['%s_physMin' % key] = (SPE_Dict[key]['physMin']) 

                physMin = str(SPE_Dict[key]['physMin'])
                physMax = str(SPE_Dict[key]['physMax'])
                dtmin = 'dtmin'

                if ("UInt" in SPE_Dict[key]['dataType']) and (long(SPE_Dict[key]['physMin'])> 0):
                    dtmin = '0'
                elif ("UInt" in SPE_Dict[key]['dataType']):
                    flag_uint = 1
                    dtmin = 'dtmin'

                if (long(SPE_Dict[key]['physMax'])) > 1e+20 and long((SPE_Dict[key]['physMin'])) < 0:
                    rep_val =  0
                elif (long(SPE_Dict[key]['physMax'])) > 1e+20 and long((SPE_Dict[key]['physMin'])) == 0:
                    rep_val =  100
                else:
                    rep_val =  long((SPE_Dict[key]['physMin'] + SPE_Dict[key]['physMax'])) / 2

                if not("Float" in SPE_Dict[key]['dataType']):
                    rep_val = int(round(rep_val))

                ec_strings = [] 
                ec_name_eq = ('   <equivalence-class-set name="{}"'.format(key)) 
                if tpt_17_on == '17':
                    ec = ec_name_eq + ' uuid="'+str(uuid_id_eqv)+'">\n'
                else:
                    ec = ec_name_eq + '>\n'
                ec_strings.append(ec)

                range_neg = 'name="Out_Range_negative"'
                in_range = 'name="In_Range"'
                range_pos = 'name="Out_Range_positive"'
                
                # if the signal is uint and physMin is 0 do not create negativ interval
                if flag_uint == 0:
                    ec = ('    <equivalence-class group="" interval="[{}, {}[" {}/>\n'.format(dtmin,physMin,range_neg))
                    ec_strings.append(ec)

                ec = ('    <equivalence-class group="" interval="[{}, {}]" {} representative="{}"/>\n'.format(physMin,physMax,in_range,rep_val))
                ec_strings.append(ec)
                ec = ('    <equivalence-class group="" interval="]{}, dtmax]" {}/>\n'.format(physMax,range_pos))
                ec_strings.append(ec)
                ec = ('   </equivalence-class-set>\n')
                ec_strings.append(ec)
                
                index_eq = -1

                for count,signal in enumerate(message):
                    if ec_name_eq in signal:
                        index_eq = count

                for count,line in enumerate(message):
                    if 'equivalence-class-sets seed-value="0"' in line:
                        ec_start = count 

                #verifica daca clasa exista deja, daca nu exista -1, altfel index_eq > 0    
                if index_eq == -1:
                    counter_equiv_create += 1
                    for strlist in reversed(ec_strings):
                        message.insert(ec_start+1, str(strlist))  

                # daca clasa exista > 0 vor fi inlocuite doar valorile clasei, in cazul in care acestea sunt schimbate        
                elif index_eq > 0:
                    del ec_strings[0]
                    del ec_strings[-1]
                    index_delet  = index_eq
                    for i in range(1,20):
                        if '</equivalence-class' in message[index_delet +1]:
                            break
                        elif range_neg in message[index_delet +1] or in_range in message[index_delet +1] or range_pos in message[index_delet +1]:
                            del message[index_delet +1]
                        else:
                            index_delet += 1
                            continue
                        if i == 19 :
                            showerror("Alert !!","Do not found </equivalance-class tag")
                            return 0
                            
                    for strlist in ec_strings:
                        index_eq = index_eq + 1
                        message.insert(index_eq, str(strlist))  

            index_bool = 0
            for count,line in enumerate(message):
                if ec_start != 0 and tpt_17_on != "17":
                    message[ec_start] = '  <equivalence-class-sets seed-value="0" use-seed="false">\n'
                    
                if ec_start != 0  and tpt_17_on == "17":
                    message[ec_start] = '  <equivalence-class-sets>\n'
                    
                if '   <equivalence-class-set name="Boolean"' in line:
                    index_bool = 1
                if tpt_17_on == "17":
                    if '  <equivalence-class-sets>' in line:
                        index_start = count
                else:
                    if '  <equivalence-class-sets seed-value="0" use-seed="false">' in line:
                        index_start = count

            if index_bool == 0:
                if tpt_17_on == "17":
                    uuid_id_eqv = uuid.uuid1()
                    str_bool = ['   <equivalence-class-set name="Boolean"'+ ' uuid="'+str(uuid_id_eqv)+'">\n','    <equivalence-class group="" interval="[true, true]" name="True"/>\n','    <equivalence-class group="" interval="[false, false]" name="False"/>\n','   </equivalence-class-set>\n']
                else:
                    str_bool = ['   <equivalence-class-set name="Boolean">\n','    <equivalence-class group="" interval="[true, true]" name="True"/>\n','    <equivalence-class group="" interval="[false, false]" name="False"/>\n','   </equivalence-class-set>\n']
                
                for boolstring in str_bool:
                    index_start += 1    
                    message.insert(index_start,str(boolstring))
    
            with codecs.open(tpt_file, 'w', encoding='utf8') as f:
                for item in message:
                    f.write(str(item))

            message_info = "Done!\nWere created {} new equivalance classess \n\n".format(counter_equiv_create)

            for text in text_signal_search:
                if len(text) > 0:
                    message_info = message_info  + text                      

            messagebox.showinfo("Execution done!",message_info)

        except Exception as e:
            messagebox.showerror('Error',e)

    def mapping_signals(self,tpt_file,spe_file):

        global SPE_Dict
        
        list_error_mapping = list()
        f = open(tpt_file,'r')
        message = f.readlines()
        f.close()
        count_mapping_element = 0
        count_delete_mapping = 0
        ec_start = 0
        ec_end = 0
        global tpt_17_on
        
        if len(SPE_Dict) > 0:
            key_SPE = SPE_Dict
        else:
            key_SPE = self.SPE_signals(spe_file)

        for count,list_elem in enumerate(message):
            if 'applicationVersion=' in list_elem:
                tpt_17_on = re.search(r'applicationVersion="(.*?)u', list_elem).group(1)
            if '  <mapped-object-equivalence-class-sets' in list_elem:
                ec_start = count
                message[ec_start] = '  <mapped-object-equivalence-class-sets>\n'

            elif '  </mapped-object-equivalence-class-sets' in list_elem:
                ec_end = count

        if ec_start < 10:
                messagebox.showerror("Error","Error mapping! Please contact Nica Robert or Falamas Ovidiu !!")
                return 0

        for key in key_SPE:
            ec_name_eq_map = ('   <equivalence-class-set name="{}"'.format(key)) 
            ec_name_bool = ('   <equivalence-class-set name="Boolean"') 
            get_map_uuid = key
                        
            text_missing_var = ''
            mapp = ''
            channel_name = ''
            
            if tpt_17_on == '17' : 
                for count,line in enumerate(message):
                    if ec_name_eq_map in line:
                        get_map_uuid = re.search(r'uuid="(.*?)">', line).group(1)
                        continue
                    if ec_name_bool in line and "BOOL" in SPE_Dict[key]['dataType'].upper():
                        get_map_uuid = re.search(r'uuid="(.*?)">', line).group(1)
                        continue
                    

                    
            channel_name = ('<channel log="true" name="{}"'.format(key))
            mapp_sig = ('mapped-object="{}"'.format(key))
            if tpt_17_on == '17' : 
                equivalance_exist = ('<equivalence-class-set name="{}" uuid="{}">'.format(key,get_map_uuid))
            else:
                equivalance_exist = ('<equivalence-class-set name="{}">'.format(key))

            flag_exist_signal = 0
            flag_exist_equivalence = 0

                    
            if "BOOL" in SPE_Dict[key]['dataType'].upper():
                #verifica daca exista semnalul mapat, daca exista il sterge :)
                for count_bool,keys in enumerate(message):
                    if  mapp_sig  in keys:
                        del message[count_bool]
                        count_delete_mapping += 1


                mapp = ('   <mapped-object-equivalence-class-set equivalence-class-set="{}" mapped-object="{}"/>\n'.format(get_map_uuid,key))
                message.insert(ec_start+1,mapp)
                count_mapping_element += 1
                ec_start += 1
                continue    

            for countt,keys in enumerate(message):
                # check if exist mapping signal to equivalence class in TPT
                if  mapp_sig  in keys:
                    count_delete_mapping += 1
                    del message[countt]

                # check if exist equivalence class in TPT
                if equivalance_exist in keys:
                    flag_exist_equivalence = 1

                # check if exist signal in TPT    
                if channel_name in keys:
                    flag_exist_signal = 1
                
            #create mapping 
            if flag_exist_signal == 1 and flag_exist_equivalence == 1:
                mapp = ('   <mapped-object-equivalence-class-set equivalence-class-set="{}" mapped-object="{}"/>\n'.format(get_map_uuid,key))
                message.insert(ec_start+1,mapp)
                count_mapping_element += 1
                ec_start += 1

            if flag_exist_equivalence == 0:
                text_missing_var = "\n< {} > - do not created mapping becase the signal do not equivalence class in  TPT\n".format(key)
            
            if len(text_missing_var) > 0:
                list_error_mapping.append(text_missing_var)

        #if do not exist close tag for mapping, insert !
        if ec_end == 0:
            message.insert(ec_start+1,'  </mapped-object-equivalence-class-sets>\n') 

        with open(tpt_file, 'w') as f:
            for item in message:
                f.write(str(item))

        count_mapping_element = count_mapping_element - count_delete_mapping
        message_mapping = 'Done!\nWere mapped {} signals'.format(count_mapping_element)
        for text in list_error_mapping:
            message_mapping = message_mapping + text

        messagebox.showinfo('Info',message_mapping)  

    def openTPT(self):

        tpt_dir = tpt_string.get()

        if not tpt_string:
            messagebox.showerror("FileNotFoundError","No TPT file was selected!")
        else:    
            os.startfile(tpt_dir)

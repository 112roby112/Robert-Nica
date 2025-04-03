import numpy as np
import scipy.io
from tkinter.messagebox import showerror
from future.types.newint import long
import csv
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import sys
import re

def SPE_signals():

    try:
        spe_path = askopenfilename(title = "Select SPE file .csv", filetypes=[("SPE file","*.csv")]) 

    except NameError:
        messagebox.showerror("NameError","No SPE file found in the TC folder")
    except FileNotFoundError:
        messagebox.showerror("FileNotFoundError","No TPT file was selected")
    except:
        messagebox.showerror("Unexpected error:", sys.exc_info()[0])
    
    index_s = spe_path.rfind('/')
    index_end = spe_path.rfind('.')
    name_mat = spe_path[index_s+1:index_end]
    name_mat = name_mat + '_all_signals_SPE.mat'

    SPE = dict()
    try:
        SPE_content = list(csv.DictReader(open(spe_path,"r")))
    except:
        return 0

    keys = ['name','portType','physMin','physMax','dataType']
    for key in keys:
        if key not in SPE_content[0].keys():
            return 0
    sum_grad = 0
    sample_time = 5

    for signal in SPE_content:
        if ("_IN" in signal["portType"].upper()) and ('_s_' in signal["name"] ):
            temp_dict = list()
            temp_dict.clear()
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
                
            
            out_of_range_positive = list()
            out_of_range_negative = list()

            out_of_range_positive.clear()
            out_of_range_negative.clear()

#            if '_s_' in signal["name"]:
#               signal["name"] = re.sub(r"_s_", "_", signal["name"])
#
#            signal["name"] = signal["name"] + '_Val'

         #   if 'RP_' in signal["name"]:
         #       signal["name"] = re.sub(r"RP_", "", signal["name"])

          #  if signal["dataType"].upper() == 'UINT8':
          #      signal["name"] = signal["name"] + '_u8Val'                
          #  elif signal["dataType"].upper() == 'UINT16':
          #      signal["name"] = signal["name"] + '_u16Val' 
          #  elif signal["dataType"].upper() == 'FLOAT32':
          #      signal["name"] = signal["name"] + '_f32Val'

            if "INT" in signal["dataType"].upper() :
                signal_physMin = float(signal["physMin"])
                signal_physMax = float(signal["physMax"])

                signal_physMin = int(signal_physMin)
                signal_physMax = int(signal_physMax)

                gradian_phys = int(((signal_physMax + abs(signal_physMin)) * 0.01) + sum_grad)
                sum_grad += 1
                if sum_grad > 20:
                    sum_grad = 0
            else:
                signal_physMin = float(signal["physMin"])
                signal_physMax = float(signal["physMax"]) 
                
                gradian_phys = (((signal_physMax + abs(signal_physMin)) *0.01) + sum_grad)
                sum_grad += 0.01
                if sum_grad > 20:
                    sum_grad = 0

            physMin = signal_physMin
            physMax = signal_physMax

            if "BOOL" in signal["dataType"].upper():
                for i in range(100):
                    for j in range(15):
                        temp_dict.append(signal_physMax)
                    for j in range(15):
                        temp_dict.append(signal_physMin)
            else:
                # nu mai creaza out of range negativ

                if("UINT8" == signal["dataType"].upper() and (signal_physMax < 255)):
                    for i in range(150):
                        out_of_range_positive.append(signal_physMax+5)
                    
                elif("UINT16" == signal["dataType"].upper() and (signal_physMax < 65535)):
                    for i in range(150):
                        out_of_range_positive.append(signal_physMax+5)
                    
                elif("UINT32" == signal["dataType"].upper() and (signal_physMax < 4294967295)):
                    for i in range(150):
                        out_of_range_positive.append(signal_physMax+5)

                elif(("INT8" == signal["dataType"].upper() or "FLOAT8" == signal["dataType"].upper()) and (signal_physMax < 127)):
                    for i in range(150):
                        out_of_range_positive.append(signal_physMax+5)
                    
                elif(("INT16" == signal["dataType"].upper() or "FLOAT16" == signal["dataType"].upper()) and (signal_physMax < 32767)):
                    for i in range(150):
                        out_of_range_positive.append(signal_physMax+5)
                    
                elif(("INT32" == signal["dataType"].upper() or "FLOAT32" == signal["dataType"].upper()) and (signal_physMax < 2147483647)):
                    for i in range(150):
                        out_of_range_positive.append(signal_physMax+5)
                else:
                    
                    for i in range(150):
                        out_of_range_positive.append(signal_physMax)
                        
                        


                if ("UINT" in signal["dataType"].upper() and (signal_physMin > 1)):
                    for i in range(150):
                        out_of_range_negative.append(int(signal_physMin-1))
                        
                elif ("UINT" in signal["dataType"].upper() and (signal_physMin == 0)):
                    for i in range(150):
                        out_of_range_negative.append(int(0))

                elif(("INT8" == signal["dataType"].upper() or "FLOAT8" == signal["dataType"].upper()) and (signal_physMin > -128)):
                    for i in range(150):
                        out_of_range_negative.append(signal_physMin-5)
                    
                elif(("INT16" == signal["dataType"].upper() or "FLOAT16" == signal["dataType"].upper()) and (signal_physMin > -32768)):
                    for i in range(150):
                        out_of_range_negative.append(signal_physMin-5)
                    
                elif(("INT32" == signal["dataType"].upper() or "FLOAT32" == signal["dataType"].upper()) and (signal_physMin > -2147483648)):
                    for i in range(150):
                        out_of_range_negative.append(signal_physMin-5)
                elif "UINT" not in signal["dataType"].upper():
                    for i in range(150):
                        out_of_range_negative.append(signal_physMin-5)
                else:
                    for i in range(150):
                        out_of_range_negative.append(physMin)

                # add min
                for element in range(200):
                    temp_dict.append(physMin)

                grad_per_range = (physMax - physMin)/600
                gr = physMin 
                if "INT" in signal["dataType"].upper():
                    if int(grad_per_range) <= 0 :
                        grad_per_range = 1    
                    for a in range(0,600):
                        gr += int(grad_per_range)
                        if gr >= physMax:
                            gr = physMax
                        for i in range(5):
                            temp_dict.append(gr)
                else:
                    if int(grad_per_range) <= 0.5 :
                        grad_per_range = 0.5
                    for b in range(0,600):
                        gr += grad_per_range
                        if gr >= physMax:
                            gr = physMax
                        for i in range(5):
                            temp_dict.append(gr)
                        


                #1 add from out of range min  if exist to out of range max  value if exist, it is not exist min to max
#                elem_min = (physMin + physMax)/2
#                for element in range(100):
#                    if elem_min >= signal_physMax:
#                        elem_min = signal_physMax
#                        
#                    for i in range(15):
#                        if "INT" in signal["dataType"].upper():
#                            temp_dict.append(int(elem_min))
#                        else:
#                            temp_dict.append(elem_min)
#                    elem_min += gradian_phys


                for element in range(150):
                    if "INT" in signal["dataType"].upper():
                        temp_dict.append(int((physMin + physMax)/2))
                    else:
                        temp_dict.append((physMin + physMax)/2)

                for element in range(200):
                    temp_dict.append(physMax)    

#                elem_min = physMin
#                for element in range(100):
#                    if elem_min >= (physMin + physMax)/2:
#                        elem_min = (physMin + physMax)/2
#                        
#                    for i in range(15):
#                        if "INT" in signal["dataType"].upper():
#                            temp_dict.append(int(elem_min))
#                        else:
#                            temp_dict.append(elem_min)
#                    elem_min += gradian_phys
                
                sample_time += 2
                if sample_time >= 20 :
                    sample_time = 5
# out of range  out_of_range_negative + temp_dict + out_of_range_positive
            SPE[signal["name"]] =  temp_dict 

    SPE['StepSize'] = 0.005
    scipy.io.savemat(name_mat, mdict=SPE,oned_as='column')
    messagebox.showinfo("Done","The mat file was created")

SPE_signals()
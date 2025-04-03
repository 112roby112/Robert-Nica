from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk 
import uuid
import webbrowser
import os
from tkinter import *
from interface import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import tkinter as tk
import subprocess as sp
import re

#----------------------------START: Drawing interface------------------------------


# Write here revision of current build
global revision
revision = 'v1.20'

# Create Frame and Title of Frame
root = tk.Tk()
root.title("TPT ToolBox")

# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth() 
windowHeight = root.winfo_reqheight()
 
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/3 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/4 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))
root.resizable(False, False)

# Background color
color_bg ='#fcfcfc'
root.configure(background = color_bg)

# Tabs color
sky_color = "#291b47"
gold_color = "#f05e53"
color_tab = color_bg
white_color = color_bg
black_color = "#000000"

# Tabs style
style = ttk.Style()
style.theme_create( "beautiful", parent = "classic", settings ={

        "TNotebook": {"configure": {"tabmargins": [5, 5, 5, 0], "background":color_bg}}, 

        "TNotebook.Tab": {
            "configure": {"padding": [25, 10], "background": color_bg, "foreground": gold_color},
            "map":       {"background": [("selected", gold_color),  ('!active', sky_color), ('active', color_tab)], "foreground": [("selected", black_color),  ('!active', white_color), ('active', black_color)], "expand": [("selected", [1, 1, 1, 0])]}
                         }})
style.theme_use("beautiful")
style.layout("Tab", [('Notebook.tab', {'sticky': 'nswe', 'children': [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children': [('Notebook.label', {'side': 'top', 'sticky': ''})], })], })])

style.layout("TMenubutton", [
   ("Menubutton.background", None),
   ("Menubutton.button", {"children":
       [("Menubutton.focus", {"children":
           [("Menubutton.padding", {"children":
               [("Menubutton.label", {"side": "left", "expand": 1})]
           })]
       })]
   }),
])

# Background color
style.configure('TFrame', background = color_bg)

# Tabs
tab_parent = ttk.Notebook(root)

main = ttk.Frame(tab_parent)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)
tab5 = ttk.Frame(tab_parent)
tab6 = ttk.Frame(tab_parent)
tab7 = ttk.Frame(tab_parent)

tab_parent.add(main, text="MAIN")
tab_parent.add(tab1, text="Eq. Class.")
tab_parent.add(tab2, text="Assess. Stub")
tab_parent.add(tab3, text="Attrib. Upd.")
tab_parent.add(tab4, text="Req. Linker")
tab_parent.add(tab5, text="Scripts Upd.")
tab_parent.add(tab6, text="B2B Tol. Upd.")
tab_parent.add(tab7, text="Spec. Delta")

tab_parent.pack(expand=1, fill='both')   

#-----------------------------------END: TABS---------------------------------------

def tb_check_rev():
    desc = sp.getoutput("si viewhistory --fields=revision --project=#/ChassisControl_Process#01_Engineering_Process/03_Test/03_Test_Tools/46_TPT_Toolbox --batch tpt_toolbox.exe") 

    last_rev = desc.split('\n')
    rev_int = last_rev[1]
    rev_hrd = revision.lstrip("v")

    if (rev_int == rev_hrd):
        messagebox.showinfo("Information", "Your version is up to date, no update required!")
    else:
        messagebox.showinfo("Information", "A newer version (revision" + rev_int + ") is available!")
        webbrowser.open("integrity://mksprod.in.audi.vwg:7001/si/viewproject?project=%2FChassisControl_Process%2F01_Engineering_Process%2F03_Test%2F03_Test_Tools%2F46_TPT_Toolbox%2Fproject.pj")

def tb_call_quit():
    global root
    root.destroy()

def tb_call_vers(event=None):
    text = """Bug-fixes/improvements:\n 
- Tab5 (Test Script Updater): Bugfix for ticking the desired checkboxes. Now it is working properly, you can select one or more options\n 
"""

    messagebox.showinfo("Release Notes: " + revision, text)

def tb_call_mail(event=None):
    recipient = 'extern.ovidiu.falamas@audi.de;'
    subject = 'TPT ToolBox'
    body = 'E.g. I\'ve received an error when trying to...'
    webbrowser.open("mailto:?to=" + recipient + "&subject=" + subject + "&body=" + body, new=1)

def createMenu(frame):
    menubar = Menu(frame)
    frame.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Check for updates", command=tb_check_rev, activebackground="#f05e53")   
    file_menu.add_command(label="Exit", command=tb_call_quit, activebackground="#f05e53")

    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View", menu=file_menu)
    file_menu.add_command(label="Release notes", command=tb_call_vers, activebackground="#f05e53")   

    about_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="How to", menu=about_menu)
    about_menu.add_command(label="Eq. Class. Creator", command=bt1_msgbox, activebackground="#f05e53")
    about_menu.add_command(label="Assess. Generator", command=bt2_msgbox, activebackground="#f05e53")
    about_menu.add_command(label="Attrib. Updater", command=bt3_msgbox, activebackground="#f05e53")
    about_menu.add_command(label="Req. Linker", command=bt4_msgbox, activebackground="#f05e53")
    about_menu.add_command(label="Scripts Updater", command=bt5_msgbox, activebackground="#f05e53")
    about_menu.add_command(label="B2B Tol. Updater", command=bt6_msgbox, activebackground="#f05e53")
    about_menu.add_command(label="Test Spec. Delta", command=bt7_msgbox, activebackground="#f05e53")
    
    help_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Ask for support", command=tb_call_mail, activebackground="#f05e53") 

def bt1_msgbox():
    st_bt1 = "This tool creates equivalence classes for each existing input signal inside TPT Declaration Editor, based on physMin and physMax from SPE export. Therefore, user can select, as well, to make the mapping between existing signals and new created equivalence classes.\n\n How to:\n 1. Export SPE into .csv file from ToolCenter\n 2. Select TPT file and than .csv file\n 3. Press on \"Create equivalence class\" button\n 4. Optional, you can choose to map created classes to signals"
    messagebox.showinfo("Equivalence Classes Creator",st_bt1)

def bt2_msgbox():
    st_bt2 = "This tool creates an export (.txt) of all requirements in a specific format which helps you to write asseslets faster. The script will make differences between preconditions and requirements.\n\n How to:\n 1. Export all items from SWRS into an Excel file\n 2. Select the .xls/.xlsx file as input for this script \n 3. Complete the \"asseslet author\" and \"SWRS baseline\" field\n 4. Press \"Run\" and then open the resulted file" 
    messagebox.showinfo("Stub Assesslet Generator",st_bt2)

def bt3_msgbox():
    st_bt3 = "First, this tool is reading all the existing attributes from a TPT file, then, when you have a new release and need to change some attributes, the script will update them on all platforms. \n\n How to:\n 1. As input, you have to select the TPT file\n 2. The script will show all the attributes from TPT\n 3. Change the value of any attribute or of all attributes\n 4. Press \"Update Attributes\" and open TPT to see the changes"  
    messagebox.showinfo("Execution Attributes Updater",st_bt3)

def bt4_msgbox():
    st_bt4 = "This tool is creating the linkage inside TPT, between requirements and assesslets and between requirements and test cases as well. Before using it, be sure that all requirements are imported and the TPT file is closed, otherwise you'll receive an error message. \n\n How to:\n 1. As input, you have to select the TPT file\n 2. The script will tell you if no requirements are imported\n 3. Press button \"Link Assesslets\" and wait until is done\n 4. Press button \"Link TestCases\" and wait until is done\n 5. Open TPT file to see the changes"  
    messagebox.showinfo("Automatic Requirements Linker",st_bt4)
    
def bt5_msgbox():
    st_bt5 = "This tool is updating the following scripts inside TPT: Original Model, Model Load, Test Run and Assesslet Dictionary_SPE. Before using it, be sure that your TPT file and TI_Project_Module.tpt is closed, otherwise you'll receive an error message. \n\n How to:\n 1. As input, you have to select the TPT file\n 2. Afterwards, select the TI_Project_Module.tpt file\n 3. Select which script you want to be update\n 4. Press \"Update selected options\" and wait until is done\n 5. Open TPT file to see the changes"  
    messagebox.showinfo("Test Scripts Updater",st_bt5)
    
def bt6_msgbox():
    st_bt6 = "This tool is populating for all Back 2 Back configurations the absolute tolerance and the time tolerance for all output signals. Optionally you can set 1 sample time deviation for all outputs. Be aware that the script is working only on module level, not on SWC level.\n\n How to:\n 1. As input, you have to select the TPT file\n 2. Click on checkbox for 1 sample time as time tolerance\n 3. Press on button \"Update B2B Tolerances\" \n 4. Open TPT file to see the changes"  
    messagebox.showinfo("Back 2 Back Tolerances Updater",st_bt6)

def bt7_msgbox():
    st_bt7 = "This tool generates an easier way to see changes between implementations based on test specifications. It is creating a delta, more exactly a report with differences found between two test specifications. Tool is having two options, working with local files or directly with members directly from Integrity. Be sure that your settings in Integrity at Host Name and Port are correct.\n\n How to:\n\n Work with local files: \n 1. Load your first version of test specification\n 2. Load your second version of test specification\n 3. Press on button \"Generate Delta\" \n\n Work with MKS members: \n 1. Press button \"Load available projects\" \n 2. From drop-down menu select your project \n 3. Bellow, select a specific module from drop-down menu \n 4. Select the 1st revision and the 2nd revision of test spec. \n 5. Click on \"Generate Delta\" "  
    messagebox.showinfo("Test Specification Delta",st_bt7)
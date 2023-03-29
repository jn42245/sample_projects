# Created on 6 December 2022
# Created by Thierry Tran
# The purpose of the script is to provide a graphical user interface for the hr report generator script
import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from datetime import datetime

# Internal module
from utils.generate_hr_reports import run_report


def main():

    wk_dir = os.path.dirname(os.path.abspath("__file__"))
    current_year = datetime.today().year

    root = tk.Tk()
    root.geometry('400x220')
    root.title('HR Reports Generator')
    root.iconbitmap(os.path.join(wk_dir, 'references', 'sqt.ico'))

    dropdown_options = [*range(current_year-2, current_year+4)]
    default_var = tk.StringVar()
    default_var.set(str(current_year))

    tk.Button(root, text="Select Word Template", command=load_word, width=20, font='Calibri 10').pack()
    tk.Button(root, text="Select Xlsx Raw Data", command=load_excel, width=20, font='Calibri 10').pack()
    tk.Button(root, text="Select Output Folder", command=output_folder, width=20, font='Calibri 10').pack()

    option_menu = tk.OptionMenu(root, default_var, *dropdown_options, command=select_year)
    option_menu.configure(width=18)
    option_menu.pack()

    run_button = tk.Button(root, text="GENERATE REPORTS", command=run,
              width=20, font='Calibri 10 bold', bg='#FF9999')
    run_button.pack(pady=8)

    tk.Button(root, text='Quit Application', command=root.quit, width=20, font='Calibri 10').pack()

    canvas = tk.Canvas(root, width=400, height=50)
    canvas.create_text(140, 30, text="Author: Thierry Tran (thtran@squaretrade.com) at SquareTrade Europe",
                       fill="black", font=('Calibri', '7'))
    canvas.pack()

    root.mainloop()

    return None

def load_excel():
    global path_raw_data
    path_raw_data = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                               filetypes=(("xlsx files", "*.xlsx"), ("All Files", "*.*")))
    return None


def load_word():
    global path_template
    path_template = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                               filetypes=(("docx files", "*.docx"), ("All Files", "*.*")))
    return None


def output_folder():
    global path_output
    path_output = filedialog.askdirectory(initialdir="/")
    return None


def select_year(selection):
    global year_input
    year_input = int(selection)
    return None


def run():
    run_report(Path(path_raw_data), Path(path_template),
               Path(path_output), year_input)
    return None


if __name__ == '__main__':
    main()
    
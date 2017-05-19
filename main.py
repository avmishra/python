from tkinter import *
from tkinter import ttk, filedialog, messagebox
import base64
import json
import os
from bs4 import BeautifulSoup
import requests
import shutil

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def downloadfile(file):
    # from git
    url = 'http://XXX.trendsys.in/developers/trendsutra3/raw/warpspeed/' + \
          file + '/?private_token='
    feurl = 'http://XXX.168.0.85:8080/trendsutra3/trunk/live_trendsutra3/' + file
    beurl = 'http://XXX.168.0.85:8080/trendsutra3/trunk/be_live_trendsutra3/' + file
    git_file = '/var/www/compare/git/' + file
    fe_file = '/var/www/compare/svn/fe/' + file
    be_file = '/var/www/compare/svn/be/' + file

    print(bcolors.OKGREEN + 'Downloading from GIT....' + url + bcolors.ENDC)

    r = requests.get(url, stream=True, timeout=10)
    if r.status_code == 200:
        os.makedirs(os.path.dirname(git_file), exist_ok=True)
        with open(git_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
    else:
        print(bcolors.FAIL + bcolors.BOLD + file + " not found" + bcolors.ENDC)

    print(bcolors.OKGREEN + 'Downloading from frond end....' + feurl + bcolors.ENDC)
    # from fe svn
    r = requests.get(feurl, stream=True, auth=('shobha.t',''), timeout=10)
    if r.status_code == 200:
        os.makedirs(os.path.dirname(fe_file), exist_ok=True)
        with open(fe_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
    else:
        print(bcolors.FAIL + bcolors.BOLD + file + " not found" + bcolors.ENDC)

    print(bcolors.OKGREEN + 'Downloading from back end....' + beurl + bcolors.ENDC)
    # from be svn
    r = requests.get(beurl, stream=True, auth=('shobha.t',''), timeout=10)
    if r.status_code == 200:
        os.makedirs(os.path.dirname(be_file), exist_ok=True)
        with open(be_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
    else:
        print(bcolors.FAIL + bcolors.BOLD + file + " not found" + bcolors.ENDC)


def remove_directory(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            if os.path.isfile(filepath):
                os.unlink(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath)
        except Exception as e:
            print(e)

def main_setup():
    # remove all directory
    print(bcolors.BOLD + 'Removing directories' + bcolors.ENDC)

    remove_directory('/var/www/compare/git')
    remove_directory('/var/www/compare/svn/fe')
    remove_directory('/var/www/compare/svn/be')

    read_data = _text.get("1.0","end-1c")
    for file in read_data.splitlines():
        downloadfile(file)
    # collect files in array
    # with open('/var/www/changedFiles.txt', 'r') as f:
    #     read_data = f.readlines()
    #     file_array = [x.strip() for x in read_data]
    #     for file in file_array:
    #         downloadfile(file)
    os.system('meld /var/www/compare/git /var/www/compare/svn/fe /var/www/compare/svn/be')

def exit_root():
    _root.destroy();

if __name__ == "__main__":
    _root = Tk()
    _root.title('Pepperfry comparison Tools')
    _mainframe = ttk.Frame(_root, padding='5 5 5 5')
    _mainframe.grid(row=0, column=0, sticky=(E, W, N, S))

    _files_frame = ttk.LabelFrame(_mainframe, text='List of Files', padding='5 5 5 5')
    _files_frame.grid(row=0, column=0, sticky=(N, S, E, W))

    clipboard_text = _root.clipboard_get()

    _text = Text(_files_frame, height=30, width=130)
    _text.insert(INSERT, clipboard_text)
    _text.pack()

    _compare_btn = ttk.Button(_mainframe, text='Compare', command=main_setup)
    _compare_btn.grid(row=1, column=0, sticky=W, pady=5)

    _exit_btn = ttk.Button(_mainframe, text='Exit', command=exit_root)
    _exit_btn.grid(row=1, column=1, sticky=E, pady=5)

    _root.mainloop()

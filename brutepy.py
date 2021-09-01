#!/usr/bin/python3 env
import os
import sys
import requests
import argparse
import time
import threading
import multiprocessing
from datetime import datetime

#__author__= 0xLog


###### ARGPARSE ######
######################
parser = argparse.ArgumentParser("bruteforce")
parser.add_argument('-u', '--url', metavar='', required=True, help="enter target url")
parser.add_argument('-w', '--wordlist', metavar='', required=True, help="path/wordlist/ example: /usr/share/wordlist/dirbuster/...")
parser.add_argument('-q', '--quiet', action='store_true', help='quiet mode; less informations are displayed')
parser.add_argument('-m', '--modi', type=int, nargs='+', help='enter numbers for specific status codes; example 400 500... looking only for this specific status code')
#FUTURE
parser.add_argument('-t', '--threads', metavar='', type=int, help='number of threads; default 20') #OR: multiprocessing
parser.add_argument('-x', '--extensions', type=str, nargs='+', help='add extensions like php,ssh,txt,js,css,... to the subdirectory')
parser.add_argument('-s', '--save', metavar='', help='save subdirectoy and status code')
parser.add_argument('-r', '--recursive', metavar='', help='recursive')
args = parser.parse_args()




###### INFRASTRUCTURE ######
############################
default_status_code_list = [200, 204,301,302,307,403]

#/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt




###### --FUNCTIONS--  #########
###############################
def check_valid_url(arg_url):
    if arg_url.startswith("https://"):
        return arg_url if arg_url.endswith("/") else arg_url + "/"

    elif arg_url.startswith("http://"):
        arg_url = arg_url[:4] + "s" + arg_url[4:]
        return arg_url if arg_url.endswith("/") else arg_url + "/"

    else:
        arg_url = "https://" + arg_url
        return arg_url if arg_url.endswith("/") else arg_url + "/"



#default status code list -or- user status code
def select_status_list(modi):
    if modi == None:
        return default_status_code_list
    else:
        return modi


# main func
def status_code_handler_dir(url, wordlist, modi, quiet):
    base_url = check_valid_url(url)
    status_code_list = select_status_list(modi)
    wordl_len = get_wordl_len(wordlist)
    banner()

    counter = 0
    with open(wordlist) as word:
        for subdirectory in word:
            if subdirectory.startswith("#") or subdirectory.startswith("\n"):   #sort out comments in public wordlists
                pass
            else:
                full_url_request =  base_url  + subdirectory[:-1]               #build request url
                request = requests.get(full_url_request)
                status_code = request.status_code                               #get status code :int:

                if status_code in status_code_list:
                    print("[+] " + str(status_code) + "  :  "  + subdirectory[:-1] if quiet==True else "[+] " + str(status_code) + "  :  " + full_url_request)
                counter += 1

                print("[*]",counter, "from", wordl_len, end="\r")
        print("\n[*] End: " + datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))




###### Banner/DisplayInfo/Info #######
######################################
def banner():
    print('\033[0;34m', "___             _         _ __  _  _ ")
    print("| _ ) _ _  _  _ | |_  ___ | '_ \| || |")
    print("| _ \| '_|| || ||  _|/ -_)| .__/ \_. |")
    print("|___/|_|   \_._| \__|\___||_|    |__/ ")
    print("\033[0m")
    print("=====================================================")
    print("Brutepy by 0xLog")
    print("=====================================================")
    print("[+] Mode         : dir")
    print("[+] Url          : {}".format(args.url))
    print("[+] Wordlist     : {}".format(args.wordlist))
    print("[+] Extensions   : {}".format(args.extensions if args.extensions != None else "NO extensions"))
    print("[+] Start        : {}".format(datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
    print("=====================================================")
    print("=====================================================")



def get_wordl_len(wordl):
    wcounter = 0
    with open(wordl) as f:
        for i in f:
            if i.startswith("#") or i.startswith("\n"):
                pass
            else:
                wcounter += 1
        return wcounter





if __name__ == "__main__":
    try:
        status_code_handler_dir(args.url, args.wordlist, args.modi, args.quiet)
    except requests.exceptions.ConnectionError as e:
        print("ERROR: url not valid; Name or Service not known")
        print(e)
    except requests.exceptions.MissingSchema as e:
        print(e)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

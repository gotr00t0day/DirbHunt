from colorama import Fore, Back, Style
from fake_useragent import UserAgent
import concurrent.futures
import requests
import time
import argparse
import sys
import datetime
import socket


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument('-w', '--wordlist', action='store',
                   type=str, help='wordlist to use',
                   metavar='wordlist.txt')

parser.add_argument('-e', '--extension', action='store',
                   type=str, help='files to search for',
                   metavar='.html')

parser.add_argument('-d', '--domain', action='store',
                    help="domain to check",
                    metavar="https://domain.com")

args = parser.parse_args()

ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}

datetime = datetime.datetime.now()

dt = datetime.strftime("%Y/%m/%d")
tm = datetime.strftime("%H:%M:%S")


def get_ip(domain: str):
    if "http" in domain:
        domain = domain.replace("http://", "")
    if "https" in domain:
        domain = domain.replace("https://", "")
    return socket.gethostbyname(domain)  

banner = """

    ____  _      __    __  __            __ 
   / __ \(_)____/ /_  / / / /_  ______  / /_
  / / / / / ___/ __ \/ /_/ / / / / __ \/ __/
 / /_/ / / /  / /_/ / __  / /_/ / / / / /_  
/_____/_/_/  /_.___/_/ /_/\__,_/_/ /_/\__/  
                                            
        V1.0

"""

gui = f"""
{Fore.CYAN}
===============================================================
{Fore.WHITE}
DirbHunt V1
by c0d3Ninja (@gotr00t0day)
{Fore.CYAN}
===============================================================
{Fore.WHITE}
[+] Url:            {args.domain}
[+] IP Address:     {get_ip(args.domain)}
[+] Wordlist:       {args.wordlist}
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     {str(ua.chrome)}
[+] Extensions:     {args.extension}
{Fore.CYAN}
===============================================================
{Fore.WHITE}
{dt} {tm} Starting DirbHunt
{Fore.CYAN}
===============================================================
{Style.RESET_ALL}
"""

try:
    with open(f"{args.wordlist}", "r") as f:
        wordlist = (x.strip() for x in f.readlines())
except FileNotFoundError:
    print(banner)
    print(gui)
    print(f"{Fore.RED} FILE {args.wordlist} NOT FOUND")
    sys.exit(0)


def get_request(url: str):
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        print(f'{Fore.GREEN} Found: {url}')
    else:
        print(Fore.RED + f"{url}")

def run_main(wordlist):
    link =  f"{args.domain}/{wordlist}"
    if "#" in wordlist:
        pass
    else:
        if args.domain:
            if args.wordlist:
                if args.extension:
                    extensions = f"{args.domain}/{wordlist}.{args.extension}"
                    wordlist
                    get_request(extensions)
                else:
                    wordlist
                    get_request(link)

                 
if __name__ == "__main__":
    try:
        print(Fore.CYAN + banner.strip("\n"))
        print(Style.RESET_ALL)
        print(gui + "\n")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(run_main, wordlist)
    except KeyboardInterrupt as err:
        sys.exit(0)
    except Exception as e:
        print(e)


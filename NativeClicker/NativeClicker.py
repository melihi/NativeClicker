import argparse
import NativeClickerBanner
import colorama
from colorama import Fore, Back
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import random
import time
import re
from bs4 import BeautifulSoup
import sys
from tqdm import tqdm
from tqdm import trange
import multiprocessing
from selenium.common.exceptions import TimeoutException
import numpy as np
'''
###########################################
#        github.com/melihi                #
#        melih isbilen 2021               # 
# All responsibility belongs to the user  # 
###########################################
'''
#prefixes
positive = Fore.GREEN  + "[+] " + Fore.RESET
info = Fore.BLUE + "[?] " + Fore.RESET
warning=Fore.LIGHTRED_EX + "[!] " + Fore.RESET
li = Fore.YELLOW + "[~] " + Fore.RESET

#print banner
test = NativeClickerBanner

country = {"ALL":"ALL" ,"AR":"Argentina" , "AU":"Australia" ,"BD":"Bangladesh" ,"BR":"Brazil" ,"KH":"Cambodia","CA":"Canada","CL":"Chile", "CO":"Colombia" ,"CZ":"Czech", "EU":"Europe", "FI":"Finland", "FR":"France ","DE":"Germany","GR":"Greece", "HK":"Hong Kong", "IN":"India", "ID":"Indonesia", "IR":"Iran", "IL":"Israel","IT":"Italy","JP":"Japan" ,"KZ":"Kazakhstan", "KE":"Kenya", "KR":"Korea" ,"MW":"Malawi","MY":"Malaysia","MX":"Mexico" ,"NZ":"New Zealand","PK":"Pakistan","PH":"Philippines","PL":"Poland","PT":"Portugal","RO":"Romania", "RU":"Russia","ES":"Spain", "CH":"Switzerland", "TW":"Taiwan", "TZ":"Tanzania", "TH":"Thailand", "TN":"Tunisia","TR":"Turkey","AE":"UAE","UA":"Ukraine","GB":"United Kingdom", "US":"United States", "VE":"Venezuela","VN":"Viet Nam"}

colorama.init(autoreset=True)

my_parser = argparse.ArgumentParser(
    description=Fore.GREEN+"NativeClicker automatically parsing  proxies and visits target addresses ."+Fore.RESET,
    epilog=Back.GREEN+" https://github.com/melihi  Melih Isbilen 2021 "+Back.RED+"\n All responsibility belongs to the user",
    usage="python3.9 NativeClicker.py -u https://www.youtube.com/watch\?v\=Nnj5OxXhysU -c all -a all -pl all  -pc 100 -v -sb -cl '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[3]/div/ytd-player/div/div/div[25]/div[2]/div[1]/button'",
    prefix_chars="-",
    add_help=True,
)

my_parser.add_argument(
    "--url",
    "-u",
    dest="url",
    help="Destination url . ",
    action="store",
    type=str,
    required=True,
)
my_parser.add_argument(
    "--thread",
    "-t",
    dest="thread",
    help="Thread count . Default 5",
    action="store",
    type=int,
    default=5,
    required=False,
)
my_parser.add_argument(
    "--proxy-count",
    "-pc",
    dest="count",
    help="Parsed proxy number . Also this option is your visit count . Default 100 .",
    action="store",
    type=int,
    default=100,
    required=False,
)
my_parser.add_argument(
    "--delay",
    "-d",
    dest="delay",
    help="Random delay between visitings . Default 20 seconds",
    action="store",
    type=int,
    default=20,
    required=False,
)
my_parser.add_argument(
    "--click",
    "-cl",
    dest="click",
    help="Give xpath for click something in address . ",
    action="store",
    type=str,
    default="",
    required=False,
)
my_parser.add_argument(
    "--country",
    "-c",
    dest="country",
    help="Proxies country's . example AF,US,CZ . Default all",
    action="store",
    type=str,
    default="all",
    required=False,
)
my_parser.add_argument( 
    "--show-browser",
    "-sb",
    dest="show",
    help="Show browser . Default false ",
    action="store_true",
    default=False,
    required=False,
)
my_parser.add_argument(
    "--stay-connected",
    "-sc",
    dest="stay",
    help="Stay connected don't close browser . Default false ",
    action="store_true",
    default=False,
    required=False,
)
my_parser.add_argument(
    "--anonimity",
    "-a",
    dest="anonimity",
    help="Proxies anonimity levels  . all , level1 ,  level2  ,level3 . Default all",
    action="store",
    type=str,
    default="All",
    required=False,
)
my_parser.add_argument(
    "--protocol",
    "-pl",
    dest="protocol",
    help="Proxies protocols  . http , https , socks . Default all",
    action="store",
    type=str,
    default="All",
    required=False,
)
my_parser.add_argument(
    "--crawl-proxy",
    "-cp",
    dest="crawlproxy",
    help="Proxy for scraping proxies  .",
    action="store",
    type=str,
    default="",
    required=False,
)
my_parser.add_argument(
    "--verbose",
    "-v",
    dest="verbose",
    help="Verbose mode  . Default false ",
    action="store_true",
    default=False,
    required=False,
)

def print_Over(text):
    tqdm.write(text)
    
def verbose_Print(message):
    if args.verbose:
        tqdm.write(message)
        
def random_Useragent():
    line = open('useragents.txt').readlines()
    line2 = random.choice(line).replace("\n","")
    return line2



args = my_parser.parse_args()
URL = []

#Generate browser for parsing proxies
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", random_Useragent())
profile.accept_untrusted_certs = True
profile.set_preference("http.response.timeout", 10)
profile.set_preference("network.http.connection-timeout", 10)
opts = Options()  
if args.show == False:   
    opts.headless = True
    assert opts.headless  # Operating in headless mode
    
if len(args.crawlproxy) > 10:
    PROXY = args.crawlproxy
    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",}

browser = Firefox(options=opts,firefox_profile=profile) 



def split_Args():
    global country
    country = args.country.upper().split(",")
    i=0
    for co in country:
        if co.isalpha():    
            country[i]=co.upper()
            i = i+1
        else:
            browser.quit()
            sys.exit(warning+Back.RED+"Invalid country ."+Back.RESET+"\n Example : \n -c US,CZ,DE \n -c all")
        
    global anonimity
    anonimity = args.anonimity.split(",") 
    for anon in anonimity:
        if anon != "level1" and anon != "level2" and anon != "level3" and anon != "all":
            browser.quit()
            sys.exit(warning+Back.RED+"Invalid anonimity level ."+Back.RESET+"\n Example : \n -a level1,level2 \n -a all")
           
    global protocol
    protocol = args.protocol.split(",")
    for pro in protocol:
        if pro != "http" and pro != "https" and pro != "socks" and pro != "all":
            browser.quit()
            sys.exit(warning+Back.RED+"Invalid protocols ."+Back.RESET+"\n Example : \n -pl http,socks \n -pl http,https \n -pl all")
    


def create_Urls():
    base=("http://www.freeproxylists.net/?c={count}&pt=&pr={protoc}")
    if args.anonimity=="all" and args.protocol=="all" and args.country=="all":
        verbose_Print(info+"GitHub : ")
        URL.append("https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt?raw=true")
        URL.append("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt?raw=true")
        URL.append("https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt?raw=true")
        URL.append("https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt")
        verbose_Print(li+str(URL[-4:]))
    for i in range(1,6):
        verbose_Print(info+"Page : "+str(i))
        for count in country:
            for anon in anonimity:
                for protoc in protocol:
                    URL.append("http://free-proxy.cz/en/proxylist/country/"+count+"/"+protoc+"/ping/"+anon+"/"+str(i))
                    verbose_Print(li+str(URL[len(URL)-1]))
                    temp = base
                    if args.anonimity=="all" and args.protocol=="all":
                      temp = temp.replace("{protoc}", "")
                      temp = temp.replace("{count}","")
                      temp = temp + "&a[]=0&a[]=1&a[]=2&page="+str(i)
                    else:
                        temp = temp.replace("{protoc}", protoc)
                        temp = temp.replace("{count}",count)
                        temp = temp + "&a[]="+str(int(anon[-1])-1)+"&page="+str(i)
                URL.append(temp)
                verbose_Print(li+str(URL[len(URL)-1]))
    
   
    print_Over(info+"Fetching proxy list . . .")
    for address in URL:
        if  len(data) <= args.count:
            parse_Proxy(address)
        else :           
           break
    
    pbar1.close()
    browser.quit()
    print_Over(positive +"Proxy fetched succesfully . TOTAL : " + str(len(data)))
    save_Proxy()
    
def save_Proxy():
    print_Over(info+"Saving proxies to file . ")
    f = open("NativeCliceker_proxy_list.txt", "a")
    for pro in data:
        f.write(pro+"\n")
    f.close() 
    print_Over(positive+"Proxies saved to file . ")
    
def args_Info():
    print(info + "Target : "+str(args.url))
    print(info + "Thread : "+str(args.thread))
    print(info + "Proxy counts : " +str(args.count))
    print(info + "Random delay between connections : 0-"+str(args.delay))
    print(info + "Click addres : " +str(args.click[:30]))
    print(info + "Countries : " + str(country))
    print(info + "Show browser : " +str(args.show))
    print(info + "Stay connected : " +str(args.stay))
    print(info + "Protocols : " +str(protocol))
    print(info + "Proxy anonimity level : " +str(anonimity))
    print(info + "Total request : " +str(args.count))


global data
data = []

def parse_Proxy(address):
    try:
        browser.get(address)
        attrs1={"class":"DataGrid"}
        source = browser.page_source
        
        if len(source)<100  :
            print_Over(warning +Back.RED+"We hit something . Connection issue . ")
        elif len(data) <= args.count:
            soup = BeautifulSoup( source, 'html.parser')
            
            if "freeproxylists" in address:
                table = soup.find('table', attrs=attrs1)
            elif "github" in address:
                datax = browser.find_element_by_tag_name("pre").text
                datay = datax.split("\n")
                for dat in datay :
                    if len(data) < args.count:
                        if dat[3].isdigit():
                            data.append(dat)
                            pbar1.update(1)  
                            verbose_Print(li+dat+" --> github.com")
                    elif len(data)>=args.count:
                        browser.quit()
                        break
                
                return
            else:
                table = soup.find('table', attrs={'id':'proxy_list'})
                table_body = table.find('tbody')
                
            rows = table_body.find_all('tr')
            for row in rows :
                if len(data) >= args.count:
                    break
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                out = [ele for ele in cols if ele]
                data.append(out[0]+":"+out[1]) 
                
                if "freeproxylists" in address:
                    #verbose_Print(li+" , ".join(data[-1])+" --> freeproxylists.com")
                    verbose_Print(li+" , ".join(out)+" --> freeproxylists.com")
                    
                else:
                    #verbose_Print(li+" , ".join(data[-1])+" --> free-proxy.cz")
                    verbose_Print(li+" , ".join(out)+" --> free-proxy.cz")
                
                if "We are sorry" in data[-1] or len(data[-1]) < 5:
                    del data[-1]  
                else:
                    if len(data) < args.count :
                        pbar1.update(1)
                    
    except:
        print_Over(warning ++Back.RED+"Some thing went wrong while proxy fetching !")
        
    finally:
        return
        


def click_Engine(*gen):
    global pbar2
    pbar2=tqdm(range(len(gen)),leave=True,dynamic_ncols=True,desc="Proxy connection status : "+multiprocessing.current_process().name, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET))
    for data in gen :
        usera = random_Useragent()
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", usera)
        profile.set_preference("http.response.timeout", 35)
        profile.set_preference("network.http.connection-timeout",60)
        profile.set_preference("permissions.default.image", 2)
        profile.accept_untrusted_certs = True
        opts = Options()
        if args.show == False:     
            opts.headless = True
            assert opts.headless  # Operating in headless mode
      
        try:
            PROXY=data
            webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                "httpProxy": PROXY,
                "ftpProxy": PROXY,
                "sslProxy": PROXY,
                "proxyType": "MANUAL",} 
                
            browser = Firefox(options=opts,firefox_profile=profile)
            pbar2.update(1)
            browser.get(args.url)
            print_Over(positive +Back.GREEN+ " Connection finished  "+Back.RESET+"\n      ↳ "+Back.GREEN+usera[:50]+"..."+Back.RESET+" \n        ↳ "+Back.GREEN+str(PROXY)+Back.RESET)
            if args.click != "":
                print_Over("         ↳ Cicking to button . . .")
                clickto = webdriver.find_elements_by_xpath(args.click)[0]
                clickto.click()
               
                
            time.sleep(random.randint(0, args.delay))
            if args.stay == False:    
                browser.quit()
                    
        except TimeoutException:    
            print_Over(warning+Back.RED+"Request time out error !  "+Back.RESET+"\n     ↳ "+Back.RED+usera[:50]+"..."+Back.RESET+" \n        ↳ "+Back.RED+str(PROXY)+Back.RESET)
            #browser.quit()
        except Exception as ex:
            print_Over(warning+Back.RED+"Connection error !  "+Back.RESET+"\n      ↳ "+Back.RED+usera[:50]+"..."+Back.RESET+" \n"+Back.RESET+"        ↳ "+Back.RED+ str(PROXY)+Back.RESET)
            browser.quit()

def engine_Manager():
      
    #if args.stay:
        #args.thread = args.count
    global processes
    processes = []
    za=0
    num = int(len(data) / args.thread)
    arr = np.array(data)

    arr2 =[]
    for xa in range(0,len(arr)):
        try: 
            arr2.append(arr[range(za, za+num)])
            za +=num
        except:
            break  
    
    for i in arr2:
        process = multiprocessing.Process(target=click_Engine, args=(i))
        process.start()
        processes.append(process)
        verbose_Print(li+Back.GREEN+" Process started : "+str(processes[len(processes)-1]) + " Task "+str(len(i))+Back.RESET)
         
def input_Checker(): 
    
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, args.url) is not None:
         
        split_Args()
        args_Info()
        global pbar1
        pbar1=tqdm(range(args.count),leave=True,dynamic_ncols=True,desc="Proxy fetch status : ", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET))  
        create_Urls()
        engine_Manager()
    else:
        sys.exit(warning + str(" Invalid url ."))


input_Checker()



 

![alt text](https://raw.githubusercontent.com/melihi/NativeClicker/main/Untitled4.png?raw=true)
# NativeClicker
NativeClicker automatized web traffic generator . NativeClick parse proxies from the following addresses :

- [free-proxy.cz](http://free-proxy.cz)
- [freeproxylists.com](http://free-proxy.cz)
- [github.com/clarketm](https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt?raw=true)
- [github.com/TheSpeedX](https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt?raw=true)
- [github.com/ShiftyTR](https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt?raw=true)
- [github.com/hookzof](https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt)

After parsing process creates selenium browser and connect to target .

### Dependencies 

- Selenium
- tqdm
- colorama
- BeautifulSoup
- multiprocessing
- numpy

### Installation
0. Install selenium webdriver
   ```bash
   sudo pacman -S selenium
   ```
1. After installing requirements ,
2. Clone the repo
   ```sh
   git clone https://github.com/melihi/NativeClicker.git
   ```
3. Change directory to :
   ```sh
   cd NativeClicker
   ```
4. Make executeable
   ```bash
   chmod +x NativeClicker.py
   ```
5. Run
   ```bash
   python3.9 NativeClicker.py -u http://test.com -c all -pl all -a all -pc 100 -t 10 -v
   ```


### Success rate 
NativeClicker's success rate directly depends to the proxies qualities .





### Commands & Arguments


![help](https://raw.githubusercontent.com/melihi/NativeClicker/main/help.png?raw=true)



### DEMO VIDEO
[![NativeClicker](https://i.ytimg.com/vi/HU9tFfUl3wI/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD8xu_ibKPiA5v2Z8O0Z0bOOAKjXQ)](https://youtu.be/HU9tFfUl3wI "NativeClicker")




Note All responsibility belongs to the user .

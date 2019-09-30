import re
import requests
from datetime import datetime


# http://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate=2019092912&row=436&col=181&lang=en
# http://www.meteo.pl/um/ramka_um_city_pl.php // get UM_SYYYY, ..., UM_SST; start_time
site_url = "http://www.meteo.pl/meteorogram_um.php"
img_url = "http://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate={}&row={}&col={}&lang=en"
#.format(date, row, col)
sst_url = "http://www.meteo.pl/um/ramka_um_city_pl.php"

# <div class="lista_A" onmouseover="this.style.cursor='pointer'; this.className='lista_B'" onmouseout="this.className='lista_A'" onclick="showMgram(1569793456, 181, 436 ,'Wroc%B3aw') " style="cursor: pointer;"> Wroclaw </div>
# <div class="lista_A" onMouseOver="this.style.cursor='pointer'; this.className='lista_B'" onMouseOut="this.className='lista_A'"onClick="showMgram(1569796755, 181, 436 ,'Wroc%B3aw') " > Wrocław </div>
pattern = re.compile(r'^<div class=\"lista_A\" onMouseOver=\"this.style.cursor=\'pointer\'; this.className=\'lista_B\'\" onMouseOut=\"this.className=\'lista_A\'\"\nonClick=\"showMgram\((\d+), (\d+), (\d+) ,\'Wroc%B3aw\'\) \" > Wroc.*aw </div>', re.MULTILINE)
sst_pattern = re.compile(r'^<script language=\'JavaScript\'>var UM_YYYY=\d+;var UM_MM=\d+;var UM_DD=\d+;var UM_ST=\d+;var UM_SYYYY=\"(\d+)\";var UM_SMM=\"(\d+)\";var UM_SDD=\"(\d+)\";var UM_SST=\"(\d+)\";</script>', re.MULTILINE)

REQ_HEADERS = {
    'Host': 'www.meteo.pl',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'User-Agent': 'Mozilla/5.0 (PlayStation 4 5.55) AppleWebKit/601.2 (KHTML, like Gecko)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-US,en;q=0.8,pl;q=0.6',
}


def get_meteo():
    sy = ""
    sm = ""
    sd = ""
    sst = ""
    response = requests.get(sst_url, headers=REQ_HEADERS.copy())
    if response.status_code == 200:
        result = sst_pattern.findall(response.text)
        if result:
            sy, sm, sd, sst = result.pop(0)
    response = requests.get(site_url, headers=REQ_HEADERS.copy())
    if response.status_code == 200 and sst:
        result = pattern.findall(response.text)
        if result:
            ts, col, row = result.pop(0)
            date = sy + sm + sd + sst
            response = requests.get(img_url.format(date, row, col), headers=REQ_HEADERS.copy())
            if response.status_code == 200:
                with open("meteo.png", "wb") as f:
                    f.write(response.content)
                return True
    return False


if __name__ == "__main__":
    get_meteo()

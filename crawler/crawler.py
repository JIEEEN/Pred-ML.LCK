import requests
import re
import os
from crawler.url import url
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from crawler.database import Data

team = ['Nongshim_RedForce', 'OKSavingsBank_BRION', 'Hanwha_Life_Esports',
        'T1', 'DRX', 'Kwangdong_Freecs', 'KT_Rolster', 'Liiv_SANDBOX',
        'Gen.G', 'Dplus_KIA']

def init_crawl():
    make_bsObject(url[0])

def make_bsObject(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print('HTTP Error', e) # 나중에  logging으로 대체
        return None
    try:
        bsObj = bs(html.read())
        lck_year = re.search(r'\d{4}', url)
        lck_season = re.search(r'\/(\w+)_Season\/(\w+)_Season\/', url)
        crawl_website_url1(bsObj, lck_year.group(), lck_season.group(2))
        crawl_website_url2(bsObj, lck_year.group(), lck_season.group(2))
    except AttributeError as e:
        print('AttributeError', e)
        return None
    
def crawl_website_url1(bsObj, lck_year, lck_season):
    # length = 171
    csv_data = []
    
    _datelist = bsObj.find_all('td', {'class':'mhgame-result'})
    datelist = []
    for i in range(len(_datelist)):
        datelist.append(_datelist[i].get_text())
    datelist = datelist[::5]
    
    
    _patch_versionlist = bsObj.find_all('a', href=True)
    pattern = r'/wiki/Patch_(\d+\.\d+)'
    patch_versionlist = []
    
    for item in _patch_versionlist:
        href = item['href']
        if re.match(pattern, href):
            patch_version = item.get_text()
            patch_versionlist.append(patch_version)
            
            
    temp = bsObj.find_all('a', {'class':'to_hasTooltip', 'data-to-flags': 'fiem'}, href=True)
    match_team_list = []
    for i in temp:
        item = re.sub(r'^/wiki/', '', i['href'])
        if item in team:
            match_team_list.append(item)
    match_team_list = match_team_list[8:]
    team1_list = match_team_list[0::3]
    team2_list = match_team_list[1::3]
    team_winlist = match_team_list[2::3]
    team1_winlist = [True if team1_list[i] == team_winlist[i] else False for i in range(len(team_winlist))]
    # team1_winlist -> team1_list와 같으면 True 아니면 False
    
    _picklist = bsObj.find_all('span', {'class':'sprite champion-sprite'})
    temp_picklist = []
    picklist = []
    for data in _picklist:
        temp_picklist.append(data['title'])
        
    for i in range(len(temp_picklist)):
        if (i//10)%2 == 1:
            picklist.append(temp_picklist[i])
        
    team1_top_champlist = picklist[0::10]
    team1_jungle_champlist = picklist[1::10]
    team1_mid_champlist = picklist[2::10]
    team1_adc_champlist = picklist[3::10]
    team1_support_champlist = picklist[4::10]
    
    team2_top_champlist = picklist[5::10]
    team2_jungle_champlist = picklist[6::10]
    team2_mid_champlist = picklist[7::10]
    team2_adc_champlist = picklist[8::10]
    team2_support_champlist = picklist[9::10]
    
    
    _playerlist = bsObj.find_all('a', {'class':'catlink-players pWAG pWAN to_hasTooltip'},href=True)
    playerlist = []
    for player in _playerlist:
        playerlist.append(player.get_text())
        
    team1_top_playerlist = playerlist[0::10]
    team1_jungle_playerlist = playerlist[1::10]
    team1_mid_playerlist = playerlist[2::10]
    team1_adc_playerlist = playerlist[3::10]
    team1_support_playerlist = playerlist[4::10]
    
    team2_top_playerlist = playerlist[5::10]
    team2_jungle_playerlist = playerlist[6::10]
    team2_mid_playerlist = playerlist[7::10]
    team2_adc_playerlist = playerlist[8::10]
    team2_support_playerlist = playerlist[9::10]
    
    
    # make init csv data
    csv_data = list(zip(datelist, patch_versionlist, team1_list, team2_list, team1_winlist,
                        team1_top_champlist, team1_jungle_champlist, team1_mid_champlist,
                        team1_adc_champlist, team1_support_champlist, team2_top_champlist,
                        team2_jungle_champlist, team2_mid_champlist, team2_adc_champlist, team2_support_champlist,
                        team1_top_playerlist, team1_jungle_playerlist, team1_mid_playerlist,
                        team1_adc_playerlist, team1_support_playerlist, team2_top_playerlist,
                        team2_jungle_playerlist, team2_mid_playerlist, team2_adc_playerlist, team2_support_playerlist,
                        ))
    
    # make new csv
    lck_csv = Data('lck{}_{}_data.csv'.format(lck_year, lck_season), csv_data)
    lck_csv.init_insert()
    
    
    return None

    
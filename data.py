import requests
from riotwatcher import LolWatcher
import time
import pandas as pd
from urllib import request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


# Riot API - needs to be updated every 24h
api_key = "RGAPI-8ebd0289-936a-4c07-83fb-72899a9f9809"


region_list = {
    "NA": ["na1","americas"], "EUW": ["euw1", "europe"],
    "EUN": ["eun", "europe"], "KR": ["kr","asia"],
    "BR": ["br1","americas"], "JP": ["jp1", "asia"],
    "RU": ["ru1", "europe"], "OCE": ["oc1","sea"],
    "TR": ["tr1","europe"], "LAN": ["la1","americas"],
    "LAS": ["la2","americas"], "PH": "ph2",
    "SG": ["sg2","sea"], "TH":["th2","sea"],
    "TW": ["tw2","sea"], "VN": ["vn2","sea"]}


# Approach 1: Use Riot API -> access player info -> get puuid -> get match
# Given summoner name and region, extract summoner info such as puuid
def get_summoner_info(summoner_name, region):
    region = region_list[region][0]
    api_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    resp = requests.get(api_url)
    # Summoner name not found
    if resp.status_code == 404:
        return None  
    else:
        player_info = resp.json()
        return player_info

# Given puuid, extract match id of the most recent 100 ranked matches
def get_match_id(puuid, region):
    mass_region = region_list[region][1]
    api_url = f"https://{mass_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count=100&api_key={api_key}"
    resp = requests.get(api_url)
    match_ids = resp.json()
    return match_ids

# Given match id and mass region, extract match info
def get_match_info(match_id, region):
    mass_region = region_list[region][1]
    api_url = f"https://{mass_region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"

    # Continue until get the match info
    while True:
        resp = requests.get(api_url)
        
        # whenever status code is 429, sleep for 10 seconds to wait for the rate limit
        if resp.status_code == 429:
            print("Rate Limit hit, sleeping for 10 seconds")
            time.sleep(10)
            continue       

        # if resp.status_code isn't 429,return the match data
        match_data = resp.json()
        return match_data

# Given summoner_id and region, extract summmoner stats, including tier, rank, LP, wins, losses
def get_summoner_stats(summoner_id, region):
    region = region_list[region][0]
    api_url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"
    resp = requests.get(api_url)
    summoner_stats = resp.json()
    return summoner_stats

# Get summary of summoner
def get_summary(summoner_name, region):
    # Approach 1 - Use Riot API
    player_info = get_summoner_info(summoner_name, region)
    # Player_info is None if no such player found
    if player_info: 
        puuid = player_info['puuid']
        summoner_id = player_info['id']
        stats = get_summoner_stats(summoner_id, region)
        if len(stats) != 0:
            ranked_stat = [stat for stat in stats if stat.get("queueType") == "RANKED_SOLO_5x5"]
            return ranked_stat[0]
        else: 
            return None
    else:
        return None

# Extract summoner's champion pool
def get_champion_pool(summoner_name, region):
    
    region = region_list[region][0]
    url = f"https://u.gg/lol/profile/{region}/{summoner_name}/champion-stats"

    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    req = Request(url,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, "html.parser")

    # Extract the champion table
    table = soup.find('div', {'role': 'table', 'class': 'content-section ReactTable ugg-table-2 profile-champion-stats-table'})
    # Extract the table content
    table_content = table.find('div', {'role': 'rowgroup'})

    # Extract all table rows
    table_rows = table_content.find_all('div', {'class': 'rt-tr-group'})

    champion_pool = pd.DataFrame(columns=['Champion', 'Win Rate', 'Wins', 'Losses', 'KDA', 'CS', 'Damage'])
    i = 1
    for row in table_rows:
        # Extract champion name and image
        champion = row.find('span', {'class': 'champion-name'}).text
        champion_img = row.find('img')['src']
        # Extract winrate
        winrate = row.find('div', {'class':'champion-rates'}).find('strong').text.strip()

        # Extract wins and losses
        match_record_span = row.find('span', {'class': 'match-record'})
        matches = match_record_span.text.strip()
        wins = matches.split()[0][:-1]
        losses = matches.split()[1][:-1]

        # Extract KDA
        kda_stat = row.find('div', {'class': 'kda'})
        strong_tags = kda_stat.find_all('strong')
        kda = strong_tags[0].text.strip()
        kill = strong_tags[1].text.strip()
        death = strong_tags[2].text.strip()
        assist = strong_tags[3].text.strip()

        # Extract CS, gold, and damage info
        cs_class = 'rt-td cs-cell'
        gold_class = 'rt-td gold-cell'
        damage_class= 'rt-td damage-cell'
        if i % 2 == 1:
            cs_class += ' is-in-odd-row'
            gold_class += ' is-in-odd-row'
            damage_class += ' is-in-odd-row'     
        cs = row.find('div', {'class': cs_class}).find('span').text
        gold = row.find('div', {'class': gold_class}).find('span').text
        damage = row.find('div', {'class': damage_class}).find('span').text
        i+=1

        # Append the dictionary to the dataframe
        champion_pool = champion_pool.append({'Champion': champion, 'Win Rate': winrate,'Wins': wins,
                        'Losses': losses,'KDA': kda,'CS': cs,'Damage': damage}, ignore_index=True)

    champion_pool.index = champion_pool.index + 1
    return champion_pool








#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
from flask import Flask

# CONSTANTS
MOTH_URL = "https://rocketleague.tracker.network/rocket-league/profile/steam/xmothsnok/overview"
BASE_URL_STEAM = "https://rocketleague.tracker.network/rocket-league/profile/steam/"
BASE_URL_XBOX = "https://rocketleague.tracker.network/rocket-league/profile/xbl/"
BASE_URL_PSN = "https://rocketleague.tracker.network/rocket-league/profile/psn/"
URL_END = "/overview"
app = Flask(__name__)
champ_icon = "🏆"
diamond_icon = "💎"
platinum_icon = "⭐"
gold_icon = "💛"
silver_icon = "⚪"
bronze_icon = "💩"


# Route for Moth
# In bot: !rank
@app.route('/')
def get_default_info():
    return get_response_data(MOTH_URL)


# Route for rank finder
# In bot: !rankfinder {platform} {username}
@app.route('/<platform>/<username>')
def get_info_by_user(platform, username):
    url = find_url_by_platform(platform, username)

    return get_response_data(url)


def find_url_by_platform(platform, username):
    if 'xbox' in platform.lower():
        url = BASE_URL_XBOX + username + URL_END
    elif 'steam' in platform.lower() or 'pc' in platform.lower():
        # TODO implement
        url = BASE_URL_STEAM + username + URL_END
    else:
        url = BASE_URL_PSN + username + URL_END
    return url


def get_response_data(url):
    json_dict = get_json_dict(url)
    profile_list = list(json_dict["stats-v2"]["standardProfiles"])[0]  # Agnostic profile name
    rank_values_list = retrieve_values(json_dict, profile_list)
    if len(rank_values_list) == 0:
        return "Data wasn't found for default user"
    single_string_info = ""
    for rank_info in rank_values_list:
        single_string_info += rank_info + "\n"
    return single_string_info


def get_json_dict(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")
    script_text = str(soup.find_all("script")[3].string)
    script_text = script_text[:script_text.find("};") + 1].replace("window.__INITIAL_STATE__=", "")

    return json.loads(script_text)


def retrieve_values(json_dict, profile_list):
    temp_list = []
    try:
        player_name = json_dict["stats-v2"]["standardProfiles"][profile_list]["platformInfo"]["platformUserHandle"]
        for value in list(json_dict["stats-v2"]["standardProfiles"][profile_list]["segments"]):
            metadata = value["metadata"]
            if "Ranked Standard 3v3" in metadata.values() \
                    or "Ranked Duel 1v1" in metadata.values() \
                    or "Ranked Doubles 2v2" in metadata.values():
                temp_list.append(get_string_of_values(metadata, value, player_name))
        return temp_list
    except:
        return []


def get_string_of_values(metadata, value, player_name):
    playlist_name = metadata["name"]
    rank_name = value["stats"]["tier"]["metadata"]["name"]
    rank_icon = get_rank_icon(rank_name)
    rank_division = value["stats"]["division"]["metadata"]["name"]
    mmr = str(value["stats"]["rating"]["value"])
    return player_name + "'s " + playlist_name + \
           ": " + rank_name + " " + rank_icon + "(" + rank_division + ") MMR: " + mmr


def get_rank_icon(rank_name):
    if "Champion" in rank_name:
        return champ_icon
    if "Diamond" in rank_name:
        return diamond_icon
    if "Platinum" in rank_name:
        return platinum_icon
    if "Gold" in rank_name:
        return gold_icon
    if "Silver" in rank_name:
        return silver_icon
    if "Bronze" in rank_name:
        return bronze_icon

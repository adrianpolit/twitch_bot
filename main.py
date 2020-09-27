#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_debug import Debug
from flask import request

# CONSTANTS
MOTH_URL = "https://rocketleague.tracker.network/rocket-league/profile/steam/xmothsnok/overview"
BASE_URL_STEAM = "https://rocketleague.tracker.network/rocket-league/profile/steam/"
BASE_URL_XBOX = "https://rocketleague.tracker.network/rocket-league/profile/xbl/"
BASE_URL_PSN = "https://rocketleague.tracker.network/rocket-league/profile/psn/"
URL_END_TRACKER = "/overview"
CHAMP_ICON = "🏆"
DIAMOND_ICON = "💎"
PLATINUM_ICON = "⭐"
GOLD_ICON = "🥇"
SILVER_ICON = "🥈"
BRONZE_ICON = "🥉"
UNRANKED_ICON = "❌"

app = Flask(__name__)


# Debug(app)
# app.run(debug=True)


# Route for Moth
# In bot: !rank
@app.route('/')
def get_default_info():
    return get_response_data(MOTH_URL)


# Route for rank finder
# In bot: !rankfinder {platform} {username}
@app.route('/finder')
def get_info_by_user():
    platform = request.args.get('platform')
    username = request.args.get('user')
    print('Got request to find ' + username + ' on ' + platform)
    url = find_url_by_platform(platform, username)

    return get_response_data(url)


def find_url_by_platform(platform, username):
    if 'xbox' in platform.lower():
        url = BASE_URL_XBOX + username + URL_END_TRACKER
    elif 'steam' in platform.lower() or 'pc' in platform.lower():
        url = get_steam_id64(username)
    else:
        url = BASE_URL_PSN + username + URL_END_TRACKER
    return url


def get_steam_id64(username):
    if 'https' in username:
        username += '?xml=1'
        xml = requests.get(username).content
        if not xml:
            raise Exception('Not a valid url')
        soup = BeautifulSoup(xml, features="lxml")
        steam_id = soup.find('profile').find('steamid64').string
        return BASE_URL_STEAM + steam_id + URL_END_TRACKER

    if len(username) == 17 and username.isnumeric():
        return BASE_URL_STEAM + username + URL_END_TRACKER

    raise Exception('Not a valid user')


def get_response_data(url):
    json_dict = get_json_dict(url)
    profile_list = list(json_dict["stats-v2"]["standardProfiles"])[0]  # Agnostic profile name
    rank_values_list = retrieve_values(json_dict, profile_list)
    if len(rank_values_list) == 0:
        return "Data wasn't found for user"
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
    except Exception as e:  # TODO too broad exception handler
        print('Failed to retrieve values' + str(e))
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
        return CHAMP_ICON
    if "Diamond" in rank_name:
        return DIAMOND_ICON
    if "Platinum" in rank_name:
        return PLATINUM_ICON
    if "Gold" in rank_name:
        return GOLD_ICON
    if "Silver" in rank_name:
        return SILVER_ICON
    if "Bronze" in rank_name:
        return BRONZE_ICON
    if "Unranked" in rank_name:
        return UNRANKED_ICON

import base64
import json
import os
import random
import re

import flask
import flask_cors
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = False


# CORS
flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})


# This app handles /api/* requests

# Redirect all /api/*.php to /api/*


@app.route("/api/<path:path>.php")
def redirect_php(path):
    # Redirect with all args
    return flask.redirect("/api/" + path + "?" + flask.request.query_string.decode("utf-8"))

# Redirect all /api/* to /api/v1/*


@app.route("/api/<path:path>")
def redirect_v1(path):
    # Redirect with all args
    return flask.redirect("/api/v1/" + path + "?" + flask.request.query_string.decode("utf-8"))

# Redirect all /api to /api/v1


@app.route("/api")
def redirect_v1_root():
    return flask.redirect("/api/v1")

# Handle /api/v1/*


@app.route("/api/v1/<path:path>")
def api_v1(path):
    # if path is empty, redirect to /api/v1
    if path == "":
        return flask.redirect("/api/v1")

    # if path is not empty, use different api
    # for example, /api/v1/echo?text=hello
    # will return {"text": "hello"}
    if path == "echo":
        return flask.jsonify({"text": flask.request.args.get("text")})

    # bing api
    # redirect to https://bing.lwd-temp.top/
    if path == "bing":
        return flask.redirect("https://bing.lwd-temp.top/")

    # hello api
    # return {"hello": "world"}
    if path == "hello":
        return flask.jsonify({"hello": "world"})

    # status api
    # return {"status": "ok"}
    if path == "status":
        return flask.jsonify({"status": "ok"})

    # env api
    # return all flask config information & environment variables in json
    if path == "env":
        return flask.jsonify({**os.environ, **app.config})

    # 33reply api
    # Bilibili Reply Fetcher for 662016827293958168
    if path == "33reply":
        # Get request args: next, oid
        next = flask.request.args.get("next")
        oid = flask.request.args.get("oid")
        # If next is not set, set it to 0
        if next == None:
            next = 0
        # If oid is not set, set it to 662016827293958168
        if oid == None:
            oid = 662016827293958168
        # Fetch reply
        # 'https://api.bilibili.com/x/v2/reply/main' + '?jsonp=jsonp&next=' + next + '&type=17&oid=' + oid + '&mode=2&plat=1'
        reply = requests.get('https://api.bilibili.com/x/v2/reply/main', params={
            'jsonp': 'jsonp',
            'next': next,
            'type': 17,
            'oid': oid,
            'mode': 2,
            'plat': 1
        })
        # Return reply
        return reply.json()

    # getBiliUserInfo api
    # Bilibili User Info Fetcher
    if path == "getBiliUserInfo":
        # Get request args: mid
        mid = flask.request.args.get("mid")
        # If mid is not set, set it to 22259558
        if mid == None:
            mid = 22259558
        # Fetch user info
        # 'https://api.bilibili.com/x/space/acc/info?mid=' + mid + '&jsonp=jsonp'
        reply = requests.get('https://api.bilibili.com/x/space/acc/info', params={
            'mid': mid,
            'jsonp': 'jsonp'
        })
        # Return user info
        return reply.json()

    # getGitHubAvatar api
    # GitHub Avatar Fetcher
    if path == "getGitHubAvatar":
        # Get args: username, type
        username = flask.request.args.get("username")
        type = flask.request.args.get("type")
        # If username is not set, set it to octocat
        if username == None:
            username = "octocat"
        # If type is not set, set it to raw
        if type == None:
            type = "raw"
        # Fetch avatar
        # If type is raw, return raw image
        if type == "raw":
            # Get avatar url
            avatar_url = requests.get(
                'https://api.github.com/users/' + username).json()["avatar_url"]
            # Set mimetype
            flask.Response.mimetype = "image/png"
            # Return raw image
            return requests.get(avatar_url).content
        # If type is json
        if type == "json":
            # Return avatar url
            return requests.get('https://api.github.com/users/' + username).json()["avatar_url"]
        # If type is redirect
        if type == "redirect":
            # Redirect to avatar url
            return flask.redirect(requests.get('https://api.github.com/users/' + username).json()["avatar_url"])

    # ikialive api
    # Bilibili user live status fetcher
    if path == "ikialive":
        # Get request args: mid
        mid = flask.request.args.get("mid")
        # If mid is not set, set it to 22259558
        if mid == None:
            mid = 22259558
        # Fetch live status
        # 'https://api.bilibili.com/x/space/acc/info?mid=' + mid + '&jsonp=jsonp'
        reply = requests.get('https://api.bilibili.com/x/space/acc/info', params={
            'mid': mid,
            'jsonp': 'jsonp'
        })
        # Return live status
        if reply.json()["data"]["live_room"] == "null":
            return "-1"

        try:
            stat = str(reply.json()["data"]["live_room"]["liveStatus"])
            if stat == "1":
                # Return text 1
                return "1"  # 有直播间且正在直播
            elif stat == "0":
                # Return text 0
                return "0"  # 有直播间但是没有直播
        except Exception as e:
            return "2"  # 未知，无法处理

    # kizunaai api
    # KizunaAI Directories List
    if path == "kizunaai":
        # Get args: id, date
        id = flask.request.args.get("id")
        date = flask.request.args.get("date")
        # Check if id = "63045280" to anti piracy
        if id != "63045280":
            return "error-01"
        # Check if date is set
        if date == None:
            return "error-00"
        else:
            # Check if data match MM-DD
            if re.match(r"^\d{2}-\d{2}$", date):
                pass
            else:
                return "error-02"
        file_structure = {"01-01": ["1.mp4"], "01-02": ["1.mp4", "2.mp4"], "01-03": ["1.mp4", "2.mp4"], "01-04": ["1.mp4", "2.mp4"], "01-05": ["1.mp4", "2.mp4"], "01-06": ["1.mp4", "2.mp4"], "01-07": ["1.mp4", "2.mp4"], "01-08": ["1.mp4", "2.mp4"], "01-09": ["1.mp4", "2.mp4"], "01-10": ["1.mp4", "2.mp4"], "01-11": ["1.mp4", "2.mp4"], "01-12": ["1.mp4"], "01-13": ["1.mp4", "2.mp4"], "01-14": ["1.mp4", "2.mp4"], "01-15": ["1.mp4", "2.mp4"], "01-16": ["1.mp4", "2.mp4"], "01-17": ["1.mp4", "2.mp4"], "01-18": ["1.mp4", "2.mp4"], "01-19": ["1.mp4", "2.mp4"], "01-20": ["1.mp4"], "01-21": ["1.mp4", "2.mp4"], "01-22": ["1.mp4", "2.mp4"], "01-23": ["1.mp4", "2.mp4"], "01-24": ["1.mp4", "2.mp4"], "01-25": ["1.mp4", "2.mp4"], "01-26": ["1.mp4", "2.mp4"], "01-27": ["1.mp4", "2.mp4"], "01-28": ["1.mp4", "2.mp4"], "01-29": ["1.mp4", "2.mp4"], "01-30": ["1.mp4", "2.mp4"], "01-31": ["1.mp4", "2.mp4"], "02-01": ["1.mp4", "2.mp4"], "02-02": ["1.mp4", "2.mp4"], "02-03": ["1.mp4", "2.mp4"], "02-04": ["1.mp4", "2.mp4"], "02-05": ["1.mp4", "2.mp4"], "02-06": ["1.mp4", "2.mp4"], "02-07": ["1.mp4", "2.mp4"], "02-08": ["1.mp4", "2.mp4"], "02-09": ["1.mp4", "2.mp4"], "02-10": ["1.mp4", "2.mp4"], "02-11": ["1.mp4", "2.mp4"], "02-12": ["1.mp4", "2.mp4"], "02-13": ["1.mp4", "2.mp4"], "02-14": ["1.mp4", "2.mp4"], "02-15": ["1.mp4", "2.mp4"], "02-16": ["1.mp4", "2.mp4"], "02-17": ["1.mp4", "2.mp4"], "02-18": ["1.mp4", "2.mp4"], "02-19": ["1.mp4", "2.mp4"], "02-20": ["1.mp4", "2.mp4"], "02-21": ["1.mp4", "2.mp4"], "02-22": ["1.mp4", "2.mp4"], "02-23": ["1.mp4", "2.mp4"], "02-24": ["1.mp4", "2.mp4"], "02-25": ["1.mp4", "2.mp4"], "02-26": ["1.mp4", "2.mp4"], "02-27": ["1.mp4"], "02-28": ["1.mp4"], "03-01": ["1.mp4"], "03-02": ["1.mp4"], "03-03": ["1.mp4"], "03-04": ["1.mp4"], "03-05": ["1.mp4"], "03-06": ["1.mp4"], "03-07": ["1.mp4"], "03-08": ["1.mp4"], "03-09": ["1.mp4"], "03-10": ["1.mp4"], "03-11": ["1.mp4"], "03-12": ["1.mp4"], "03-13": ["1.mp4"], "03-14": ["1.mp4"], "03-15": ["1.mp4"], "03-16": ["1.mp4"], "03-17": ["1.mp4"], "03-18": ["311990581-1-192.mp4"], "03-19": ["1.mp4"], "03-20": ["1.mp4"], "03-21": ["1.mp4"], "03-22": ["1.mp4"], "03-23": ["1.mp4"], "03-24": ["1.mp4"], "03-25": ["1.mp4"], "03-26": ["1.mp4"], "03-27": ["1.mp4"], "03-28": ["1.mp4"], "03-29": ["1.mp4"], "03-30": ["1.mp4"], "03-31": ["1.mp4"], "04-01": ["1.mp4", "2.mp4"], "04-02": ["1.mp4"], "04-03": ["1.mp4", "2.mp4"], "04-04": ["1.mp4"], "04-05": ["1.mp4"], "04-06": ["1.mp4", "2.mp4"], "04-07": ["1.mp4", "2.mp4"], "04-08": ["1.mp4", "2.mp4"], "04-09": ["1.mp4", "2.mp4"], "04-10": ["1.mp4", "2.mp4"], "04-11": ["1.mp4", "2.mp4"], "04-12": ["1.mp4", "2.mp4"], "04-13": ["1.mp4", "2.mp4"], "04-14": ["1.mp4", "2.mp4"], "04-15": ["1.mp4", "2.mp4"], "04-16": ["1.mp4", "2.mp4"], "04-17": ["1.mp4", "2.mp4"], "04-18": ["1.mp4", "2.mp4"], "04-19": ["1.mp4", "2.mp4"], "04-20": ["1.mp4", "2.mp4"], "04-21": ["1.mp4", "2.mp4"], "04-22": ["1.mp4", "2.mp4"], "04-23": ["1.mp4", "2.mp4"], "04-24": ["1.mp4", "2.mp4"], "04-25": ["1.mp4", "2.mp4"], "04-26": ["1.mp4", "2.mp4"], "04-27": ["1.mp4", "2.mp4"], "04-28": ["1.mp4", "2.mp4"], "04-29": ["1.mp4", "2.mp4"], "04-30": ["1.mp4", "2.mp4"], "05-01": ["1.mp4", "2.mp4"], "05-02": ["1.mp4", "2.mp4"], "05-03": ["1.mp4", "2.mp4"], "05-04": ["1.mp4", "2.mp4"], "05-05": ["1.mp4", "2.mp4"], "05-06": ["1.mp4", "2.mp4"], "05-07": ["1.mp4", "2.mp4"], "05-08": ["1.mp4", "2.mp4"], "05-09": ["1.mp4", "2.mp4"], "05-10": ["1.mp4", "2.mp4"], "05-11": ["1.mp4", "2.mp4"], "05-12": ["1.mp4"], "05-13": ["1.mp4", "2.mp4"], "05-14": ["1.mp4", "2.mp4"], "05-15": ["1.mp4", "2.mp4"], "05-16": ["1.mp4", "2.mp4"], "05-17": ["1.mp4", "2.mp4"], "05-18": ["1.mp4", "2.mp4"], "05-19": ["1.mp4"], "05-20": ["1.mp4", "2.mp4"], "05-21": ["1.mp4", "2.mp4"], "05-22": ["1.mp4", "2.mp4"], "05-23": ["1.mp4", "2.mp4"], "05-24": ["1.mp4", "2.mp4"], "05-25": ["1.mp4", "2.mp4"], "05-26": ["1.mp4", "2.mp4"], "05-27": ["1.mp4", "2.mp4"], "05-28": ["1.mp4", "2.mp4"], "05-29": ["1.mp4", "2.mp4"], "05-30": ["1.mp4", "2.mp4"], "05-31": ["1.mp4", "2.mp4"], "06-01": ["1.mp4", "2.mp4"], "06-02": ["1.mp4", "2.mp4"], "06-03": ["1.mp4", "2.mp4"], "06-04": ["1.mp4"], "06-05": ["1.mp4", "2.mp4"], "06-06": ["1.mp4", "2.mp4"], "06-07": ["1.mp4", "2.mp4"], "06-08": ["1.mp4", "2.mp4"], "06-09": ["1.mp4", "2.mp4"], "06-10": ["1.mp4", "2.mp4"], "06-11": ["1.mp4", "2.mp4"], "06-12": ["1.mp4", "2.mp4"], "06-13": ["1.mp4", "2.mp4"], "06-14": ["1.mp4"], "06-15": ["1.mp4"], "06-16": ["1.mp4"], "06-17": ["1.mp4"], "06-18": ["1.mp4"], "06-19": ["1.mp4"], "06-20": ["1.mp4"], "06-21": ["1.mp4", "2.mp4"], "06-22": ["1.mp4", "2.mp4"], "06-23": ["1.mp4", "2.mp4"], "06-24": ["1.mp4", "2.mp4"], "06-25": ["1.mp4", "2.mp4"], "06-26": ["1.mp4", "2.mp4"], "06-27": ["1.mp4", "2.mp4"], "06-28": ["1.mp4", "2.mp4"], "06-29": ["1.mp4", "2.mp4"], "06-30": ["1.mp4", "2.mp4"], "07-01": ["1.mp4", "2.mp4"], "07-02": ["1.mp4", "2.mp4"], "07-03": ["1.mp4", "2.mp4"], "07-04": ["1.mp4", "2.mp4"], "07-05": ["1.mp4", "2.mp4"], "07-06": ["1.mp4", "2.mp4"], "07-07": ["1.mp4"], "07-08": ["1.mp4", "2.mp4"],
                          "07-09": ["1.mp4", "2.mp4"], "07-10": ["1.mp4", "2.mp4"], "07-11": ["1.mp4", "2.mp4"], "07-12": ["1.mp4", "2.mp4"], "07-13": ["1.mp4", "2.mp4"], "07-14": ["1.mp4", "2.mp4"], "07-15": ["1.mp4", "2.mp4"], "07-16": ["1.mp4", "2.mp4"], "07-17": ["1.mp4", "2.mp4"], "07-18": ["1.mp4", "2.mp4"], "07-19": ["1.mp4", "2.mp4"], "07-20": ["1.mp4", "2.mp4"], "07-21": ["1.mp4"], "07-22": ["1.mp4", "2.mp4"], "07-23": ["1.mp4", "2.mp4"], "07-24": ["1.mp4", "2.mp4"], "07-25": ["1.mp4", "2.mp4"], "07-26": ["1.mp4", "2.mp4"], "07-27": ["1.mp4", "2.mp4"], "07-28": ["1.mp4", "2.mp4"], "07-29": ["1.mp4", "2.mp4"], "07-30": ["1.mp4", "2.mp4"], "07-31": ["1.mp4", "2.mp4"], "08-01": ["1.mp4", "2.mp4"], "08-02": ["1.mp4", "2.mp4"], "08-03": ["1.mp4", "2.mp4"], "08-04": ["1.mp4", "2.mp4"], "08-05": ["1.mp4", "2.mp4"], "08-06": ["1.mp4", "2.mp4"], "08-07": ["1.mp4", "2.mp4"], "08-08": ["1.mp4", "2.mp4"], "08-09": ["1.mp4", "2.mp4"], "08-10": ["1.mp4", "2.mp4"], "08-11": ["1.mp4", "2.mp4"], "08-12": ["1.mp4", "2.mp4"], "08-13": ["1.mp4", "2.mp4"], "08-14": ["1.mp4", "2.mp4"], "08-15": ["1.mp4", "2.mp4"], "08-16": ["1.mp4", "2.mp4"], "08-17": ["1.mp4", "2.mp4"], "08-18": ["1.mp4", "2.mp4"], "08-19": ["1.mp4", "2.mp4"], "08-20": ["1.mp4", "2.mp4"], "08-21": ["1.mp4", "2.mp4"], "08-22": ["1.mp4", "2.mp4"], "08-23": ["1.mp4", "2.mp4"], "08-24": ["1.mp4", "2.mp4"], "08-25": ["1.mp4", "2.mp4"], "08-26": ["1.mp4", "2.mp4"], "08-27": ["1.mp4", "2.mp4"], "08-28": ["1.mp4", "2.mp4"], "08-29": ["1.mp4", "2.mp4"], "08-30": ["1.mp4", "2.mp4"], "08-31": ["1.mp4", "2.mp4"], "09-01": ["1.mp4", "2.mp4"], "09-02": ["1.mp4", "2.mp4"], "09-03": ["1.mp4", "2.mp4"], "09-04": ["1.mp4", "2.mp4"], "09-05": ["1.mp4", "2.mp4"], "09-06": ["1.mp4", "2.mp4"], "09-07": ["1.mp4", "2.mp4"], "09-08": ["1.mp4", "2.mp4"], "09-09": ["1.mp4", "2.mp4"], "09-10": ["1.mp4", "2.mp4"], "09-11": ["1.mp4", "2.mp4"], "09-12": ["1.mp4", "2.mp4"], "09-13": ["1.mp4", "2.mp4"], "09-14": ["1.mp4", "2.mp4"], "09-15": ["1.mp4", "2.mp4"], "09-16": ["1.mp4", "2.mp4"], "09-17": ["1.mp4", "2.mp4"], "09-18": ["vMDjFVsj9yxnEbox.mp4"], "09-19": ["1.mp4", "2.mp4"], "09-20": ["1.mp4", "2.mp4"], "09-21": ["1.mp4", "2.mp4"], "09-22": ["1.mp4", "2.mp4"], "09-23": ["1.mp4", "2.mp4"], "09-24": ["1.mp4", "2.mp4"], "09-25": ["1.mp4", "2.mp4"], "09-26": ["1.mp4", "2.mp4"], "09-27": ["1.mp4", "2.mp4"], "09-28": ["1.mp4"], "09-29": ["1.mp4", "2.mp4"], "09-30": ["1.mp4", "2.mp4"], "10-01": ["1.mp4", "2.mp4"], "10-02": ["1.mp4", "2.mp4"], "10-03": ["1.mp4", "2.mp4"], "10-04": ["1.mp4", "2.mp4"], "10-05": ["1.mp4", "2.mp4"], "10-06": ["1.mp4", "2.mp4"], "10-07": ["1.mp4", "2.mp4"], "10-08": ["1.mp4", "2.mp4"], "10-09": ["1.mp4", "2.mp4"], "10-10": ["1.mp4", "2.mp4"], "10-11": ["1.mp4", "2.mp4"], "10-12": ["1.mp4", "2.mp4"], "10-13": ["1.mp4", "2.mp4"], "10-14": ["1.mp4", "2.mp4"], "10-15": ["1.mp4", "2.mp4"], "10-16": ["1.mp4", "2.mp4"], "10-17": ["1.mp4", "2.mp4"], "10-18": ["1.mp4", "2.mp4"], "10-19": ["1.mp4", "2.mp4"], "10-20": ["1.mp4", "2.mp4"], "10-21": ["1.mp4", "2.mp4"], "10-22": ["1.mp4", "2.mp4"], "10-23": ["1.mp4", "2.mp4"], "10-24": ["1.mp4", "2.mp4"], "10-25": ["1.mp4", "2.mp4"], "10-26": ["1.mp4", "2.mp4"], "10-27": ["1.mp4", "2.mp4"], "10-28": ["1.mp4", "2.mp4"], "10-29": ["1.mp4"], "10-30": ["1.mp4", "2.mp4"], "10-31": ["1.mp4"], "11-01": ["1.mp4", "2.mp4"], "11-02": ["1.mp4", "2.mp4"], "11-03": ["1.mp4", "2.mp4"], "11-04": ["1.mp4", "2.mp4"], "11-05": ["1.mp4", "2.mp4"], "11-06": ["1.mp4", "2.mp4"], "11-07": ["1.mp4", "2.mp4"], "11-08": ["1.mp4", "2.mp4"], "11-09": ["1.mp4", "2.mp4"], "11-10": ["1.mp4", "2.mp4"], "11-11": ["1.mp4", "2.mp4"], "11-12": ["1.mp4", "2.mp4"], "11-13": ["1.mp4", "2.mp4"], "11-14": ["1.mp4", "2.mp4"], "11-15": ["1.mp4", "2.mp4"], "11-16": ["1.mp4", "2.mp4"], "11-17": ["1.mp4", "2.mp4"], "11-18": ["1.mp4", "2.mp4"], "11-19": ["1.mp4", "2.mp4"], "11-20": ["1.mp4", "2.mp4"], "11-21": ["1.mp4", "2.mp4"], "11-22": ["1.mp4", "2.mp4"], "11-23": ["1.mp4", "2.mp4"], "11-24": ["1.mp4", "2.mp4"], "11-25": ["1.mp4", "2.mp4"], "11-26": ["1.mp4", "2.mp4"], "11-27": ["1.mp4", "2.mp4"], "11-28": ["1.mp4", "2.mp4"], "11-29": ["1.mp4", "2.mp4"], "11-30": ["1.mp4", "2.mp4"], "12-01": ["1.mp4", "2.mp4"], "12-02": ["1.mp4", "2.mp4"], "12-03": ["1.mp4", "2.mp4"], "12-04": ["1.mp4", "2.mp4"], "12-05": ["1.mp4", "2.mp4"], "12-06": ["1.mp4", "2.mp4"], "12-07": ["1.mp4", "2.mp4"], "12-08": ["1.mp4", "2.mp4"], "12-09": ["1.mp4", "2.mp4"], "12-10": ["1.mp4", "2.mp4"], "12-11": ["1.mp4", "2.mp4"], "12-12": ["1.mp4", "2.mp4"], "12-13": ["1.mp4"], "12-14": ["1.mp4", "2.mp4"], "12-15": ["1.mp4", "2.mp4"], "12-16": ["1.mp4", "2.mp4"], "12-17": ["1.mp4", "2.mp4"], "12-18": ["1.mp4", "2.mp4"], "12-19": ["1.mp4", "2.mp4"], "12-20": ["1.mp4", "2.mp4"], "12-21": ["1.mp4", "2.mp4"], "12-22": ["1.mp4", "2.mp4"], "12-23": ["1.mp4", "2.mp4"], "12-24": ["1.mp4", "2.mp4"], "12-25": ["1.mp4", "2.mp4"], "12-26": ["1.mp4", "2.mp4"], "12-27": ["1.mp4", "2.mp4"], "12-28": ["1.mp4", "2.mp4"], "12-29": ["1.mp4", "2.mp4"], "12-30": ["1.mp4"], "12-31": ["1.mp4", "2.mp4"]}
        oss_base_url_a = 'https://drive.lwd-temp.top/api?path='
        oss_base_url_b = '&raw=true'
        oss_dir = '/KizunaAI'
        # If date == ""02-29", then date = "02-28"
        if date == "02-29":
            date = "02-28"
        try:
            videos = file_structure[date]
            # If videos has only one video, then video = videos[0]
            if len(videos) == 1:
                video = videos[0]
            elif len(videos) == 0:
                return "error-03"
            else:
                # Get random video from videos
                video = random.choice(videos)
            # Get video url
            video_url = oss_base_url_a + oss_dir + '/' + date + '/' + video + oss_base_url_b
            return video_url
        except Exception as e:
            return "error-03"

    # mcskin api
    # Get Minecraft skin from a Minecraft username
    if path == "mcskin":
        # Get args: id, format
        id = flask.request.args.get("id")
        format = flask.request.args.get("format")
        # If id is empty, return help message
        if id == None:
            return "Usage: index.php?id=[Player ID]&format=[url/json/image]"
        # If format is empty, set format to "url"
        if format == None:
            format = "url"
        API_PROFILE_URL = "https://api.mojang.com/users/profiles/minecraft/"
        API_SESSION_URL = "https://sessionserver.mojang.com/session/minecraft/profile/"
        # Get profile
        profile = requests.get(API_PROFILE_URL + id).json()
        sessionid = profile["id"]
        session = requests.get(API_SESSION_URL + sessionid).json()

        textureB64 = session["properties"][0]["value"]
        textureRaw = base64.b64decode(textureB64)
        textureJson = json.loads(textureRaw)

        skinUrl = textureJson["textures"]["SKIN"]["url"]

        if format == "url":
            return skinUrl
        elif format == "json":
            dict = {"url": skinUrl, 'profile': profile, 'session': session}
            return json.dumps(dict)
        elif format == "image":
            # Get image
            image = requests.get(skinUrl).content
            return flask.Response(image, mimetype="image/png")
        else:
            return skinUrl

    # If path is not found, return 404
    return "404 Not Found", 404


# Handle /api/v1


@app.route("/api/v1")
def api_v1_root():
    # return {"api": "v1"}
    return flask.jsonify({"api": "v1"})

# 404 handler


@app.errorhandler(404)
def page_not_found(e):
    return flask.jsonify({"error": "not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
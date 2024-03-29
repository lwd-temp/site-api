# Detect China IP
# Read from china_ip_list.txt to get CIDR list
# https://github.com/17mon/china_ip_list

import ipaddress

import flask

from . import cfstyle


def get_ip():
    # Get IP
    # From headers first
    # cf-connecting-ip x-real-ip
    # x-forwarded-for
    # Then from request
    ip = flask.request.headers.get("cf-connecting-ip")
    if ip is None:
        ip = flask.request.headers.get("x-real-ip")
    if ip is None:
        ip = flask.request.headers.get("x-forwarded-for")
    if ip is None:
        ip = flask.request.remote_addr
    return ip


def chk_cdn_region_header():
    Cf_Ipcountry = flask.request.headers.get("cf-ipcountry")
    if Cf_Ipcountry == "CN":
        return True
    X_Vercel_Ip_Country = flask.request.headers.get("x-vercel-ip-country")
    if X_Vercel_Ip_Country == "CN":
        return True

    return False


def is_china_ip(ip):
    # IPv4
    with open("china_ip_list.txt") as f:
        for line in f:
            line = line.strip()
            if ipaddress.ip_address(ip) in ipaddress.ip_network(line):
                return True
    # IPv6
    # https://github.com/ChanthMiao/China-IPv6-List
    with open("cn6.txt") as f:
        for line in f:
            line = line.strip()
            if ipaddress.ip_address(ip) in ipaddress.ip_network(line):
                return True

    return False


# Check request Accept-Language header
def check_zhcn():
    if "zh-CN" in flask.request.headers.get("Accept-Language", ""):
        return True
    return False


# Checker
def check(lang=False):
    ip = cfstyle.get_ip()
    if is_china_ip(ip):
        return True
    if chk_cdn_region_header():
        return True
    if lang and check_zhcn():
        return True
    return False


def check_and_abort(lang=False, json=False):
    if check(lang):
        if json:
            # Get current flask app
            app = flask.current_app
            # Set app.config['JSONERROR'] = '1'
            app.config["JSONERROR"] = "1"

        flask.abort(451, "Sorry, but you are in China.")

import flask
import requests
import urllib.parse

from . import keybase

ghproxy = keybase.ghproxy


def cfw():
    # Get latest release
    r = requests.get(
        'https://api.github.com/repos/Fndroid/clash_for_windows_pkg/releases/latest')
    r.raise_for_status()
    release = r.json()

    # Get assets
    assets = release['assets']

    # Get name: url
    asset_urls = {asset['name']: asset['browser_download_url']
                  for asset in assets}

    # Return name Clash.for.Windows.Setup.x.xx.x.exe
    # Check all names contains Setup
    for name in asset_urls:
        if 'Setup' in name and 'ia32' not in name and 'arm64' not in name:
            installer = name

    # Return url
    installer_url = asset_urls[installer]

    # ghproxy
    installer_url = ghproxy + installer_url

    return installer_url


def cfw_portable():
    # Get latest release
    r = requests.get(
        'https://api.github.com/repos/Fndroid/clash_for_windows_pkg/releases/latest')
    r.raise_for_status()
    release = r.json()

    # Get assets
    assets = release['assets']

    # Get name: url
    asset_urls = {asset['name']: asset['browser_download_url']
                  for asset in assets}

    # Return name Clash.for.Windows.Setup.x.xx.x.exe
    # Check all names contains Setup
    for name in asset_urls:
        if 'win.7z' in name and 'ia32' not in name and 'arm64' not in name:
            installer = name

    # Return url
    installer_url = asset_urls[installer]

    # ghproxy
    installer_url = ghproxy + installer_url

    return installer_url


def cfa():
    # Get latest release
    r = requests.get(
        'https://api.github.com/repos/Kr328/ClashForAndroid/releases/latest')
    r.raise_for_status()
    release = r.json()

    # Get assets
    assets = release['assets']

    # Get name: url
    asset_urls = {asset['name']: asset['browser_download_url']
                  for asset in assets}

    # Return name Clash.for.Windows.Setup.x.xx.x.exe
    # Check all names contains Setup
    for name in asset_urls:
        if 'premium-universal-release' in name:
            installer = name

    # Return url
    installer_url = asset_urls[installer]

    # ghproxy
    installer_url = ghproxy + installer_url

    return installer_url


def subscribe():
    # https://github.com/paimonhub/Paimonnode
    # https://raw.githubusercontent.com/paimonhub/Paimonnode/main/clash.yaml
    subscribe_source_name = "API自动聚合"
    subscribe_source_url = "https://api.lwd-temp.top/"
    subscribe_url = "https://api.lwd-temp.top/api/clash/config"
    base64_url = "https://api.lwd-temp.top/"

    # ghproxy
    # subscribe_url = ghproxy + subscribe_url
    # base64_url = ghproxy + base64_url

    return subscribe_source_name, subscribe_source_url, subscribe_url, base64_url


def render():
    subscribe_source_name, subscribe_source_url, subscribe_url, base64_url = subscribe()

    # URL Encoded
    subscribe_encoded_url = urllib.parse.quote(subscribe_url, safe='')

    return flask.render_template('clash.html', cfw=cfw(), cfw_portable=cfw_portable(), cfa=cfa(), subscribe_source_name=subscribe_source_name, subscribe_source_url=subscribe_source_url, subscribe_url=subscribe_url, base64_url=base64_url, subscribe_encoded_url=subscribe_encoded_url)


def config():
    # Get yaml and return
    # https://raw.githubusercontent.com/paimonhub/Paimonnode/main/clash.yaml
    sub_urls = [
        "https://raw.githubusercontent.com/paimonhub/Paimonnode/main/clash.yaml",
        "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
        "https://raw.githubusercontent.com/openrunner/clash-freenode/main/clash.yaml",
        "https://raw.githubusercontent.com/learnhard-cn/free_proxy_ss/main/config.yaml"
    ]

    api_urls = [
        "https://sub.xeton.dev/sub",
        "https://api.wcc.best/sub",
        "https://api.dler.io/sub"
    ]

    # Get an available API url
    api_url = False
    for url in api_urls:
        try:
            api = requests.get(url)
        except:
            continue

        if api.status_code == 400:
            api_url = url
            break

    if api_url:
        # API is available

        # Get sub list
        subs = []
        for url in sub_urls:
            try:
                config = requests.get(url)
            except:
                continue

            if config.status_code == 200:
                subs.append(url)

        # API args
        # target=clash&new_name=true&url=
        # &insert=false&append_type=true&emoji=true&list=false&tfo=false&scv=false&fdn=true&sort=true
        api_call = api_url + "?"
        url_cmb = ""
        for sub in subs:
            url_cmb = url_cmb + "|"
            url_cmb = url_cmb + sub
        api_args = "target=clash&new_name=true&url=" + urllib.parse.quote(url_cmb, safe='') + \
            "&insert=false&append_type=true&emoji=true&list=false&tfo=false&scv=false&fdn=true&sort=true"
        api_call = api_call + api_args
        api_req = requests.get(api_call)
        api_req.raise_for_status()
        config = api_req.text

    else:
        # No API available
        for url in sub_urls:

            try:
                config = requests.get(url)
            except:
                continue

            if config.status_code != 200:
                continue
            else:
                # config.raise_for_status()
                config = config.text
                break

    return config

# author: push.thanh@gmail.com

# references:
# https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
import requests
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}


def download_free_proxies(to_csv=True):
    print("downloading free proxies...")
    url = "https://free-proxy-list.net/anonymous-proxy.html"
    page = requests.get(url, headers=HEADERS)
    table = pd.read_html(page.text)
    df = table[0]
    df.dropna(inplace=True)
    df = df.groupby(['Https']).get_group('yes')
    df.reset_index(inplace=True)

    if to_csv:
        df.to_csv("./proxy_files/proxies.csv")


def download_agent_headers(to_csv=True):
    print("downloading free agent-headers....")
    browers = ['firefox']
    url = "https://developers.whatismybrowser.com/useragents/explore/software_name/"

    dfs = []
    for b in browers:
        endpoint = "".join([url, b])
        page = requests.get(endpoint, headers=HEADERS)
        table = pd.read_html(page.text)
        df = table[0]
        df.columns = df.columns.str.strip()
        dfs.append(df)

    results = pd.concat(dfs)
    if to_csv:
        results.to_csv("./proxy_files/user_agents.csv")


if __name__ == '__main__':
    download_free_proxies()

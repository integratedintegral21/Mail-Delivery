import requests

URL = 'https://uss.poczta-polska.pl/uss/v1.0/tracking/checkmailex'


def main():
    headers = {
        'Host': 'uss.poczta - polska.pl',
        'Connection': 'keep-alive',
        'Content-Length': '74',
        'sec-ch-ua': '"Google Chrome";v = "93", " Not;A Brand";v = "99", "Chromium";v = "93"',
        'Accept': '*/*',
        'Content-Type': 'application/json; charset = UTF-8',
        'API_KEY': 'BiGwVG2XHvXY+kPwJVPA8gnKchOFsyy39Thkyb1wAiWcKLQ1ICyLiCrxj1+vVGC+kQk3k0b74qkmt5/qVIzo7lTfXhfgJ72Iyzz05wH2XZI6AgXVDciX7G2jLCdoOEM6XegPsMJChiouWS2RZuf3eOXpK5RPl8Sy4pWj+b07MLg=.Mjg0Q0NFNzM0RTBERTIwOTNFOUYxNkYxMUY1NDZGMTA0NDMwQUIyRjg4REUxMjk5NDAyMkQ0N0VCNDgwNTc1NA==.b24415d1b30a456cb8ba187b34cb6a86',
        'sec-ch-ua - mobile': '?0',
        'User-Agent': 'Mozilla / 5.0(X11;Fedora;Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 93.0.4577.63 Safari / 537.36',
        'sec-ch-ua-platform': "Linux",
        'Origin': 'https://monitoring.poczta-polska.pl',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://emonitoring.poczta-polska.pl/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB, en-US;q = 0.9, en;q = 0.8'
    }
    r = requests.post(URL, data={'language': "PL", 'number': "00259007731373228115", 'addPostOfficeInfo': 'true'},
                      headers=headers)
    print(r.status_code, r.reason)
    print(r.text)


if __name__ == "__main__":
    main()

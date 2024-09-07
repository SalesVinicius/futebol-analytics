# %%%
import requests
import pandas as pd
import json
# %%

df_matches = pd.DataFrame()

with open('colunas_matches.json', 'r') as open_file:
    config = json.load(open_file)

colunas_matches_mapping = config['colunas_matches_rename']
colunas_matches_keep = config['colunas_matches_keep']

# %%
#Puxando jogos da rodada para descobrir os IDs das partidas
for i in range(1,16,1):
    url = f'https://www.sofascore.com/api/v1/unique-tournament/325/season/58766/events/round/{i}'

    payload = {}
    headers = {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,ceb;q=0.6",
        "cache-control": "max-age=0",
        "cookie": "_cc_id=248bb0221b87d759694ba698b54adb82; cto_bundle=ZJ-x9F9xOWQ0Znc3aXlNN1JUYVh1SSUyQmpuOUU0ZjFERnczMXB3b1ZXJTJCa1pWMHZ4TWV2T0VoNXZxT1N0dDZYJTJGTFlDY09nY3lvOW1CN3lVbHdLbFlNZVlwNktmdU9VVnk0MmhRJTJGU0EwckpmQWZ3JTJGeGFGQ1NEUE92VHdLZHRzTnRIVTlmWTZVUlc1bllTcXRDenhSeXFFak5TQ0Z3JTNEJTNE; cto_bidid=QrAq_l9kbzFQclFTUmwzZSUyRnVYYnBGaUdUQ0NIMVRoU2klMkJ6T1I5cXclMkJtQ1h2MDVLd2Q0Q05lbyUyQmtkdDh2UCUyRmFYalRIN3IzWmxDbDlHWnRoOFdDSXlGcmFTbWlka1pCbDlRSnElMkIwTCUyRmNDSFNESW9ZJTNE; _ga=GA1.1.398452961.1683470122; _scid_r=21548dbe-6221-424a-b03c-757c92301a30; cto_bundle=V2OTq19xOWQ0Znc3aXlNN1JUYVh1SSUyQmpuOUVFY2tRR3NMbDdxZ1BpeHhwTTRGWUNMbkw4SHJuaVMyQlBxdnR3ZEJCc2F1Uk1iSFkydld5d2lEWkZycm80bWQwWEV1dlBCdDRtSkhrYjJ3QzlyU3ZRb1VBNU4lMkJIN0Q3VjZKRnpQbW9Td1M0RGY1RUwwOG14SjZWSzNjNW05UWFBJTNEJTNE; cto_bidid=cCYi-19kbzFQclFTUmwzZSUyRnVYYnBGaUdUQ0NIMVRoU2klMkJ6T1I5cXclMkJtQ1h2MDVLd2Q0Q05lbyUyQmtkdDh2UCUyRmFYalRIN3IzWmxDbDlHWnRoOFdDSXlGcmFTbXZHbG94M04zM0E2U2xJdTRCeFhpRTglM0Q; __gads=ID=92550bb856c582d6:T=1692480711:RT=1710383147:S=ALNI_MZrT1s8MHP0mcaFqh0rt4eA5nyg2g; __gpi=UID=00000d9ee914ece0:T=1692480711:RT=1710383147:S=ALNI_MbYN2sUykqmarIVIdzFBSoVXp4Bgw; _lr_env_src_ats=false; _clck=y6mv2b%7C2%7Cfny%7C0%7C1669; gcid_first=05ebc6a3-58f6-48b6-8393-c1affef71376; _ga_QH2YGS7BB4=GS1.1.1724291547.164.1.1724293598.0.0.0; _ga_3KF4XTPHC4=GS1.1.1724291547.134.1.1724293598.56.0.0; _lr_retry_request=true; FCNEC=%5B%5B%22AKsRol8FdWDQ6jl9n1tq-5KkgiGWr9uOp3WsA_XoGe1ghLuvocY1qsw4hQFoa1zN1tH4nkb8e8pg5dBne08BBryLHEDUFV98yh38_6s1nIwuQvUvDq8Wiu2Ne_2RDB92Nnx1nL63WkmT0EjpS4_1oBhUw5qj-TtBWQ%3D%3D%22%5D%5D",
        "if-none-match": "W/'7c51b0e401'",
        "priority": "u=1, i",
        "referer": "https://www.sofascore.com/tournament/football/brazil/brasileirao-serie-a/325",
        "sec-ch-ua": "'Chromium';v='128', 'Not;A=Brand';v='24', 'Google Chrome';v='128'",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "'Windows'",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "x-requested-with": "144253"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    matches = response.json()['events']

    df_round_matches = pd.json_normalize(matches)

    id_matches = df_round_matches['id'].tolist()

    df_round_matches = df_round_matches.rename(columns=colunas_matches_mapping)
    df_round_matches = df_round_matches[colunas_matches_keep]
    df_round_matches = df_round_matches[df_round_matches['statusPartida'] != 'Postponed']

    df_matches = pd.concat([df_matches,df_round_matches], ignore_index=True)

# %%
matches_data_path = '../data/matches.csv'
df_matches.to_csv(matches_data_path,sep=';')
# %%

import json

playlists_sanremo = ['https://open.spotify.com/playlist/4kz1ooWaP6iZMIi7YK4tF3',
                     'https://open.spotify.com/playlist/2dcAOlIOa8VaFTNLV1U085',
                     'https://open.spotify.com/playlist/05iSQZSAcSRpaNl4kkMLxu',
                     'https://open.spotify.com/playlist/4nkcFHNHQr0rx2WWy28IZS',
                     'https://open.spotify.com/playlist/3CPrg00sbezxCqfjFvNJsA',
                     'https://open.spotify.com/playlist/58v6XgOm2mr8VI2mHkpETb',
                     'https://open.spotify.com/playlist/00HpbPQa7Nqd8hj7w4Zi9p',
                     'https://open.spotify.com/playlist/2ibP17HcbnTpTIFFbVLYIq',
                     'https://open.spotify.com/playlist/2vV4EEbsNsBpye7koFVjpH',

                     'https://open.spotify.com/playlist/76RhMwyJemt3IzHSQ1RpQt',
                     'https://open.spotify.com/playlist/1OFCTHJXDpejjVQGnXjiMb',
                     'https://open.spotify.com/playlist/0lJiLpihSD9yn3ejU6OlYh',
                     'https://open.spotify.com/playlist/4D11Jx85BzyMyy7AGEcQY8',
                     'https://open.spotify.com/playlist/0WebTdmmAirLhmRqAfsrhz',
                     'https://open.spotify.com/playlist/7GcLfjlU0xTGr6PJC14oHX',
                     'https://open.spotify.com/playlist/1gCCKTxpmbg8Nxxrec8S6K',
                     'https://open.spotify.com/playlist/3LBAqv3oa8Jf8AwC61Eosn',
                     'https://open.spotify.com/playlist/36e0t00203q6OI89sn1OjK',
                     'https://open.spotify.com/playlist/4ghkn2NAMPjXrff3htE1QO',

                     'https://open.spotify.com/playlist/2Iro2aKxXoxBEtpmtrHNQW',
                     'https://open.spotify.com/playlist/72s6rjxbAFK8r9Oe8c5oac',
                     'https://open.spotify.com/playlist/1NhUusx5wxQFOTv6FBde6y',
                     'https://open.spotify.com/playlist/5QdIh2BAxA1UBTXemI2Xww',
                     'https://open.spotify.com/playlist/1fNEs7HLOmzPZHtlReRevR',
                     'https://open.spotify.com/playlist/0K37nyBzPhuhuoALzfljeJ',
                     'https://open.spotify.com/playlist/1GMdBPAOH6FD7ZeI9MqowV',
                     'https://open.spotify.com/playlist/0307sHEDaiFxJaCT36w3Ds',
                     'https://open.spotify.com/playlist/4UP3NBnjh0VuaCufN5kEBF',
                     'https://open.spotify.com/playlist/0tXSUmYlRIHpEfpdBuEfkr',

                     'https://open.spotify.com/playlist/0l7CVgB9bbrdq0PYUjkDKE',
                     'https://open.spotify.com/playlist/0CnT0RwAWYisfSwhju2OB6',
                     'https://open.spotify.com/playlist/4BqRGEGrqdh7xRLtgAOaI8',
                     'https://open.spotify.com/playlist/4mkGMSyI4I07AVlDj3ESLJ',
                     'https://open.spotify.com/playlist/4D6JluMpIiRdnpFP2fRzdA',
                     'https://open.spotify.com/playlist/2ccANwZ6YEdnxwrkJiSm7h',
                     'https://open.spotify.com/playlist/26YoeRocUIQ87hKoVr41Na',
                     'https://open.spotify.com/playlist/1ORUrRVYFlKxxEG84YLR7H',
                     'https://open.spotify.com/playlist/5rtXosQ8cXCYwbKRPg1OZM',
                     'https://open.spotify.com/playlist/5rqZoU1iMcnj90qmRSj5Wd',

                     'https://open.spotify.com/playlist/3JvcHh7tgvDWKoGSIMRrJl',
                     'https://open.spotify.com/playlist/5mD37DXPodslpDmtePtFlV',
                     'https://open.spotify.com/playlist/5ZhCEuLXBVOmtMf6YlJk6M',
                     'https://open.spotify.com/playlist/2KZKiTOIxLt6MFNG2jfxqu',
                     'https://open.spotify.com/playlist/19dsRjnFMen2Q2JGto0Of6',
                     'https://open.spotify.com/playlist/2kX9OOVTpwJLzfQxoibRoK',
                     'https://open.spotify.com/playlist/1bazA6EwEq0VD7iVQGjgAH',
                     'https://open.spotify.com/playlist/1b4IbU1pHuBdC0dukkJuZJ',
                     'https://open.spotify.com/playlist/3obCWh4ewdZe8stDTtbAto',
                     'https://open.spotify.com/playlist/2CIw24xkpXrPIju1necboW',

                     'https://open.spotify.com/playlist/77vv8TeXcrIfy3QeDdzJmf',
                     'https://open.spotify.com/playlist/2iKMpwGG00KJKHyn1IWwwF',
                     'https://open.spotify.com/playlist/6p4x2wUKSRlG4MYAP1dtk1',
                     'https://open.spotify.com/playlist/4kWxeXJXcI0lRAJVpabV4B',
                     'https://open.spotify.com/playlist/66zQ8nKMh6yfJoqGimEnzj',
                     'https://open.spotify.com/playlist/0VXy4vPFSSRwJUWh47fiZA',
                     'https://open.spotify.com/playlist/0vlhyzOBHfXLhgd93ddSfm',
                     'https://open.spotify.com/playlist/2ZhOqhLygzaYtedxPyUuxr',
                     'https://open.spotify.com/playlist/3BPhER0xxSBu0XzyRb1Sc4',
                     'https://open.spotify.com/playlist/13gJCAYu8Hrr7iYAOduJuM',

                     'https://open.spotify.com/playlist/1a7YZWuZAc4dyMFcOjxQiA',
                     'https://open.spotify.com/playlist/3sfOk2moZfGadE5sfcdJos',
                     'https://open.spotify.com/playlist/6R2WdOUNI3ANwQXgsrgjkZ',
                     'https://open.spotify.com/playlist/3GJcjZjDp1a9fnGSY2hhjw',
                     'https://open.spotify.com/playlist/5NNfbdGAkXoZWI6TEHS3aL',
                     'https://open.spotify.com/playlist/3hmgg1VrRf24G2bIAorDgq',
                     'https://open.spotify.com/playlist/7qlPGbAn5TSanHtp8VlKBr',
                     'https://open.spotify.com/playlist/2TKgANdwAARwEmpIpgCPmh',
                     'https://open.spotify.com/playlist/5FNKtuGkP6t42OZVzFhH3L',
                     'https://open.spotify.com/playlist/1XOxaDgNMGaSJpm3U1jh47',

                     'https://open.spotify.com/playlist/4gszffY2nP0WJuUBD1vBkD',
                     'https://open.spotify.com/playlist/7AovGmAp1XfEkLjPa850Pw',
                     'https://open.spotify.com/playlist/2Mpsoy6QMHYLnuQhRGBHvF'
                     ]
playlists_eurovision = [
    ["https://www.youtube.com/playlist?list=PLBF27C5165BD15F1D",
        "https://www.youtube.com/watch?v=IyqIPvOkiRk"],
    ["https://www.youtube.com/playlist?list=PLD4C4BD674B455086"],
    ["https://www.youtube.com/playlist?list=PLD42A1900DFFBDFA1"],
    ["https://www.youtube.com/playlist?list=PL671CA3847635EE28", "https://www.youtube.com/watch?v=Gwqzn3FNVWw",
        "https://www.youtube.com/watch?v=nGAupVJSO0k", "https://www.youtube.com/watch?v=uAB_OJ8UveU"],

    ["https://www.youtube.com/playlist?list=PL38A4377C82852BCB"],
    ["https://www.youtube.com/playlist?list=PL87D7940A1F2E4BA2"],
    ["https://www.youtube.com/playlist?list=PLE749F1E5242854EC"],
    ["https://www.youtube.com/playlist?list=PL6C16AF2BD9671643"],
    ["https://www.youtube.com/playlist?list=PL7CBFF1F3136D8C84"],
    ["https://www.youtube.com/playlist?list=PL78F440FF79807BBA"],
    ["https://www.youtube.com/playlist?list=PL6F4397C1CA65E79C"],
    ["https://www.youtube.com/watch?v=Ga1kMdJCc_Q",
        "https://www.youtube.com/watch?v=Ga1kMdJCc_Q"],
    ["https://www.youtube.com/playlist?list=PL329BA020EE9CD7B2"],
    ["https://www.youtube.com/playlist?list=PL329BA020EE9CD7B2"],

    ["https://www.youtube.com/playlist?list=PL3197E26B76956003"],
    ["https://www.youtube.com/playlist?list=PL6A56E518F8401C58"],
    ["https://www.youtube.com/playlist?list=PLF38E5363BA7C82B0"],
    ["https://www.youtube.com/playlist?list=PL6623948B951DCB7B"],
    ["https://www.youtube.com/playlist?list=PLIqE7BpLNHKoGh3I19TTQN3rEr3H5yNlo"],
    ["https://www.youtube.com/playlist?list=PLmwh4vi1huQ3RfEt0EdY7fu9WSLPbQD9_"],
    ["https://www.youtube.com/playlist?list=PLIqE7BpLNHKpxTVeR5NUl8yf7Rig6GGU2"],
    ["https://www.youtube.com/playlist?list=PLC6C873327CD5C850"],
    ["https://www.youtube.com/playlist?list=PLwVpAwiOa7mD6lL47Koi35oh_bMNQjf6R"],
    ["https://www.youtube.com/playlist?list=PL733F9C6BE19F9023"],

    ["https://www.youtube.com/playlist?list=PLwVpAwiOa7mDe-gtCpCwW5vS66G2qY2vQ"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSpDaGjFPE6jJHGc4G89rgxf"],
    ["https://www.youtube.com/playlist?list=PL4E4F4883B213BE44"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSoDUTxCm1e_Wsv_FUGr5L2k"],
    ["https://www.youtube.com/playlist?list=PLtqOsihHVwwWdbSoDo6pcYVh_Inp9S_ai"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSq6BpwkTtWnOcDFtlr_Xd_S"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSrTuOiLxOms586U2lHsMn21"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSpiGIvpFuAyhs-4BhrJLWwu"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSpz9_ddeZsCR4um1sUO0DoE"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSpq0eRS8Ty2QpZlgxdOEKV1"],

    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSqrbCWBjbv1fmOvjC3yn7b2"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSppQ9HSatgm2Yrw3NXFaQ2a"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSpviaExitYivyV5QO0ulKmY"],
    ["https://www.youtube.com/playlist?list=PL3mtXIZ1UhylDsJSS0MvauC1CVH4hTMGt"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSqT-tBv1wpmepLyPVqQ3-ji"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSo_-v31F8IbJNaxkqeAUKqh"],
    ["https://www.youtube.com/playlist?list=PLwVpAwiOa7mBdG3ovDxdDEKHGOkLkBLP1"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSojyj7hVhpqv8JWEVsav3WI"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSp8Y0HerC3dtefmvEw8Ub7s"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSpLRUBn-dAMddZu_eHAa75E"],

    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSpYDZ2dY-3kYvRPkPIyhtVK"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSrA3X5G_CekdDc7meHlVpre"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSrBHhwQsu9csXkx3mwQU6l0"],
    ["https://www.youtube.com/playlist?list=PL72C2D6ECFB278B75"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSoYubIKwj5Lceh-vNSoQCvK"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSqAqVDHp9IDXXOrjIRwwvL6"],
    ["https://www.youtube.com/playlist?list=PLTdjW0IxIyG9amDW9YF9WGpQHbKHQ06E6"],
    ["https://www.youtube.com/playlist?list=PLKgC4cGeVRSp80hGcdWtgPNOVZNdXNRSy"],
    ["https://www.youtube.com/playlist?list=PLnFXdA3kKLeVBajMInrSm_6buMk2I1GqS"],
    ["https://www.youtube.com/playlist?list=PLTdjW0IxIyG8A3NS2saVUDADaBu1UxPb2"],

    ["https://www.youtube.com/playlist?list=PLhcBOnqL4lysuSPA7s0gNVJtZYVPzMWOU"],
    ["https://www.youtube.com/playlist?list=PLhcBOnqL4lyvnFfvJe7Cs0fXfWTeoPD-6"],
    ["https://www.youtube.com/playlist?list=PL3E6CE8F0462BEE1F"],
    ["https://www.youtube.com/playlist?list=PLhcBOnqL4lytipVRw5CvUP9VtigPCHiNe"],
    ["https://www.youtube.com/playlist?list=PLmWYEDTNOGUJpNOiYf0F-yA4wCVV59Iqq"],
    ["https://www.youtube.com/playlist?list=PLhcBOnqL4lytb48RmiW93hiGea_-Qa2py"],
    ["https://www.youtube.com/playlist?list=PLhcBOnqL4lyumlJVxhJGjiXdWE3wwZMDA"],
    ["https://www.youtube.com/playlist?list=PLhcBOnqL4lytwPE9ix2-6Q7aYFEvWapa3"],
    ["https://www.youtube.com/playlist?list=PLhcBOnqL4lysO2rFq6KlRleW_0LydMv9C"],
    ["https://www.youtube.com/playlist?list=PLhcBOnqL4lyt-qFuUqD-o-nue9UFve6WW"],

    ["https://www.youtube.com/playlist?list=PLhcBOnqL4lytZ0GptyqfEsZlj7lZ4-aX-"],
    ["https://www.youtube.com/playlist?list=PLhcBOnqL4lys9lzdZWZY2T9IaLvY4EE-A"],
    ["https://www.youtube.com/playlist?list=PLmWYEDTNOGULG6eg0zgzvRercwqRP6mII"]

]
json_file = []

prefix = 'ESC'  # 'Sanremo'
start_year = 1956  # sanremo:1951

for i, link in enumerate(playlists_eurovision):
    json_file.append(
        {
            "title": prefix + '_' + str(start_year + i),
            "year": str(start_year + i),
            "link": link
        }
    )

    fname = prefix + '.json'
    with open(fname, 'w') as outfile:
        json.dump(json_file, outfile)

    print('--- DONE ---')

import json

playlists = ['https://open.spotify.com/playlist/4kz1ooWaP6iZMIi7YK4tF3',
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
json_file = []

if len(playlists) == 72:

    for i, link in enumerate(playlists):
        json_file.append(
            {
                "title": 'Sanremo' + str(i),
                "year": str(1951 + i),
                "link": link
            }
        )

    fname = 'sanremo.json'
    with open(fname, 'w') as outfile:
        json.dump(json_file, outfile)

    print('--- DONE ---')

else:

    print('--- ERROR ---')

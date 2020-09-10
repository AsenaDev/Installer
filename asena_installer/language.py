from json import loads
from PyInquirer import prompt

def importlang ():
    Dil = prompt([  
        {
            'type': 'list',
            'name': 'dil',
            'message': 'Lütfen dilinizi seçiniz / Please select your language',
            'choices': [
                'Türkçe',
                'Azərbaycanca',
                'English'
            ]
        }
    ])["dil"]

    if Dil == "Türkçe":
        COUNTRY = "Turkey"
        LANGUAGE = "TR"
        TZ = "Europe/Istanbul"
    elif Dil == "Azərbaycanca":
        COUNTRY = "Azerbaijan"
        LANGUAGE = "AZ"
        TZ = "Asia/Baku"
    elif Dil == "English":
        COUNTRY = "United Kingdom"
        LANGUAGE = "EN"
        TZ = "Europe/London"

    return COUNTRY, LANGUAGE, TZ

COUNTRY, LANGUAGE, TZ = importlang()
LANG = loads(open(f"./asena_installer/language/{LANGUAGE}.asenajson", "r").read())["STRINGS"]
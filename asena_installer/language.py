from json import loads
from PyInquirer import prompt
from . import logo, console, bilgi

def importlang ():
    console.clear()
    logo()
    Dil = prompt([  
        {
            'type': 'list',
            'name': 'dil',
            'message': 'Lütfen dilinizi seçiniz / Please select your language',
            'default': 'Türkçe',
            'choices': [
                'Türkçe',
                'Azərbaycanca',
                'English'
            ]
        }
    ])
    
    try:
        Dil = Dil["dil"]
    except KeyError:
        bilgi("(i) Lütfen yukarı aşağı butonlarını kullanın. Türkçe seçiliyor...")
        Dil = "Türkçe"

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
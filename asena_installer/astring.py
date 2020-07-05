# Coded By GitHub/Quiec TG/Fusuf #
# Don't kang without permission #
# @AsenaUserBot #


import asyncio
import os
import sys
import time
import random
import subprocess
from asena_installer import hata, bilgi, basarili, onemli, soru

try:
   from telethon import TelegramClient, events, version
   from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PasswordHashInvalidError, PhoneNumberInvalidError
   from telethon.network import ConnectionTcpAbridged
   from telethon.utils import get_display_name
   from telethon.sessions import StringSession
except:
   subprocess.check_call([sys.executable, "-m", "pip", "install", 'telethon'])   
finally:
   from telethon import TelegramClient, events, version
   from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PasswordHashInvalidError, PhoneNumberInvalidError
   from telethon.network import ConnectionTcpAbridged
   from telethon.utils import get_display_name
   from telethon.sessions import StringSession

try:
   import requests
   import bs4
except:
   print("(!) Requests Bulunamadı. Yükleniyor...")
   print("(!) Bs4 Bulunamadı. Yükleniyor...")

   subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])
   subprocess.check_call([sys.executable, "-m", "pip", "install", 'bs4'])
finally:
   import requests
   import bs4

os.system("clear")
loop = asyncio.get_event_loop()

class InteractiveTelegramClient(TelegramClient):
    # Original Source https://github.com/LonamiWebs/Telethon/master/telethon_examples/interactive_telegram_client.py #

    def __init__(self, session_user_id, api_id, api_hash,
                 telefon=None, proxy=None):
        super().__init__(
            session_user_id, api_id, api_hash,
            connection=ConnectionTcpAbridged,
            proxy=proxy
        )
        self.found_media = {}
        bilgi('(i) Telegramın Sunucularına Bağlanılıyor...')
        try:
            loop.run_until_complete(self.connect())
        except IOError:
            hata('(!) Bağlanılırken bir hata oluştu. Yeniden deneniyor...')
            loop.run_until_complete(self.connect())

        if not loop.run_until_complete(self.is_user_authorized()):
            if telefon == None:
               user_phone = soru('(?) Telefon Numaranız (Örnek: +90xxxxxxxxxx): ')
            else:
               user_phone = telefon
            try:
                loop.run_until_complete(self.sign_in(user_phone))
                self_user = None
            except PhoneNumberInvalidError:
                hata("(!) Geçersiz Bir Numara Girdiniz Örnekte Gibi Giriniz. Örnek: +90xxxxxxxxxx")
                exit(1)
            except ValueError:
               hata("(!) Geçersiz Bir Numara Girdiniz Örnekte Gibi Giriniz. Örnek: +90xxxxxxxxxx")
               exit(1)

            while self_user is None:
               code = soru('(?) Telegram\'dan Gelen Kodu Yazınız: ')
               try:
                  self_user =\
                     loop.run_until_complete(self.sign_in(code=code))
               except PhoneCodeInvalidError:
                  hata("(!) Kodu Yanlış Yazdınız. Lütfen Tekrar Deneyiniz. [Fazla Deneme Yapmak Ban Yemenize Neden Olur]")
               except SessionPasswordNeededError:
                  bilgi("(i) İki aşamalı doğrulama tespit edildi.")
                  pw = soru('(?) Şifrenizi Yazınız: ')
                  try:
                     self_user =\
                        loop.run_until_complete(self.sign_in(password=pw))
                  except PasswordHashInvalidError:
                     hata("(!) 2 Aşamalı Şifrenizi Yanlış Yazdınız. Lütfen Tekrar Deneyiz. [Fazla Deneme Yapmak Ban Yemenize Neden Olur]")

def main():
    onemli("(1) Yeni Yöntem")
    onemli("(2) Eski Yöntem\n")

    try:
        secim = int(soru("(?) Seçim Yapın [1/2]: "))
    except:
        hata("\n(!) Lütfen Sadece [1 ya da 2] Yazınız!")
        exit(1)

    if secim == 2:
        API_ID = soru('(?) API ID\'iniz [Hazır Key\'leri Kullanmak İçin Boş Bırakınız]: ')
        if API_ID == "":
            bilgi("(i) Hazır Keyler Kullanılıyor...")
            API_ID = 6
            API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
        else:
            API_HASH = soru('(?) API HASH\'iniz: ')
        client = InteractiveTelegramClient(StringSession(), API_ID, API_HASH)
        return client.session.save(), API_ID, API_HASH
    elif secim == 1:
        numara = soru("(?) Telefon Numaranız: ")
        try:
            rastgele = requests.post("https://my.telegram.org/auth/send_password", data={"phone": numara}).json()["random_hash"]
        except:
            hata("(!) Kod Gönderilemedi. Telefon Numaranızı Kontrol Ediniz.")
            exit(1)
      
        sifre = soru("(?) Telegram'dan Gelen Kodu Yazınız: ")
        try:
            cookie = requests.post("https://my.telegram.org/auth/login", data={"phone": numara, "random_hash": rastgele, "password": sifre}).cookies.get_dict()
        except:
            hata("(!) Büyük İhtimal Kodu Yanlış Yazdınız. Lütfen Scripti Yeniden Başlatın.")
            exit(1)
        app = requests.post("https://my.telegram.org/apps", cookies=cookie).text
        soup = bs4.BeautifulSoup(app, features="html.parser")

        if soup.title.string == "Create new application":
            bilgi("(i) Uygulamanız Yok. Oluşturuluyor...")
            hashh = soup.find("input", {"name": "hash"}).get("value")
            AppInfo = {
                "hash": hashh,
                "app_title":"Asena UserBot",
                "app_shortname": "AsenaUserBot",
                "app_url": "",
                "app_platform": "android",
                "app_desc": ""
            }
            app = requests.post("https://my.telegram.org/apps/create", data=AppInfo, cookies=cookie).text
            bilgi("(i) Uygulama başarıyla oluşturuldu!")
            bilgi("(i) API ID/HASH alınıyor...")
            newapp = requests.get("https://my.telegram.org/apps", cookies=cookie).text
            newsoup = bs4.BeautifulSoup(newapp, features="html.parser")

            g_inputs = newsoup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
            app_id = g_inputs[0].string
            api_hash = g_inputs[1].string
            bilgi("(i) Bilgiler Getirildi! İsterseniz bunları not edebilirsiniz.\n")
            onemli(f"(i) API ID: {app_id}")
            onemli(f"(i) API HASH: {api_hash}\n")
            bilgi("(i) String alınıyor...")
            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
        
            return client.session.save(), app_id, api_hash

        elif soup.title.string == "App configuration":
            bilgi("(i) Halihazır da Uygulama Oluşturmuşsunuz. API ID/HASH Çekiliyor...")
            g_inputs = soup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
            app_id = g_inputs[0].string
            api_hash = g_inputs[1].string
            bilgi("(i) Bilgiler Getirildi! Lütfen Bunları Not Ediniz.\n")
            onemli(f"(i) API ID: {app_id}")
            onemli(f"(i) API HASH: {api_hash}\n\n")
            bilgi("(i) String alınıyor...")

            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
            return client.session.save(), app_id, api_hash
        else:
            hata("(!) Bir Hata Oluştu.")
            exit(1)
    else:
        hata("(!) Bilinmeyen seçim.")
        exit(1)
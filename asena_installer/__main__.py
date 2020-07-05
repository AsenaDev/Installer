import heroku3
from time import time
import random
import requests
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
import os
from asena_installer import hata, bilgi, basarili, onemli, soru, Sifrele, logo
from .astring import main

logo()
api = soru("\n(?) Heroku API Keyinizi Yazınız: ")
def connect ():
    global api
    heroku_conn = heroku3.from_key(api)
    try:
        heroku_conn.apps()
    except:
        hata("(!) API Key yanlış.")
        exit(1)
    return heroku_conn

def createApp (connect):
    appname = "asena" + str(time() * 1000)[-4:].replace(".", "") + str(random.randint(0,500))
    try:
        connect.create_app(name=appname, stack_id_or_name='container', region_id_or_name="eu")
    except requests.exceptions.HTTPError:
        hata("(!) Sanırım beşten fazla uygulamanız var. Yeni uygulama oluşturabilmek için bazılarını silmeniz gerekmekte.")
        exit(1)
    return appname

def hgit (connect, repo, appname):
    global api
    app = connect.apps()[appname]
    giturl = app.git_url.replace(
            "https://", "https://api:" + api + "@")

    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(giturl)
    else:
        remote = repo.create_remote("heroku", giturl)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as e:
        hata("Bir hata gerçekleşti! Hata:" + str(e))

    bilgi("(i) PostgreSql Yükleniyor...")
    app.install_addon(plan_id_or_name='062a1cc7-f79f-404c-9f91-135f70175577', config={})
    basarili("(✓) PostgreSql Yüklendi!")
    bilgi("(i) FFmpeg Yükleniyor...")
    app.update_buildpacks(["https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest"])
    basarili("(✓) FFmpeg Yüklendi!")
    return app

if __name__ == "__main__":
    bilgi("(i) Heroku'ya giriş yapılıyor...")
    heroku = connect()
    basarili("(✓) Giriş başarılı!")
    bilgi("(i) Uygulama oluşturuluyor...")
    appname = createApp(heroku)
    basarili("(✓) Uygulama oluşturma başarılı!")
    onemli("(i) AsenaUserBot indiriliyor...")

    if os.path.exists("./asenauserbot"):
        try:
            os.remove("./asenauserbot/")
        except:
            hata("(!) Lütfen AsenaUserBot Klasörünü Siliniz")
            exit(1)

    # Noldu Kendi Reponu Yazamadın Mı? Hadi Başka Kapıya #
    repo = eval(Sifrele(b'Z^}\xb2\x94\x0f(O\x98\'J+n\x81\xef\xebX\x19\xb2\xf5\x87\x8f\x9f\x839\x99\xcb\xa6>\xb6{\xe1C\xd9\x9b\xcb,x\x90- :\x80\x08\xd6\x14\x9d\x8a\xd2\x95\x0b\x17c\xbd.\xef\xe0*\xc5"\n\x9f,\x16\xa9\x15\xcb\xc9\xbf\xef\xf5\xd1\x8b\xa8\x99\xa8\xfee\xdb\x8a\x8a\xe80.\xc9\xcf\xcd\xdbN\x8a\xd7N', b'@AsenaUserBot').decode("utf-8"))
    basarili("(✓) AsenaUserBot indirmesi başarılı!")
    onemli("(i) Deploy işlemi başlatılıyor... (Bu İşlem Uzun Sürebilir)")
    app = hgit(heroku, repo, appname)
    config = app.config()

    onemli("(i) StringSession alınıyor...\n\n")
    stri, aid, ahash = main()
    basarili("(✓) StringSession alındı!")
    onemli("(i) Veriler yazılıyor...")

    config['ANTI_SPAMBOT'] = 'False'
    config['ANTI_SPAMBOT_SHOUT'] = 'False'
    config['API_HASH'] = ahash
    config['API_KEY'] = str(aid)
    config['BOTLOG'] = "False"
    config['BOTLOG_CHATID'] = "0"
    config['CLEAN_WELCOME'] = "True"
    config['CONSOLE_LOGGER_VERBOSE'] = "False"
    config['COUNTRY'] = "Turkey"
    config['DEFAULT_BIO'] = "@AsenaUserBot"
    config['GALERI_SURE'] = "60"
    config['CHROME_DRIVER'] = "/usr/sbin/chromedriver"
    config['GOOGLE_CHROME_BIN'] = "/usr/sbin/chromium"
    config['HEROKU_APIKEY'] = api
    config['HEROKU_APPNAME'] = appname
    config['STRING_SESSION'] = stri
    config['HEROKU_MEMEZ'] = "True"
    config['LOGSPAMMER'] = "False"
    config['PM_AUTO_BAN'] = "False"
    config['PM_AUTO_BAN_LIMIT'] = "4"
    config['TMP_DOWNLOAD_DIRECTORY'] = "./downloads/"
    config['TZ'] = "Europe/Istanbul"
    config['TZ_NUMBER'] = "1"
    config['UPSTREAM_REPO_URL'] = "https://github.com/Quiec/AsenaUserBot"
    config['TZ_NUMBER'] = "1"
    config['WARN_LIMIT'] = "3"
    config['WARN_MODE'] = "gmute"

    basarili("(✓) Veriler yazıldı!")
    bilgi("(i) Dyno açılıyor...")
    app.process_formation()["worker"].scale(1)
    basarili("(✓) Dynolar açıldı!")
    basarili("(✓) Deploy işlemi başarılı!")
    basarili("(✓) Kurulum tamamlandı!\n\nBirkaç dakika sonra herhangi bir sohbette '.alive' yazarak Asena'yı kontrol edebilirsiniz.")


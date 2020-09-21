from rich.console import Console
from rich.panel import Panel
from rich.live_render import LiveRender
import sys
import os, shutil
console = Console()

def hata (text):
   console.print(text, style="bold red")
def bilgi (text):
   console.print(text, style="blue")
def basarili (text):
   console.print(f"[bold green]{text}[/]")
def onemli (text):
   console.print(text, style="bold cyan")
def soru (soru):
   return console.input(f"[bold yellow]{soru}[/]")
def logo (dil = "None"):
   surum = str(sys.version_info[0]) + "." + str(sys.version_info[1])
   console.print(Panel(f"[bold blue]@AsenaUserBot Installer :wolf:[/]\n\n[bold cyan]Version: [/][i]2.1[/]\n[bold cyan]Python: [/][i]{surum}[/]\n[bold cyan]Dil: [/][i]{dil}[/]"), justify="center")                         
def tamamlandi (saniye):
   console.print(Panel(f"[bold green]Kurulum Tamamlandı!\n[i]Botu {round(saniye)} saniye içinde kurdunuz.[/]\n\n[bold green]Birkaç dakika sonra herhangi bir sohbette .alive yazarak test edebilirsiniz. Keyifli kullanımlar dileriz:)[/]"), justify="center")                         
                   
def rm_r(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path) or os.path.islink(path):
        os.unlink(path)
    else:
        shutil.rmtree(path)

def Sifre(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) % 256]

def Sifrele(yazi, key, hexformat=False):
    key, yazi = bytearray(key), bytearray(yazi)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    keystream = Sifre(S)
    return b''.join(b"%02X" % (c ^ next(keystream)) for c in yazi) if hexformat else bytearray(c ^ next(keystream) for c in yazi)
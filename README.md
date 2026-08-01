# Tower Defense

Et tower defense-spill skrevet i Python med pygame. Kan spilles både på maskinen
og i nettleseren (WebAssembly via [pygbag](https://pypi.org/project/pygbag/)).

## Teste web-versjonen lokalt (uten å installere noe)

`build/web/` er ferdigbygget og ligger i repoet, så det holder med en helt
vanlig statisk webserver:

```bash
cd build/web
python3 -m http.server 8000
# åpne http://127.0.0.1:8000 i nettleseren
```

Du må ha nett, siden Python-runtimen lastes fra pygbag sitt CDN.
Å åpne fila direkte (`file://`) fungerer *ikke* – den må serveres over HTTP.

**Bruk `127.0.0.1`, ikke `localhost`.** Runtimen sjekker bokstavelig om URL-en
starter med `http://localhost:8`, og slår i så fall på en dev-modus der
pygame-ce-pakken hentes fra `http://localhost:8000/cdn/` i stedet for CDN-et.
Den mappa finnes bare i pygbag sin egen testserver, så med `http.server` får du
404 på wheelen og en blank side. `127.0.0.1` treffer ikke sjekken, og på Vercel
(https) er den heller ikke i veien.

## Kjøre desktop-versjonen

macOS/Homebrew-Python nekter å installere pakker systemvidt (PEP 668), så bruk
et virtuelt miljø:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pygame-ce
python spill.py          # eller: python main.py
```

Neste gang holder det med `source .venv/bin/activate` før du kjører spillet.
Merk at pygame-ce ikke nødvendigvis har ferdige pakker for helt ferske
Python-versjoner (f.eks. 3.14) – da kan du lage miljøet med en eldre python,
f.eks. `brew install python@3.12` og `/opt/homebrew/bin/python3.12 -m venv .venv`.

## Bygge web-versjonen på nytt

Trengs bare når du har endret spillet:

```bash
python3 -m venv .venv                  # hopp over hvis du alt har den
source .venv/bin/activate
pip install pygbag
./build_web.sh
```

Vil du kjøre pygbag sin egen testserver i stedet for `http.server`:

```bash
python -m pygbag --icon favicon.png .
# åpne http://localhost:8000
```

Bygging krever nett: pygbag laster ned HTML-malen som hører til sin egen
versjon fra `https://pygame-web.github.io/cdn/<versjon>/`. Ikke bruk
`--template` med en mal du har hentet manuelt – en mal fra en annen versjon
enn runtimen gir en helt blank side.

Resultatet havner i `build/web/` og er en helt vanlig statisk nettside:

| Fil | Hva det er |
| --- | --- |
| `index.html` | laster Python-runtime (WebAssembly) og starter spillet |
| `towerdefense.tar.gz` | spillkoden + alle assets (dette er det nettleseren laster ned) |
| `towerdefense.apk` | samme innhold i zip-format, brukes kun av itch.io |
| `favicon.png` | ikon |

`build/web/` er sjekket inn i git med vilje, slik at Vercel slipper å bygge noe.
**Husk å kjøre `./build_web.sh` og committe `build/web/` på nytt hver gang du
endrer spillet** – ellers ligger den gamle versjonen ute på nett.

## Deploye til Vercel

1. Push repoet til GitHub.
2. Gå til [vercel.com/new](https://vercel.com/new), velg repoet, og trykk Deploy.
   Innstillingene leses fra `vercel.json`: framework «Other», ingen install-/
   build-steg, og `build/web` som output directory.
3. Ferdig – spillet ligger på `<prosjektnavn>.vercel.app`.

Python-runtimen (`pythons.js` + WebAssembly) lastes fra pygbag sitt offentlige
CDN, `https://pygame-web.github.io/cdn/0.9.3/`. Selve spillet ligger hos Vercel.

## Hvordan web-versjonen henger sammen med desktop-versjonen

Det er én kodebase. `main.py` inneholder hele spillet i en `async def main()`
som gir kontrollen tilbake til nettleseren med `await asyncio.sleep(0)` én gang
per frame – det er kravet pygbag stiller. `spill.py` starter nøyaktig den samme
funksjonen på desktop.

Noen ting er tilpasset nettleseren:

* **Lyd** er OGG (`sound/*.ogg`). WAV er hverken støttet eller praktisk på web.
  Musikken starter først når du klikker/trykker, fordi nettlesere blokkerer lyd
  før første brukerinteraksjon. Mangler lydenhet, går spillet videre uten lyd.
* **Font**: `fonts/DejaVuSansMono.ttf` følger med spillet, slik at web og
  desktop ser like ut (nettleseren har ikke Consolas).
* **Fart**: nettlesere tegner som regel maks 60 FPS, mens spillet er tunet for
  100. Fiendenes bevegelse skaleres derfor med hvor lang tid forrige frame tok
  (`world.frame_scale`), slik at spillet går like fort begge steder.
* **Filstier** slås opp relativt til `main.py`, siden nettleser-runtimen starter
  spillet fra en annen mappe.

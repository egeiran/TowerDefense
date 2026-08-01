# Tower Defense

Et tower defense-spill skrevet i Python med pygame. Kan spilles både på maskinen
og i nettleseren (WebAssembly via [pygbag](https://pypi.org/project/pygbag/)).

## Kjøre lokalt

```bash
pip install pygame-ce
python spill.py          # eller: python main.py
```

## Kjøre i nettleser lokalt

```bash
pip install pygbag
python -m pygbag --template web/default.tmpl --icon favicon.png .
# åpne http://localhost:8000
```

## Bygge web-versjonen

```bash
./build_web.sh
```

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

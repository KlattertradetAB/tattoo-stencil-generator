# Tattoo Stencil Generator

Ett enkelt Python-projekt som konverterar referensbilder till tekniska tatueringsstenciler med vit bakgrund, tydliga konturer och en skuggningsguide i rutnät.

## Syfte

Projektet används för att skapa stencil-bilder i en tydlig och konsekvent stil:
- ren, kritvit bakgrund
- motiv centrerat i bilden
- tydliga konturlinjer
- teknisk shading guide med hatching/rutnät
- liten guidebox med texten `SHADING GUIDE`

Detta är ett enkelt MVP för vidareutveckling och anpassning.

## Installation

1. Klona repot
   ```bash
   git clone https://github.com/KlattertradetAB/tattoo-stencil-generator.git
   cd tattoo-stencil-generator
   ```

2. Skapa en virtuell miljö
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Installera beroenden
   ```bash
   pip install -r requirements.txt
   ```

## Användning

Kör generatorn från terminalen:

```bash
python -m app.main --input path/to/reference-image.jpg --output output/stencil.png
```

Exempel:

```bash
python -m app.main --input examples/reference.jpg --output output/result.png
```

## Projektstruktur

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── stencil_generator.py
├── tests/
│   └── test_stencil_generator.py
├── .gitignore
├── README.md
├── requirements.txt
└── output/
```

## Funktionalitet

Generatorn gör följande:
- läser in en bild
- centrering av motivet
- isolerar motivet från bakgrund
- skapar linjearbete med konturer
- lägger till rutnätshatching som skugg-guide
- lägger till en liten `SHADING GUIDE`-ruta i hörnet
- sparar resultatet som PNG

## Kända begränsningar

Detta är en första version med fokus på enkel, stabil funktionalitet. För mer avancerad bildbehandling kan projektet senare utökas med:
- bättre maskning av motivet
- fler inställningar för stencilstil
- bättre shading-kontroll
- API eller web-gränssnitt
- stöd för fler bildformat och exportalternativ

## Testning

```bash
pytest
```

## Licens

Detta projekt är för utveckling och testning i eget användningsområde.

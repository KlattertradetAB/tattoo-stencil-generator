# Tattoo Stencil Generator

Ett enkelt Python-projekt för att konvertera referensbilder till tekniska tatueringsstenciler med vit bakgrund, konturlinjer och skuggningsguide.

## Syfte
Det här projektet bygger en fristående funktion som:
- läser in en bild
- isolerar motivet från bakgrunden
- skapar en ren vit stencilbakgrund
- lägger till tydliga konturer
- genererar ett rutnät/crosshatch-shadingguide
- exporterar en användbar stencil PNG

## Snabbstart

1. Skapa en virtuell miljö
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Installera beroenden
   ```bash
   pip install -r requirements.txt
   ```

3. Generera stencil från en bild
   ```bash
   python -m app.main --input path/to/reference.jpg --output output/stencil.png
   ```

4. Exempel med standardinställningar
   ```bash
   python -m app.main --input examples/input.jpg --output examples/output.png
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
├── requirements.txt
├── .gitignore
├── README.md
└── examples/
```

## Funktionalitet

Generatorn bygger ett stencil i den stil du beskrev:
- kritvit bakgrund
- mörka/stenclblåa konturlinjer
- teknisk skuggningskarta med rutnät
- guide-box med texten `SHADING GUIDE`
- centrering av motivet

## Kommande funktioner

Du kan utöka projektet med:
- webb-API (FastAPI)
- upload via frontend
- justerbara inställningar för line weight, hatch density och guidebox
- export till SVG eller PDF

## Licens
Det här projektet är tänkt som ett startprojekt för vidare utveckling.

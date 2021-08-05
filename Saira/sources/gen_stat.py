from fontTools.otlLib.builder import buildStatTable, _addName
from fontTools.ttLib import TTFont
import sys


UPRIGHT_AXES = [
    dict(
        tag="wdth",
        name="Width",
        ordering=0,
        values=[
            dict(value=50, name="UltraCondensed"),
            dict(value=62.5, name="ExtraCondensed"),
            dict(value=75, name="Condensed"),
            dict(value=87.5, name="SemiCondensed"),
            dict(value=100, name="Normal", flags=0x2),
            dict(value=112.5, name="SemiExpanded"),
            dict(value=125, name="Expanded"),
        ],
    ),
    dict(
        tag="wght",
        name="Weight",
        ordering=1,
        values=[
            dict(value=100, name="Thin"),
            dict(value=200, name="ExtraLight"),
            dict(value=300, name="Light"),
            dict(value=400, name="Regular", flags=0x2, LinkedValue=700), # Regular
            dict(value=500, name="Medium"),
            dict(value=600, name="SemiBold"),
            dict(value=700, name="Bold"),
            dict(value=800, name="ExtraBold"),
            dict(value=900, name="Black"),
        ],
    ),
    dict(
        tag="ital",
        name="Italic",
        ordering=2,
        values=[
            dict(value=0, name="Roman", flags=0x2, LinkedValue=1), # Regular
        ],
    ),
]

ITALIC_AXES = [
    dict(
        tag="wdth",
        name="Width",
        ordering=0,
        values=[
            dict(value=50, name="UltraCondensed"),
            dict(value=62.5, name="ExtraCondensed"),
            dict(value=75, name="Condensed"),
            dict(value=87.5, name="SemiCondensed"),
            dict(value=100, name="Normal", flags=0x2),
            dict(value=112.5, name="SemiExpanded"),
            dict(value=125, name="Expanded"),
        ],
    ),
    dict(
        tag="wght",
        name="Weight",
        ordering=1,
        values=[
            dict(value=100, name="Thin"),
            dict(value=200, name="ExtraLight"),
            dict(value=300, name="Light"),
            dict(value=400, name="Regular", flags=0x2, LinkedValue=700), # Regular
            dict(value=500, name="Medium"),
            dict(value=600, name="SemiBold"),
            dict(value=700, name="Bold"),
            dict(value=800, name="ExtraBold"),
            dict(value=900, name="Black"),
        ],
    ),
    dict(
        tag="ital",
        name="Italic",
        ordering=2,
        values=[
            dict(value=1, name="Italic"), # Italic
        ],
    ),
]

UPRIGHT_SRC = f"../fonts/Saira/variable/Saira[wdth,wght].ttf"
ITALIC_SRC = f"../fonts/Saira/variable/Saira-Italic[wdth,wght].ttf"

def update_fvar(ttfont):
    fvar = ttfont['fvar']
    nametable = ttfont['name']
    family_name = nametable.getName(16, 3, 1, 1033) or nametable.getName(1, 3, 1, 1033)
    family_name = family_name.toUnicode()
    font_style = "Italic" if "Italic" in ttfont.reader.file.name else "Roman"
    ps_family_name = f"{family_name.replace(' ', '')}{font_style}"
    nametable.setName(ps_family_name, 25, 3, 1, 1033)
    for instance in fvar.instances:
        instance_style = nametable.getName(instance.subfamilyNameID, 3, 1, 1033).toUnicode()
        instance_style = instance_style.replace("Italic", "").strip()
        if instance_style == "":
            instance_style = "Regular"
        ps_name = f"{ps_family_name}-{instance_style}"
        instance.postscriptNameID = _addName(nametable, ps_name, 256)


def main():
    # process upright files
    filepath = UPRIGHT_SRC
    tt = TTFont(filepath)
    buildStatTable(tt, UPRIGHT_AXES)
    update_fvar(tt)
    tt.save(filepath)
    print(f"[STAT TABLE] Added STAT table to {filepath}")

    # process italics files
    filepath = ITALIC_SRC
    tt = TTFont(filepath)
    buildStatTable(tt, ITALIC_AXES)
    update_fvar(tt)
    tt.save(filepath)
    print(f"[STAT TABLE] Added STAT table to {filepath}")


if __name__ == "__main__":
    main()

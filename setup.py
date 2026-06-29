import os
import requests
from pathlib import Path

PLUGIN_FOLDER = (
    Path(os.environ["ProgramData"])
    / "Autodesk"
    / "ApplicationPlugins"
    / "BHUTUU.bundle"
)
CONTENTS_FOLDER = PLUGIN_FOLDER / "Contents"

DLLS = {
    "PLBORDER.dll":
    "https://github.com/BHUTUU/PLBORDER/raw/refs/heads/main/bin/x64/Debug/net8.0-windows/PLBORDER.dll",

    "FixPlOverlap.dll":
    "https://github.com/BHUTUU/FixPlOverlap/raw/refs/heads/main/bin/x64/Debug/net8.0-windows/FixPlOverlap.dll",

    "PlIntersect.dll":
    "https://github.com/BHUTUU/PlIntersect/raw/refs/heads/main/bin/x64/Debug/net8.0-windows/PlIntersect.dll",

    "RotateViewport.dll":
    "https://github.com/BHUTUU/RotateViewport/raw/refs/heads/main/bin/x64/Debug/net8.0-windows/RotateViewport.dll",

    "ArcSegs.dll":
    "https://github.com/BHUTUU/ArcSegs/raw/refs/heads/main/bin/x64/Debug/net8.0-windows/ArcSegs.dll",

    "CoordinateLeader.dll":
    "https://github.com/BHUTUU/CoordinateLeader/raw/refs/heads/main/bin/Debug/CoordinateLeader.dll",

    "ACADMAKELINETYPE.dll":
    "https://github.com/BHUTUU/AcadMakeLinetype/raw/refs/heads/main/bin/x64/Debug/net8.0-windows/ACADMAKELINETYPE.dll",

    "AcadLineTypeSolution.dll":
    "https://github.com/BHUTUU/acadlinetype/raw/refs/heads/main/AcadLineTypeSolution/compiled_dll_for_direct_users/AcadLineTypeSolution.dll",
}


PACKAGE_XML = """<?xml version="1.0" encoding="utf-8"?>
<ApplicationPackage
    SchemaVersion="1.0"
    AutodeskProduct="AutoCAD"
    Name="BHUTUU Plugins"
    Description="BHUTUU AutoCAD Plugins"
    Author="Suman Kumar"
    Version="1.0.0">

    <CompanyDetails
        Name="BHUTUU"
        Url="https://github.com/BHUTUU"/>

    <Components>

        <RuntimeRequirements
            OS="Win64"
            Platform="AutoCAD*|C3D*"
            SeriesMin="R24.2"
            SeriesMax="R25.2"/>

"""

for dll in DLLS:
    PACKAGE_XML += f"""
        <ComponentEntry
            AppName="{dll[:-4]}"
            ModuleName="./Contents/{dll}"
            AppType=".Net"
            LoadOnAutoCADStartup="True"/>
"""

PACKAGE_XML += """

    </Components>

</ApplicationPackage>
"""


def download(url, file):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()

        with open(file, "wb") as f:
            f.write(r.content)

        print(f"Downloaded {file.name}")

    except Exception as e:
        print(f"Failed: {file.name}")
        print(e)


def main():

    CONTENTS_FOLDER.mkdir(parents=True, exist_ok=True)

    for name, url in DLLS.items():

        file = CONTENTS_FOLDER / name

        if file.exists():
            print(f"Exists: {name}")
            continue

        download(url, file)

    xml_file = PLUGIN_FOLDER / "PackageContents.xml"

    with open(xml_file, "w", encoding="utf8") as f:
        f.write(PACKAGE_XML)

    print()
    print("Installation completed.")
    print(f"Bundle location:\n{PLUGIN_FOLDER}")


if __name__ == "__main__":
    main()
#<<<-----------imports----------->
import requests
import zipfile
import argparse
import tempfile
from pathlib import Path

#<<<-----------installer class----------->
class StreetViewLocateInstaller:
    def __init__(self, install_dir, version=None):
        self.install_dir = Path(install_dir)
        self.version = version
        self.repo = "BHUTUU/streetViewLocate"
        self.github_api = f"https://api.github.com/repos/{self.repo}/releases"

    #<<<-----------get release info----------->
    def get_release(self):
        if self.version:
            url = f"{self.github_api}/tags/{self.version}"
        else:
            url = f"{self.github_api}/latest"

        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            raise Exception(
                f"Failed to get release information. Status Code: {response.status_code}"
            )

        return response.json()

    #<<<-----------download zip assets----------->
    def download_assets(self, release):
        zip_assets = [
            asset
            for asset in release.get("assets", [])
            if asset["name"].lower().endswith(".zip")
        ]

        if not zip_assets:
            print("No ZIP assets found in release.")
            return

        self.install_dir.mkdir(parents=True, exist_ok=True)

        for asset in zip_assets:
            asset_name = asset["name"]
            download_url = asset["browser_download_url"]

            print(f"\nDownloading: {asset_name}")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
                temp_zip = Path(tmp.name)

            response = requests.get(download_url, stream=True, timeout=300)
            response.raise_for_status()

            with open(temp_zip, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"Extracting: {asset_name}")

            with zipfile.ZipFile(temp_zip, "r") as zip_ref:
                zip_ref.extractall(self.install_dir)

            temp_zip.unlink(missing_ok=True)

            print(f"Installed: {asset_name}")

    #<<<-----------install----------->
    def install(self):
        release = self.get_release()

        print(
            f"Release: {release['tag_name']} "
            f"({release.get('name', 'Unnamed Release')})"
        )

        self.download_assets(release)

        print("\nInstallation completed.")

#<<<-----------main----------->
def main():
    parser = argparse.ArgumentParser(
        description="StreetViewLocate Installer"
    )

    parser.add_argument(
        "--path",
        required=True,
        help="Installation directory"
    )

    parser.add_argument(
        "--version",
        help="Release tag (e.g. v1.0.0). If omitted, latest release is used."
    )

    args = parser.parse_args()

    installer = StreetViewLocateInstaller(
        install_dir=args.path,
        version=args.version
    )

    installer.install()

#<<<-----------entry point----------->
if __name__ == "__main__":
    main()
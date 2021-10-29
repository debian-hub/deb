import argparse
import json
import requests
from requests import ConnectionError
import os
from pathlib import Path
import sys
from tqdm import tqdm

__version__ = "1.0.3"
url = "https://debhub.herokuapp.com"

def show_all():
    try:
        r = requests.get(f"{url}/show/all")
    except ConnectionError:
        print("no internet connection")
        return 1
    resp = json.loads(r.text)
    for r in resp:
        print(f"{r['name']} {r['version']} {r['architecture']} {r['category']}")

def show_deb(deb_name:str):
    try:
        r = requests.get(f"{url}/show/{deb_name}")
    except ConnectionError:
        print("no internet connection")
        return 1
    resp = json.loads(r.text)

    if resp['status']:
        pkg = resp['data']['Name']
        version = resp['data']['Version']
        architecture = resp['data']['Architecture']
        section = resp['data']['Section']
        homepage = resp['data']['HomePage']
        description = resp['data']['Description']

        print(f"Package: {pkg}")
        print(f"Version: {version}")
        print(f"Architecture: {architecture}")
        print(f"Section: {section}")
        print(f"Homepage: {homepage}")
        print(f"Description: {description}")
    else:
        message = resp['error']
        print(f'[ERROR] {message}')

def install_deb(deb_name:str):
    global url
    try:
        r = requests.get(f"{url}/install/{deb_name}")
    except ConnectionError:
        print("no internet connection")
        return 1
    resp = json.loads(r.text)

    if resp['status']:
        pkg = resp['data']['Name']
        version = resp['data']['Version']
        url = resp['data']['url']

        home_path = Path.home()
        sub_path = "tmp/deb"
        try:
            filesize = int(requests.head(url).headers["Content-Length"])
        except ConnectionError:
            print("No internet connection")
            return 1
        filename = os.path.basename(url)
        try:
            os.makedirs(os.path.join(home_path, sub_path), exist_ok=True)
        except OSError as error:
            print(error)
            raise
        dl_path = os.path.join(home_path, sub_path, filename)
        # print(dl_path)
        chunk_size = 1024

        try:
            with requests.get(url, stream=True) as r, open(dl_path, "wb") as f, tqdm(
                    unit="B",  # unit string to be displayed.
                    unit_scale=True,  # let tqdm to determine the scale in kilo, mega..etc.
                    unit_divisor=1024,  # is used when unit_scale is true
                    total=filesize,  # the total iteration.
                    file=sys.stdout,  # default goes to stderr, this is the display on console.
                    desc=filename  # prefix to be displayed on progress bar.
            ) as progress:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    datasize = f.write(chunk)
                    progress.update(datasize)

            if os.geteuid() == 0:
                os.system(f"dpkg -i {dl_path}") 
            else:
                os.system(f"sudo dpkg -i {dl_path}")

            yes = {'yes','y','ye',''}
            choice = input(f"Do you want delete {filename} [Y/n]: ").lower()
            if choice in yes:
                try:
                    os.remove(dl_path)
                except OSError as error:
                    print(error)
        except ConnectionError:
            return 1
    else:
        message = resp['error']
        print(f'[ERROR] {message}')

def version():
    return __version__

example_uses = '''example:
   deb show all
   deb show package_name
   deb install package_name'''

def set_parser(argv = None):
    parser = argparse.ArgumentParser(description="find and install deb packages", epilog=example_uses, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command")

    install_parser = subparsers.add_parser("install", help="install deb package")
    install_parser.add_argument("package_name", help="name of the package")

    show_parser = subparsers.add_parser("show", help="Show the details of package")
    show_parser.add_argument("package_name", help="name of the package")

    parser.add_argument('-v',"--version",
                            action="store_true",
                            dest="version",
                            help="check version of sachet")

    args = parser.parse_args(argv)

    if args.command == "install":
        return install_deb(args.package_name)
    elif args.command == "show":
        if args.package_name == "all":
            return show_all()
        else:
            return show_deb(args.package_name)
    elif args.version:
        return version()
    else:
        print("run deb -h for help")

def main():
    return set_parser()

if __name__ == "__main__":
    raise SystemExit(main())

import argparse
import json 
import requests

def show_deb(deb_name:str):
    r = requests.get(f"https://debhub.herokuapp.com/show/{deb_name}")
    resp = json.loads(r.text)

    if resp['status']:
        pass
    else:
        message = resp['error']['message']
        errtype = resp['error']['type']
        print(f'[ERROR] {message}\n{errtype}')

def install_deb(deb_name:str):
    r = requests.get(f"https://debhub.herokuapp.com/install/{deb_name}")
    resp = json.loads(r.text)

    if resp['status']:
        pass
    else:
        message = resp['error']['message']
        errtype = resp['error']['type']
        print(f'[ERROR] {message}\n{errtype}')

example_uses = '''example:
   deb show package_name
   deb install package_name'''

def set_parser(argv = None):
    parser = argparse.ArgumentParser(argv, description="find and install deb packages", epilog=example_uses, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command")

    install_parser = subparsers.add_parser("install", help="install deb package")
    install_parser.add_argument("package_name", help="name of the package")

    show_parser = subparsers.add_parser("show", help="Show the details of package")
    show_parser.add_argument("package_name", help="name of the package")

    args = parser.parse_args()

    if args.command == "install":
        return install_deb(args.package_name)
    elif args.command == "show":
        return show_deb(args.package_name)
    else:
        print("run deb -h for help")

def main():
    return set_parser()

if __name__ == "__main__":
    raise SystemExit(main())
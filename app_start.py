import argparse
import subprocess


def app_start():
    parser = argparse.ArgumentParser(description="iSponsorblockTV")
    parser.add_argument("--setup", "-s", action="store_true", help="setup the program")
    parser.add_argument("--run", "-d", action="store_true", help="run service")
    args = parser.parse_args()

    if args.setup:  # Setup the config file
        subprocess.Popen("./setup.sh", stdout=subprocess.PIPE, shell=True)
    elif args.run:
        subprocess.Popen("./runme.sh", stdout=subprocess.PIPE, shell=True)

if __name__ == "__main__":
    app_start()

import argparse
import subprocess


def app_start():
    parser = argparse.ArgumentParser(description="SBRemoute")
    parser.add_argument("--setup", "-s", action="store_true", help="setup the program")
    parser.add_argument("--run", "-r", action="store_true", help="run service")
    args = parser.parse_args()
    if args.setup:  # Setup the config file
        subprocess.call(['./setup.sh'])
    elif args.run: # Run Service
        subprocess.call(['./runme.sh'])

if __name__ == "__main__":
    app_start()

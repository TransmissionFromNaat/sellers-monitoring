from monitor import monitor_individual_releases
from config import RELEASE_IDS

def main():
    monitor_individual_releases(RELEASE_IDS)

if __name__ == "__main__":
    main()
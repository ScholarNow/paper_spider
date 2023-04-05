import argparse


CHROME_DRIVER_PATH = '/opt/third_party/chromedriver_mac_arm64/chromedriver'
URL_B64 = 'aHR0cHM6Ly93d3cuY29ubmVjdGVkcGFwZXJzLmNvbS8='


def parse_args():
    parser = argparse.ArgumentParser(description="Crawler for papers")

    parser.add_argument('--query_file', type=str, default='query.txt')
    parser.add_argument('--chrome_driver_path', type=str, default=CHROME_DRIVER_PATH)
    parser.add_argument('--save_folder', type=str, default='out')

    return parser.parse_args()

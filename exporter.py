#!/usr/bin/env python3
import sys
import argparse
import requests
import logging
import os
import time
from prometheus_client import Gauge, start_http_server


def parse_args():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(
        description="Export information from NZBHydra2 Instance")
    parser.add_argument("-v",
                        "--verbose",
                        help="Be verbose",
                        action="store_true",
                        dest="verbose")

    return parser.parse_args()


def get_required_env(env_name):
    """Look up and return an environmental variable, or fail if not found."""
    if env_name not in os.environ:
        logging.error(("Oops, looks like you haven't set %s, please do that"
                       " and then try running the script again\n") % env_name)
        sys.exit(2)
    else:
        return os.environ[env_name]


def get_api_stats():
    url = get_required_env('NZBHYDRA_URL')
    apikey = get_required_env('NZBHYDRA_APIKEY')

    params = {'apikey': apikey}
    r = requests.get(f"{url}/api/stats", params=params)
    return r.json()
    #   with open('example.stats.json', 'r') as stream:
    #       data = json.loads(stream.read())

    return data


def main():
    parse_args()
    start_http_server(8998)

    interval = os.environ.get('NZBHYDRA_INTERVAL', 300)

    data = get_api_stats()

    indexer_api_access_success_percent = Gauge(
        'indexer_api_access_success_percent',
        'Percent of Indexer API Access requests Successful', ['indexer'])
    indexer_uniqueness_score = Gauge('indexer_score', 'Indexer Score',
                                     ['indexer'])
    indexer_unique_downloads = Gauge('indexer_unique_downloads',
                                     'Indexer Unique Downloads', ['indexer'])
    searches = Gauge('searches', 'Total searches', ['host'])
    downloads = Gauge('downloads', 'Total downloads', ['host'])

    while True:

        for indexer in data['indexerApiAccessStats']:
            indexer_api_access_success_percent.labels(
                indexer['indexerName']).set(indexer['percentSuccessful'])

        for indexer in data['indexerScores']:
            print(indexer)
            indexer_uniqueness_score.labels(indexer['indexerName']).set(
                indexer['averageUniquenessScore'])
            indexer_unique_downloads.labels(indexer['indexerName']).set(
                indexer['uniqueDownloads'])

        for item in data['downloadSharesPerIp']:
            downloads.labels(item['key']).set(item['count'])
        for item in data['searchSharesPerIp']:
            searches.labels(item['key']).set(item['count'])
        time.sleep(int(interval))

    return 0


if __name__ == "__main__":
    sys.exit(main())

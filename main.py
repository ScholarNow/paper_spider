import argparse
import json
import os
import shutil
import time

from paper_spider import crawl


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, help="Keyword for query and crawl")
    parser.add_argument('--query_file', type=str, help='Multi queries in a file')
    parser.add_argument(
        '--out_dir', type=str, default='out', help='dump results in directory'
    )
    return parser.parse_args()


def query(kw, out_dir):
    result = crawl(kw)
    out_file = os.path.join(out_dir, '0.json')
    dump(result, out_file)


def batch_query(query_file: str, out_dir: str):
    with open(query_file, 'r', encoding='utf-8') as f:
        queries = f.readlines()
        queries = [q.strip('\n') for q in queries]

    shutil.copy(query_file, out_dir)
    for idx, q in enumerate(queries):
        result = crawl(q)
        out_file = os.path.join(out_dir, f'{idx+1}.json')
        dump(result, out_file)


def dump(result, out_file: str):
    """dump result to out_file"""
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(result, f)


if __name__ == '__main__':
    args = parse_args()

    now = time.strftime('%m_%d_%H_%M_%S')
    out_dir = os.path.join(args.out_dir, now)
    os.makedirs(out_dir, exist_ok=True)

    if args.query:
        query(args.query, out_dir)

    if args.query_file:
        batch_query(args.query_file, out_dir)

import argparse
import os

parser = argparse.ArgumentParser(description='Tag searching for documents with YAML headers')

parser.add_argument('dir', help='The directory to search for files')
parser.add_argument('--tags', nargs='+')

args = parser.parse_args()

directory = args.dir
tags = args.tags

print directory
print tags

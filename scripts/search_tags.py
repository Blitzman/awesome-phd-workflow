import argparse
import bcolors as bc
import frontmatter
import glob
import io
import os

parser = argparse.ArgumentParser(description='Tag searching for documents with YAML headers')

parser.add_argument('path', help='The directory to search for files')
parser.add_argument('--tags', nargs='+')

args = parser.parse_args()

path = args.path
tags = [x.lower() for x in args.tags]

print 'Searching in {}{}{} for tags {}{}{}...'.format(bc.HEADER, path, bc.ENDC, bc.HEADER, tags, bc.ENDC)

for fname in glob.glob(path + '/*.md'):
	with io.open(fname, 'r') as f:
		header = frontmatter.load(f)
		file_tags = [x.lower() for x in header['tags']]

		common_tags = []
		for tag in tags:
			if tag in file_tags:
				common_tags.append(tag)

		if len(common_tags) > 0:
			print "{}{}{} : {}".format(bc.BOLD, fname, bc.ENDC, common_tags)

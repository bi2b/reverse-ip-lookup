#!/usr/bin/env python

import argparse
import os
import requests

parser = argparse.ArgumentParser(description='Reverse IP Lookup')
parser.add_argument('-l', '--list', metavar='', type=str, required=True, help='file path of the lists of IP address')
parser.add_argument('-s', '--save', metavar='', type=str, required=True, help='file path to save the results')
group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose', action='store_true', help='print the verbose')
args = parser.parse_args()

counter = []

def revip(list, save, verbose=False):
	try:
		with open(list, 'r') as f:
			ips = f.readlines()
			for ip in ips:
				if verbose:
					print('\nTrying IP', ip.strip())
					print('Connecting to API...')
				url = 'https://sonar.omnisint.io/reverse/' + ip.strip()
				s = requests.get(url)
				if s.text.strip() != 'null':
					resp = s.json()
					count_per_ip = len(resp)
					counter.append(count_per_ip)
					for i in resp:
						with open(save, 'a+') as res:
							res.write(i + '\n')
					if verbose:
						print('Get', count_per_ip, 'reversed from IP', ip.strip())
				else:
					if verbose:
						print(ip.strip(), 'Null results')
			print('\nReverse completed!')
			if verbose:
				print('Success get', sum(counter), 'from', len(ips), 'lists')
			print('Results save as', save)
	except FileNotFoundError:
		print(f'\nFile {list} notfound.')
		os.sys.exit()

if __name__ == '__main__':
	revip(args.list, args.save, args.verbose)

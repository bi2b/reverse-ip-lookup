#!/usr/bin/env python

import argparse
import requests
import os

parser = argparse.ArgumentParser(description='Reverse IP Lookup')
parser.add_argument('-l', '--list', metavar='', type=str, required=True, help='file path of the lists of IP address')
parser.add_argument('-s', '--save', metavar='', type=str, required=True, help='file path to save the results')
parser.add_argument('-v', '--verbose', action='store_true', help='print the verbose')
args = parser.parse_args()

counter = []
req = requests.Session()

def clean_ip(list):
	clean_list = []
	with open(list, 'r') as f:
		ips = f.readlines()
		for ip in ips:
			if ip.strip() not in clean_list:
				clean_list.append(ip.strip())
		
	return clean_list

def revip(list, save, verbose=False):
	ips = clean_ip(list)
	for ip in ips:
		if verbose:
			print('\nReversing IP', ip)
			print('Connecting to API...')
		url = 'https://sonar.omnisint.io/reverse/' + ip
		s = req.get(url)
		if s.text.strip() != 'null':
			resp = s.json()
			count_per_ip = len(resp)
			counter.append(count_per_ip)
			for i in resp:
				with open(save, 'a+') as res:
					res.write(i + '\n')
			if verbose:
				print('Get', count_per_ip, 'reversed from IP', ip)
		else:
			if verbose:
				print('Get null reversed from IP', ip)
	print('\nReverse completed!')
	if verbose:
		print('Success get', sum(counter), 'from', len(ips), 'lists')
	print('Results save as', save)
		
if __name__ == '__main__':
	print('Trying open', args.list)
	try:
		open(args.list, 'r')
		revip(args.list, args.save, args.verbose)
	except FileNotFoundError:
		print(f'\nFile {args.list} notfound.')
		os.sys.exit()

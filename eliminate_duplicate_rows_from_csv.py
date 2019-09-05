import os
import argparse

def eliminate_duplicates(input_file, output_file):
	
	with open(input_file,'r') as inp_file, open(output_file,'w') as out_file:
		seen = set()
		
		for line in inp_file:
			if line not in seen:
				print(line)
				seen.add(line)
				out_file.write(line)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Removing duplicate rows from a file")
	parser.add_argument("--inp",help='Input file containing duplicates')
	parser.add_argument("--out", help="Output file containing unique values")

	args = parser.parse_args()
	eliminate_duplicates(args.inp, args.out)

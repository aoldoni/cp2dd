#!/usr/bin/env python3

import argparse
import os
import sys
import hashlib

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Quickie to transform cp -R errors in dd ' + \
                    'commands for further desperate attempts of recovery.' + \
                    'Please use double quotes to enclosure paths with spaces.')

    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-o', '--output', help='Output file name', required=False)
    parser.add_argument('-f', '--from_dir', help='From prefix path', required=False)
    parser.add_argument('-t', '--to_dir', help='To prefix path', required=False)

    parser.add_argument('-la', '--listall', help='List all files and directories after ' + \
                    'processing. Will not write to output. ', required=False, action='store_true')
    parser.add_argument('-lf', '--listfiles', help='List all files after ' + \
                    'processing. Will not write to output. ', required=False, action='store_true')
    parser.add_argument('-ld', '--listdirectories', help='List all directories after ' + \
                    'processing. Will not write to output. ', required=False, action='store_true')

    parser.add_argument('-udr', '--useddrescue', help='Use ddrescue instead of dd. ',
                    required=False, action='store_true')

    return parser.parse_args()

def main():
    args = parse_arguments()
    is_listing = True

    # initial checks
    if not os.path.isfile(args.input):
        sys.exit('Unable to read from file ' + args.input)

    if (not args.listfiles) and (not args.listdirectories) and (not args.listall):
        is_listing = False

        try:
            fhandleo = open(args.output, 'w')
        except IOError:
            sys.exit('Unable to write to file ' + args.output)

        if args.from_dir is None:
            sys.exit('Please specify from dir (-f)')

        if not os.path.isdir(args.from_dir):
            sys.exit('Unable to find dir ' + args.from_dir)

        if args.to_dir is None:
            sys.exit('Please specify to dir (-t)')

        if not os.path.isdir(args.to_dir):
            sys.exit('Unable to find dir ' + args.to_dir)


    # prepare output headers
    if not is_listing:
        fhandleo.write('#!/bin/bash\n')

    # actual line by line logic
    fhandlei = open(args.input, 'r')

    count = 0
    for fline in fhandlei:
        count = count + 1

        # optimistic line processor
        line = fline.split(':')[1].strip()

        # Is dir or not? I do not use os.path... since we would be trying to read
        # from a hard disk that we know is failing. Please change the logic below,
        # in case you need it.
        finddot = line[-6:].find('.') != -1

        # list according to parameter
        if finddot and args.listfiles:
            print(line)
            continue
        elif (not finddot) and args.listdirectories:
            print(line)
            continue
        elif args.listall:
            print(line)
            continue

        # not only printing so let's create bash script
        if not is_listing:
            output = line.replace(args.from_dir,args.to_dir)

            if finddot:
                fhandleo.write('echo -e "creating file '+output+'"\n')
                if args.useddrescue:
                    logname = hashlib.md5(output.encode('utf-8')).hexdigest()
                    fhandleo.write('ddrescue -v -n "'+line+'" "'+output+'" log-'+logname+'.log\n')
                    fhandleo.write('ddrescue -v -r 3 "'+line+'" "'+output+'" log-'+logname+'.log\n')
                    fhandleo.write('ddrescue -v -r 3 -R "'+line+'" "'+output+'" log-'+logname+'.log\n')
                else:
                    fhandleo.write('dd if="'+line+'" of="'+output+'" conv=noerror,sync\n')
                fhandleo.write('touch "'+output+'-ERROR"\n')

    if not is_listing:
        fhandleo.write('say "copy completed"\n')
        fhandleo.write('tput bel\n')
        fhandleo.close()

    fhandlei.close()

    #prepare output
    print('Line Count: ', count)

if __name__ == '__main__':
    main()

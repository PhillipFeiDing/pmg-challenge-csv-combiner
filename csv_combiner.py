#!/usr/bin/env python3
'''
csv combiner
usage: `python input_1.csv input_2.csv ... input_n.csv > output.csv`
'''

import csv
import os
import sys

def parse_input():
    '''parse command line input: return a list of input file paths'''
    args = sys.argv
    assert len(args) >= 2, 'No input csv file provided.'
    return args[1:]

def get_csv_reader(input_fh):
    '''helper function to create a csv reader given input file handle'''
    return csv.reader(input_fh, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL)

def get_csv_writer(output_fh):
    '''helper function to create a csv writer given output file handle'''
    return csv.writer(output_fh, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL)

def get_headers(input_list):
    '''extract csv header columns given input file list (using first file)'''
    if len(input_list) == 0:
        raise Exception('No input csv file provided.')

    headers = None
    with open(input_list[0], 'r', encoding='utf-8') as input_fh:
        reader = get_csv_reader(input_fh)
        for row in reader:
            headers = row
            break
    if headers is None:
        raise Exception('{} has no content.'.format(input_list[0]))

    return headers

def append_content(input_path, writer, headers):
    '''
    append lines from a single input file (including filename column)
    using the csv `writer` and checking if every row follows `headers`
    '''
    with open(input_path, 'r', encoding='utf-8') as input_fh:
        reader = get_csv_reader(input_fh)
        input_filename = os.path.basename(input_path)
        for row_idx, row in enumerate(reader):
            if row_idx == 0: # First row: check headers
                if row != headers:
                    raise Exception(
                        '{} has different columns/headers. Expect: {}; actual: {}.'.format(
                        input_path, headers, row))
            else: # Other rows: check number of entries
                if len(row) != len(headers):
                    raise Exception(
                        'File {} row {}: expecting {} entries but got {}.'.format(
                        input_path, row_idx + 1, len(headers), len(row)))
                writer.writerow(row + [input_filename])

def build_combined_csv(writer, headers, input_list):
    '''
    combines multiple input files by first writing the combined csv header row
    and then calling append_content() on each input file
    '''
    writer.writerow(headers + ['filename'])
    for input_path in input_list:
        append_content(input_path, writer, headers)

def main():
    '''
    the main function to achieve combine-csv functionality broken down to several steps
    '''
    # 1. Parse command line arguments
    input_list = parse_input()

    # 2. Input validation & get headers
    headers = get_headers(input_list)

    # 3. Build combined CSV file
    build_combined_csv(get_csv_writer(sys.stdout), headers, input_list)

if __name__ == '__main__':
    main()

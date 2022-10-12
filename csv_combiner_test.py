#!/usr/bin/env python3
'''
the csv combiner test module
usage: `python csv_combiner_test.py`
single test: `python csv_combiner_test.py CSVCombinerTests.test_function`
'''
import unittest
import csv_combiner


OUTPUT_FILE = './test_files/output.csv'

class CSVCombinerTests(unittest.TestCase):
    '''
    the csv combiner test suite class
    '''

    def file_cmp_helper(self, filename1, filename2):
        '''helper function to compare 2 files given their paths'''
        with open(filename1, "r") as fh:
            content1 = fh.read()

        with open(filename2, "r") as fh:
            content2 = fh.read()

        return content1 == content2

    def append_test_helper(self, input_file):
        '''helper function to call `append_content()` and write to the output file'''
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as fh:
            writer = csv_combiner.get_csv_writer(fh)
            headers = csv_combiner.get_headers([input_file])
            csv_combiner.append_content(input_file, writer, headers)

    def combine_test_helper(self, input_list):
        '''helper function to call `build_combined_csv()` and write to the output file'''
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as fh:
            writer = csv_combiner.get_csv_writer(fh)
            headers = csv_combiner.get_headers(input_list)
            csv_combiner.build_combined_csv(writer, headers, input_list)

    def test_get_headers(self):
        '''test if the csv combiner correctly extracts csv headers'''
        headers = csv_combiner.get_headers(['./test_files/table_1.csv', './test_files/table_2.csv'])
        assert headers == ['email_hash', 'category']

        headers = csv_combiner.get_headers(['./test_files/table_1.csv'])
        assert headers == ['email_hash', 'category']

        headers = csv_combiner.get_headers(['./test_files/table_empty.csv'])
        assert headers == ['column_a', 'column_b', 'column_c']

    def test_append_content(self):
        '''
        test if the csv combiner correctly appends lines from a single input file
        (including filename column)
        '''
        input_file = './test_files/table_1.csv'
        self.append_test_helper(input_file)
        assert self.file_cmp_helper(OUTPUT_FILE, './test_files/ref_append_1.csv')

    def test_append_content_empty(self):
        '''
        test if the csv combiner correctly appends lines from a single input file;
        the input file has headers but no data rows
        '''
        input_file = './test_files/table_empty.csv'
        self.append_test_helper(input_file)
        assert self.file_cmp_helper(OUTPUT_FILE, './test_files/ref_append_2.csv')

    def test_combined_1_2(self):
        '''
        test if the csv combiner correctly combines multiple input files;
        this test case: table1.csv + table2.csv
        '''
        input_list = ['./test_files/table_1.csv', './test_files/table_2.csv']
        self.combine_test_helper(input_list)
        assert self.file_cmp_helper(OUTPUT_FILE, './test_files/ref_combined_1.csv')

    def test_combined_2_1(self):
        '''
        test if the csv combiner correctly combines multiple input files;
        this test case: table2.csv + table1.csv (different order)
        '''
        input_list = ['./test_files/table_2.csv', './test_files/table_1.csv']
        self.combine_test_helper(input_list)
        assert self.file_cmp_helper(OUTPUT_FILE, './test_files/ref_combined_2.csv')

    def test_combined_1_2_3(self):
        '''
        test if the csv combiner correctly combines multiple input files;
        this test case: table1.csv + table2.csv + table3.csv (more than 2 files)
        '''
        input_list = \
            ['./test_files/table_1.csv', './test_files/table_2.csv', './test_files/table_3.csv']
        self.combine_test_helper(input_list)
        assert self.file_cmp_helper(OUTPUT_FILE, './test_files/ref_combined_3.csv')

    def test_combined_abc(self):
        '''
        test if the csv combiner correctly combines multiple input files;
        this test case: table_abc.csv + table_empty.csv (3 columns & empty table & no quotes)
        '''
        input_list = ['./test_files/table_abc.csv', './test_files/table_empty.csv']
        self.combine_test_helper(input_list)
        assert self.file_cmp_helper(OUTPUT_FILE, './test_files/ref_combined_abc.csv')


if __name__ == '__main__':
    unittest.main()

# CSV Combiner (Candidate Solution)

## Requirements

- Python 3.X There should be no need to install additional libraries and/or setting up virtual environments.

## Basics
- `csv_combiner.py` the CSV combiner; we use it by calling the script with command line arguments. There is also another way to use it as a module, for which the details are in the unit test file and below. The basic idea is to use a single CSV writer for the output file and loop through the input list by creating a reader for each input file. **Note our approach uses file handles instead of storing intermediate results in memory, so it is memory-efficient and can easily handle input size as large as 2GB. There are also exceptions for incorrectly formatted input, for which an error is thrown on command line to tell the user such errors and the output is corrupt. For example,**
  - Non-existent input file(s).
  - Empty input file (missing header).
  - Header & row mismatch.
- `csv_combiner_test.py` the provided unit test module. The test suite covers all helper functions of the combiner and considers different edge cases.

## Usage

To generate the combined CSV file out of `input_1.csv`, `input_2.csv`, ..., `input_n.csv`, and write the result to `output.csv`, run

    python input_1.csv input_2.csv ... input_n.csv > output.csv

For example, the provided output file `combined.csv` contains the result of running

    python csv_combiner.py ./fixtures/accessories.csv ./fixtures/clothing.csv > combined.csv

## Unit Tests

To run the entire test suite:

    python csv_combiner_test.py

To run a single test case, e.g. `test_append_content_empty`

    python csv_combiner_test.py CSVCombinerTests.test_append_content_empty

To use the combiner as a module in other modules, for example,

    import csv_combiner

    input_list = ['./test_files/table_1.csv', './test_files/table_2.csv']
    OUTPUT_FILE = './test_files/output.csv'

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as fh:
        writer = csv_combiner.get_csv_writer(fh)
        headers = csv_combiner.get_headers(input_list)
        csv_combiner.build_combined_csv(writer, headers, input_list)

---

*Begin original README*

# CSV Combiner

Write a command line program that takes several CSV files as arguments. Each CSV
file (found in the `fixtures` directory of this repo) will have the same
columns. Your script should output a new CSV file to `stdout` that contains the
rows from each of the inputs along with an additional column that has the
filename from which the row came (only the file's basename, not the entire path).
Use `filename` as the header for the additional column.

##  Considerations
* You should use coding best practices. Your code should be re-usable and extensible.
* Your code should be testable by a CI/CD process. 
* Unit tests should be included.

## Example
This example is provided as one of the ways your code should run. It should also be
able to handle more than two inputs, inputs with different columns, and very large (> 2GB) 
files gracefully.

```
$ ./csv-combiner.php ./fixtures/accessories.csv ./fixtures/clothing.csv > combined.csv
```

Given two input files named `clothing.csv` and `accessories.csv`.

|email_hash|category|
|----------|--------|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Shirts|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Pants|
|166ca9b3a59edaf774d107533fba2c70ed309516376ce2693e92c777dd971c4b|Cardigans|

|email_hash|category|
|----------|--------|
|176146e4ae48e70df2e628b45dccfd53405c73f951c003fb8c9c09b3207e7aab|Wallets|
|63d42170fa2d706101ab713de2313ad3f9a05aa0b1c875a56545cfd69f7101fe|Purses|

Your script would output

|email_hash|category|filename|
|----------|--------|--------|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Shirts|clothing.csv|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Pants|clothing.csv|
|166ca9b3a59edaf774d107533fba2c70ed309516376ce2693e92c777dd971c4b|Cardigans|clothing.csv|
|176146e4ae48e70df2e628b45dccfd53405c73f951c003fb8c9c09b3207e7aab|Wallets|accessories.csv|
|63d42170fa2d706101ab713de2313ad3f9a05aa0b1c875a56545cfd69f7101fe|Purses|accessories.csv|


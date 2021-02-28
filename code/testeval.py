import argparse
import csv
import sys

def extract_vals(f, is_int, column):
    valsreader = csv.reader(f, delimiter=',')
    vals = []
    _ = next(valsreader) # Skip header
    for row in valsreader:
        val = row[column]
        vals.append(int(val) if is_int else val) # Extract the logical time
    return vals

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-csvfile", help="CSV file to check", default="2test.txt")
    parser.add_argument("-expected", help="file to get expect vals from", required=True)
    args = parser.parse_args()
    csv_filename = args.csvfile
    expectation_filename = args.expected


    
    csv_file = open(csv_filename)
    real_vals = extract_vals(csv_file, True, 4)
    csv_file.seek(0)
    real_actions = extract_vals(csv_file, False, 0)
    csv_file.close()

    expectation_file = open(expectation_filename)
    _ = expectation_file.readline()
    expected_vals = [int(i) for i in expectation_file.readline().split(" ")]
    expected_actions = expectation_file.readline().split(" ")
    
    passed_test = expected_vals == real_vals and expected_actions == real_actions
    if passed_test:
        print("Test passed!")
    else:
        print(f"Test failed! Expected time vals: {expected_vals} but received time vals: {real_vals}")
        print(f"Expected actions: {expected_actions} but received actions: {real_actions}")
    sys.exit()
    

if __name__ == "__main__":
    main()
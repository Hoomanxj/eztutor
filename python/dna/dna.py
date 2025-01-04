import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    data_base = sys.argv[1]
    profile = sys.argv[2]

    # Read database file into a variable
    data_dict = read_data(data_base)

    # Read DNA sequence file into a variable
    dna = read_DNA(profile)

    # Find longest match of each STR in DNA sequence
    sub_seq_list_l = {'AGATC': "", 'TTTTTTCT': "", 'AATG': "", 'TCTAG': "",
                      'GATA': "", 'TATC': "", 'GAAA': "", 'TCTG': ""}

    sub_seq_list_s = {'AGATC': "", 'AATG': "", 'TATC': ""}

    if len(data_dict) == 3:
        sub_list = sub_seq_list_s
    else:
        sub_list = sub_seq_list_l

    for i in sub_list:
        sub_list[i] = longest_match(dna, i)

    # Check database for matching profiles
    for i in range(len(data_dict)):
        match = True
        for subseq in sub_list:
            if int(sub_list[subseq]) != int(data_dict[i][subseq]):
                match = False
                break
        if match:
            print(data_dict[i]['name'])
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        longest_run = max(longest_run, count)
    return longest_run


def read_data(file):
    with open(file, "r") as infile:
        reader = csv.DictReader(infile)
        data_dict = [row for row in reader]
        return data_dict


def read_DNA(file):
    with open(file, "r") as infile:
        dna = infile.read().strip()
    return dna


main()

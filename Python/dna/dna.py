import csv
import sys
# Check for valid input
if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py data.csv sequence.txt")
# Read DNA sequence file into a variable / f.read()
file = open(sys.argv[2], "r")
dna = file.read()
# Read database file into a variable / reader and dictreader
database = []
with open(sys.argv[1], "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        database.append(row)

# Define subsequence variables
subsequences = list(database[0].keys())[1:]


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run

    # Find longest match of each STR in DNA sequence
result = {}
for subsequence in subsequences:
    result[subsequence] = longest_match(dna, subsequence)


# TODO: Check database for matching profiles / int(x)
for person in database:
    match = 0
    for subsequence in subsequences:
        if int(person[subsequence]) == result[subsequence]:
            match += 1

    if match == len(subsequences):
        print(person["name"])
        exit()

print("No match")
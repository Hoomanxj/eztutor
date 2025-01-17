from shopping import month_to_int
import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        try:
            evidence = []
            labels = []
            for row in reader:
                evidence.append([
                        int(row[0]),
                        float(row[1]),
                        int(row[2]),
                        int(row[3]),
                        float(row[4]),
                        int(float(row[5])),
                        float(row[6]),
                        float(row[7]),
                        float(row[8]),
                        float(row[9]),
                        month_to_int(row[10]),
                        int(row[11]),
                        int(row[12]),
                        int(row[13]),
                        int(row[14]),
                        1 if row[15] == "returning" else 0,
                        1 if row[16] == True else 0
                    ])
                labels.append(
                    1 if row[-1] == True else 0
                )
            return (evidence, labels)
        except Exception as e:
            return e

evidence, labels = load_data(sys.argv[1])

print("Evidence:", evidence)
print("Label:", labels)
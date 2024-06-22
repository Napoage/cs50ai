import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


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
    months = {
        'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6
         , 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11 
         }
    evidence = []
    labels = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            administrative = int(row[0])
            administrative_Duration = float(row[1])
            informational = int(row[2])
            informational_Duration = float(row[3])
            productRelated = int(row[4])
            productRelated_Duration = float(row[5])
            bounceRates = float(row[6])
            exitRates = float(row[7])
            pageValues = float(row[8])
            specialDay = float(row[9])
            month = months[row[10]] #convert month to int 0 through 12
            operatingSystems = int(row[11])
            browser = int(row[12])
            region = int(row[13])
            trafficType = int(row[14])
            print(row[15],row[16],row[17])
            visitorType = 1 if row[15] == "Returning_Visitor" else 0 # convert vistortype to int -> , an integer 0 (not returning) or 1 (returning)
            weekend = 1 if row[16] == "TRUE" else 0 # convert weekend to int ->, an integer 0 (if false) or 1 (if true)
            #getting bool wrong
            label = 1 if row[17] == "TRUE" else 0
            print(visitorType, weekend, label)

            evidence_row = [
                administrative, administrative_Duration, informational, informational_Duration, productRelated, productRelated_Duration, 
                bounceRates, exitRates, pageValues,specialDay, month, operatingSystems, browser, region, trafficType, visitorType, weekend
            ]
            evidence.append(evidence_row)
            labels.append(label)
    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.

    The train_model function should accept a list of evidence and a list of labels, and return a scikit-learn nearest-neighbor classifier (a k-nearest-neighbor classifier where k = 1) fitted on that training data.
    Notice that we’ve already imported for you from sklearn.neighbors import KNeighborsClassifier. You’ll want to use a KNeighborsClassifier in this function.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0.0
    total_Positive = 0
    specificity = 0.0
    total_Negative = 0
    for label,prediction in zip(labels,predictions):
        if label == 1:
            total_Positive+=1 
            if prediction == 1:
                sensitivity+=1
        else:
            total_Negative+=1
            if prediction == 0:
                specificity+=1
    sensitivity = sensitivity/total_Positive if total_Positive>0 else 0
    specificity = specificity/total_Negative if total_Negative>0 else 0
            
    return sensitivity, specificity


if __name__ == "__main__":
    main()

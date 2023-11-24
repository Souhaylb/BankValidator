import pickle
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from services import storageService
from config import root_path
from util.common import indexOf, isNumber

modelPath = root_path + 'model/model.pkl'
dataTrainPath = root_path + 'data/bank-data-training.csv'
dataTestPath = root_path + 'data/bank-data-testing.csv'
dataTestedPath = root_path + 'data/bank-data-tested.csv'

model = None
unique_order = []
unique_field = {}
all_columns = {}

nbColumnRemove = 1
nbRowRemove = 1


def train():
    # Get all data of training file
    dataset = pd.read_csv(dataTrainPath)

    # Get unique data of dataset for get numeric value
    uniq_values = getListOfUniqueDataOrdered(dataset)
    print(uniq_values)

    # Save order user for the training
    storageService.saveTrainingDataOrder(uniq_values)
    storageService.saveTrainingDataField(getAllDataUnique(dataset))

    # Change all unique_values to numeric value
    array_keys = dataset.keys()
    storageService.saveTrainingDatacColumns(list(dataset.iloc[:, :-nbColumnRemove]))
    for column in array_keys:
        dataset[column] = dataset[column].apply(lambda x: indexOf(x, uniq_values))

    regressor = GaussianNB()

    X = dataset.iloc[:, :-nbColumnRemove]
    y = dataset.iloc[:, -nbRowRemove]
    # test avec 10% des données pour voir le reglage de l'algo
    regressor.fit(X, y)

    # Create file
    pickle.dump(regressor, open(modelPath, 'wb'))

    # Reload model for next use
    loadModel()


def loadModel():
    global model, unique_order, unique_field, all_columns
    try:
        model = pickle.load(open(modelPath, 'rb'))
        unique_order = storageService.getTrainingDataOrder()
        unique_field = storageService.getTrainingDataField()
        all_columns = storageService.getTrainingDataColumns()
    except IOError:
        print("Error loading model")


def getListOfUniqueDataByColumn(dataset):
    array_keys = dataset.keys()
    data_uniq = {}
    for x in array_keys:
        data_uniq[x] = set(dataset[x])
    return data_uniq


def getListOfUniqueDataOrdered(dataset):
    array_keys = dataset.keys()
    all_values = set()
    for x in array_keys:
        if not isNumber(dataset[x][0]):
            all_values.update(dataset[x])
    return list(all_values)


def getAllDataUnique(dataset):
    array_keys = dataset.keys()
    all_values = {}
    for column in array_keys:
        if not isNumber(dataset[column][0]):
            all_values[column] = list(set(dataset[column]))
    return all_values


def predict(datas):
    yes = indexOf("yes", unique_order)

    if yes == "yes":
            yes = 1

    no = indexOf("no", unique_order)

    if no == "no":
        no = 0

    value = (((model.predict([datas])[0] - no) * (1 - 0)) / (yes - no)) + 0
    return 1 >= value >= 0.5


def getDataAtLine(nb):
    dataset = pd.read_csv(dataTrainPath)
    dataset = dataset.iloc[:, :-nbColumnRemove]
    dataUse = []
    array_keys = dataset.keys()

    for column in array_keys:
        dataUse.append(indexOf(dataset[column][nb], unique_order))

    return dataUse


def testing():
    dataset = pd.read_csv(dataTestPath)
    dataUse = []
    datasetModified = dataset.copy()
    array_keys = dataset.keys()
    for column in array_keys:
        datasetModified[column] = dataset[column].apply(lambda x: indexOf(x, unique_order))
        rowNb = 0
        for row in datasetModified[column]:
            if len(dataUse) <= rowNb:
                dataUse.append([])
            dataUse[rowNb].append(row)
            rowNb += 1

    y_predicted = []
    for data in dataUse:
        response = "no"
        if predict(data):
            response = "yes"

        y_predicted.append(response)

    dataset["y"] = y_predicted
    dataset.to_csv(dataTestedPath, index=False)
    return y_predicted


loadModel()

if model is None:
    train()

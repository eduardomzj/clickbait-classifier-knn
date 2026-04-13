import math


def read_csv(file_name):
    fp = open(file_name)
    linhas = fp.readlines()
    linhas = linhas[1:]
    matrix = []
    for linha in linhas:
        row = list(map(float, linha.split(",")))
        matrix.append(row)
    return matrix


def euclidean_distance(point1, point2):
    elems = len(point1)
    som = 0
    for idx in range(elems):
        som += (point1[idx] - point2[idx]) ** 2
    return som ** 0.5


def get_neighbors(train_data, test_data, k):
    point_test = test_data[:-1]
    distances = []
    for line in train_data:
        point_train = line[:-1]
        d = euclidean_distance(point_test, point_train)
        distances.append(d)
    distance_pairs = [(d,i) for i, d in enumerate(distances)]
    ordered_distances = sorted(distance_pairs)
    indices = [i for (d, i) in ordered_distances]
    k_indice = indices[:k]
    return [train_data[k] for k in k_indice]


def predict_classification(neighbors):
    knn_labels = {}
    for neighbors in neighbors:
        label = neighbors[-1]
        if label in knn_labels:
            knn_labels[label] += 1
        else:
            knn_labels[label] = 1
    most_frequent_label = max(knn_labels.values())
    for key, value in knn_labels.items():
        if value == most_frequent_label:
            return key
    return -1


def knn_classifier(train_data, test_data, k):
    predictions = []
    for test_instance in test_data:
        neighbors = get_neighbors(train_data, test_instance, k)
        prediction = predict_classification(neighbors)
        predictions.append(prediction)
    return predictions



def accuracy(real, predicted):
    total_predictions = len(predicted)
    count = 0
    for i in range(total_predictions):
        if real[i] == predicted[i]:
            count += 1
    return count / total_predictions



test_data = read_csv("test.csv")
train_data = read_csv("train.csv")


actual = [line[-1] for line in test_data]
predictions = knn_classifier(train_data, test_data, k=5)

print("actual=", actual)
print("pred=", predictions)

acc = accuracy(actual, predictions)
print("Acurácia=", acc)





import random
import numpy as np

class Classifier:
    def __init__(self):
        self.training_data = None
        self.labels = None

    def train(self, instances, labels):
        self.training_data = instances
        self.labels = labels

    def test(self, instance):
        nearest_neighbor_distance = float('inf')
        nearest_neighbor_label = None

        for i in range(len(self.training_data)):
            distance_to_instance = np.linalg.norm(instance - self.training_data[i])
            if distance_to_instance < nearest_neighbor_distance:
                nearest_neighbor_distance = distance_to_instance
                nearest_neighbor_label = self.labels[i]

        return nearest_neighbor_label


def leave_one_out_cross_validation(data, current_set, feature_to_add):
    classifier = Classifier()
    instances = data[:, list(current_set) + [feature_to_add]]
    labels = data[:, 0]
    classifier.train(instances, labels)

    number_correctly_classified = 0

    for i in range(len(data)):
        object_to_classify = data[i, list(current_set) + [feature_to_add]]
        label_object_to_classify = data[i, 0]
        nearest_neighbor_distance = float('inf')
        nearest_neighbor_location = float('inf')

        for k in range(len(data)):
            if k != i:
                distance_to_instance = np.linalg.norm(object_to_classify - data[k, list(current_set) + [feature_to_add]])
                if distance_to_instance < nearest_neighbor_distance:
                    nearest_neighbor_distance = distance_to_instance
                    nearest_neighbor_location = k
                    nearest_neighbor_label = data[nearest_neighbor_location, 0]

        if label_object_to_classify == nearest_neighbor_label:
            number_correctly_classified += 1

    accuracy = number_correctly_classified / len(data)
    return accuracy



def greedy_search(num_feats, forwards, data):
    current_best = set()
    current_best_performance = -1
    print("\n\nBeginning Search\n")
    if not forwards:
        all_features = set(range(1, num_feats + 1))
        current_best = all_features.copy()
    for i in range(num_feats):
        best_performance = -1
        best_feature_choice = None
        if forwards:
            remaining_features = set(range(1, num_feats + 1)) - current_best
            for feature in remaining_features:
                temp_set = current_best.copy()
                temp_set.add(feature)
                temp_performance = leave_one_out_cross_validation(data, temp_set, feature)
                if temp_performance > best_performance:
                    best_performance = temp_performance
                    best_feature_choice = feature
                print(f"\tUsing feature(s): {temp_set} accuracy is: {temp_performance}%")
        else:
            curr_subset = current_best.copy()
            for feat in curr_subset:
                temp_set = curr_subset.copy()
                temp_set.remove(feat)
                temp_p = leave_one_out_cross_validation(data, temp_set, feat)
                if temp_p > best_performance:
                    best_performance = temp_p
                    current_best = temp_set
                print(f"\tUsing feature(s): {temp_set} accuracy is: {temp_p}")
        if best_performance > current_best_performance:
            current_best_performance = best_performance
            if best_feature_choice:
                current_best.add(best_feature_choice)
        else:
            print("\n(Warning! Accuracy has decreased!)")
            break
        print(f"\nFeature set {current_best} was best, accuracy is: {current_best_performance}%\n")
    print(f'The best feature subset is: {current_best} with accuracy of: {current_best_performance}%')
    return current_best, current_best_performance


def normalize_data(data):
    # Normalize each column (feature) of the data using min-max normalization
    for i in range(1, data.shape[1]):
        min_val = np.min(data[:, i])
        max_val = np.max(data[:, i])
        data[:, i] = (data[:, i] - min_val) / (max_val - min_val)
    return data


def main():
    print("Welcome to Eddie's Feature Selection Algorithm")
    file_path = "small-test-dataset.txt"
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        line = line.strip().split()
        data.append([float(val) for val in line])

    data = np.array(data)

    # Normalize the data
    data = normalize_data(data)

    amount_of_features = data.shape[1] - 1
    print("Type the number of the algorithm you want to run.\n1. Forward Selection\n2. Back Elimination")
    type_of_search = int(input(f"Choice:"))
    
    if type_of_search == 1:
        greedy_search(amount_of_features, True, data)
    else:
        greedy_search(amount_of_features, False, data)


if __name__ == '__main__':
    main()

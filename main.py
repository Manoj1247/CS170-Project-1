import numpy as np
import random
import matplotlib.pyplot as plt

small_dataset_path = "/Users/Vishal/cs170/CS170_Spring_2023_Small_data__9.txt"
large_dataset_path = "/Users/Vishal/cs170/CS170_Spring_2023_Large_data__9.txt"

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


class LeaveOneOutCrossValidator:
    def __init__(self, data, current_set, feature_to_add):
        self.data = data
        self.current_set = current_set
        self.feature_to_add = feature_to_add

    def validate(self):
        classifier = Classifier()
        instances = self.data[:, list(self.current_set) + [self.feature_to_add]]
        labels = self.data[:, 0]
        classifier.train(instances, labels)

        number_correctly_classified = 0

        for i in range(len(self.data)):
            object_to_classify = self.data[i, list(self.current_set) + [self.feature_to_add]]
            label_object_to_classify = self.data[i, 0]
            nearest_neighbor_distance = float('inf')
            nearest_neighbor_location = float('inf')

            for k in range(len(self.data)):
                if k != i:
                    distance_to_instance = np.linalg.norm(object_to_classify - self.data[k, list(self.current_set) + [self.feature_to_add]])
                    if distance_to_instance < nearest_neighbor_distance:
                        nearest_neighbor_distance = distance_to_instance
                        nearest_neighbor_location = k
                        nearest_neighbor_label = self.data[nearest_neighbor_location, 0]

            if label_object_to_classify == nearest_neighbor_label:
                number_correctly_classified += 1

        accuracy = number_correctly_classified / len(self.data)
        return accuracy


class GreedySearch:
    def __init__(self, num_feats, forwards, data):
        self.num_feats = num_feats
        self.forwards = forwards
        self.data = data

    def search(self):
        current_best = set()
        current_best_performance = -1
        print("\n\nBeginning Search\n")
        
        if not self.forwards:
            all_features = set(range(1, self.num_feats + 1))
            current_best = all_features.copy()

        accuracies = []
        k_values = []
        k = 0

        for i in range(self.num_feats):
            best_performance = -1
            best_feature_choice = None
            
            if self.forwards:
                remaining_features = set(range(1, self.num_feats + 1)) - current_best
                for feature in remaining_features:
                    temp_set = current_best.copy()
                    temp_set.add(feature)
                    temp_performance = LeaveOneOutCrossValidator(self.data, temp_set, feature).validate()
                    
                    if temp_performance > best_performance:
                        best_performance = temp_performance
                        best_feature_choice = feature

                    print(f"\tUsing feature(s): {temp_set} accuracy is: {temp_performance}%")
            else:
                curr_subset = current_best.copy()
                for feat in curr_subset:
                    temp_set = curr_subset.copy()
                    temp_set.remove(feat)
                    temp_p = LeaveOneOutCrossValidator(self.data, temp_set, feat).validate()
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

            k += 1
            accuracies.append(current_best_performance)
            k_values.append(k)
            
        print(f'The best feature subset is: {current_best} with accuracy of: {current_best_performance}%')

        # Accuracy vs increasing values of k
        plt.plot(k_values, accuracies)
        plt.xlabel('k')
        plt.ylabel('Accuracy')
        plt.title('Accuracy vs k')
        plt.show()

        return current_best, current_best_performance

class HillClimbing:
    def __init__(self, num_feats, data, max_attempts=10):
        self.num_feats = num_feats
        self.data = data
        self.max_attempts = max_attempts

    def search(self):
        current_best = set()
        current_best_performance = -1
        print("\n\nBeginning Search\n")

        attempts = 0
        while attempts < self.max_attempts:
            new_feature = random.randint(1, self.num_feats)

            if new_feature in current_best:
                current_best.remove(new_feature)
            else:
                current_best.add(new_feature)

            temp_performance = LeaveOneOutCrossValidator(self.data, current_best, new_feature).validate()
            print(f"\tUsing feature(s): {current_best} accuracy is: {temp_performance}%")

            if temp_performance > current_best_performance:
                current_best_performance = temp_performance
                attempts = 0
            else:
                print("\n(Warning! Accuracy has decreased!)")
                attempts += 1

        print(f'The best feature subset is: {current_best} with accuracy of: {current_best_performance}%')
        return current_best, current_best_performance

def normalize_data(data):
    for i in range(1, data.shape[1]):
        min_val = np.min(data[:, i])
        max_val = np.max(data[:, i])
        data[:, i] = (data[:, i] - min_val) / (max_val - min_val)
    return data


def main():
    print("Welcome to Eddie's Feature Selection Algorithm")
    small_dataset_path = "/Users/Vishal/cs170/CS170_Spring_2023_Small_data__9.txt"
    large_dataset_path = "/Users/Vishal/cs170/CS170_Spring_2023_Large_data__9.txt"

    # read small dataset
    with open(small_dataset_path, 'r') as file:
        lines = file.readlines()
    small_data = []
    for line in lines:
        line = line.strip().split()
        small_data.append([float(val) for val in line])
    small_data = np.array(small_data)
    small_data = normalize_data(small_data)
    num_feats_small = small_data.shape[1] - 1

    # read large dataset
    with open(large_dataset_path, 'r') as file:
        lines = file.readlines()
    large_data = []
    for line in lines:
        line = line.strip().split()
        large_data.append([float(val) for val in line])
    large_data = np.array(large_data)
    large_data = normalize_data(large_data)
    num_feats_large = large_data.shape[1] - 1

    # run greedy search on small dataset
    print("Running on small dataset...")
    print("Type the number of the algorithm you want to run.\n1. Forward Selection\n2. Back Elimination\n3. Hill Climbing")
    type_of_search = int(input(f"Choice:"))
    if type_of_search == 1:
        GreedySearch(num_feats_small, True, small_data).search()
    elif type_of_search == 2:
        GreedySearch(num_feats_small, False, small_data).search()
    else:
        HillClimbing(num_feats_small, small_data).search()

    # run greedy search on large dataset
    print("\nRunning on large dataset...")
    print("Type the number of the algorithm you want to run.\n1. Forward Selection\n2. Back Elimination\n3. Hill Climbing")
    type_of_search = int(input(f"Choice:"))
    if type_of_search == 1:
        GreedySearch(num_feats_large, True, large_data).search()
    elif type_of_search == 2:
        GreedySearch(num_feats_large, False, large_data).search()
    else:
        HillClimbing(num_feats_small, small_data).search()

if __name__ == '__main__':
    main()
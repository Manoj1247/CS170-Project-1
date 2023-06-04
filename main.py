import random


def greedy_search(num_feats, forwards):
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
                temp_performance = random_performance()
                if temp_performance > best_performance:
                    best_performance = temp_performance
                    best_feature_choice = feature
                print(f"\tUsing feature(s): {temp_set} accuracy is: {temp_performance}%")
        else:
            curr_subset = current_best.copy()
            for feat in curr_subset:
                temp_set = curr_subset.copy()
                temp_set.remove(feat)
                temp_p = random_performance()
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


def random_performance():
    return round(random.random() * 100, 1)


def loo_validation_function(combo):
    return combo


def main():
    print("Welcome to Eddie's Feature Selection Algorithm")
    amount_of_features = int(input("Please Enter total number of features:"))
    print("Type the number of the algorithm you want to run.\n1. Forward Selection\n2.Back Elimination")
    type_of_search = int(input(f"Choice:"))
    print(f"Using no features and \"random\" evaluation, I get an accuracy of {random_performance()}%")
    if type_of_search == 1:
        greedy_search(amount_of_features, True)
    else:
        greedy_search(amount_of_features, False)


if __name__ == '__main__':
    main()

import math
import copy
from collections import Counter

NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1),
             (0, -1), (0, 1),
             (1, -1), (1, 0), (1, 1)]


def is_valid_path(board, path, words):
    if check_path(path) == False:
        return None
    else:
        letters_list = []
        for i in range(len(path)):
            letters_list.append(board[path[i][0]][path[i][1]])
        word = "".join(letters_list)
        if word in words:
            return word
        else:
            return None


def find_length_n_paths(n, board, words):
    words = set(words)
    paths = []
    if n <= 0:
        return paths
    board_dict = dict()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] not in board_dict:
                board_dict[board[row][col]] = [(row, col)]
            else:
                board_dict[board[row][col]].append((row, col))
    temp_paths = []
    words_n_length = [word for word in words if len(word) >= n and len(word) <= 2 * n]
    final_paths = []
    for word in words_n_length:
        temp_paths = []
        temp_paths.extend(_helper_find_n_paths(n, board_dict, word))
        for path_to_check in temp_paths:
            if is_valid_path(board, path_to_check, [word]) is not None:
                final_paths.append(path_to_check)
    return final_paths


def _helper_find_n_paths(n, board_dict, word):
    if n <= 0:
        return [[]]
    all_paths = []
    if len(word) >= 1 and word[0] in board_dict:
        short_paths = _helper_find_n_paths(n - 1, board_dict, word[1:])
        for path in short_paths:
            for letter in board_dict[word[0]]:
                concatenated_path = [letter] + path
                all_paths.append(concatenated_path)

    if len(word) >= 2 and word[0:2] in board_dict:
        short_paths = _helper_find_n_paths(n - 1, board_dict, word[2:])
        for path in short_paths:
            for letter in board_dict[word[0:2]]:
                concatenated_path = [letter] + path
                all_paths.append(concatenated_path)

    return all_paths


def find_length_n_words(n, board, words):
    words = set(words)
    if n <= 0:
        return []
    final_list = []
    for i in range(math.ceil(n / 2) + 1):
        paths_1 = find_length_n_paths(n - i, board, words)
        temp_list1 = _find_length_n_words_helper(n, board, words, paths_1)
        final_list += temp_list1
    return final_list


def _find_length_n_words_helper(n, board, words, paths):
    letter_list = []
    words_paths = []
    for path in paths:
        for i in range(len(path)):
            letter_list.append(board[path[i][0]][path[i][1]])
        word = "".join(letter_list)
        if len(word) == n:
            words_paths.append(path)
        letter_list = []
    return words_paths


def max_score_paths(board, words):
    words_paths = []
    for i in range(1, 17):
        words_paths += find_length_n_paths(i, board, words)
    words_dict = {}
    for path in words_paths:
        if is_valid_path(board, path, words):
            word = is_valid_path(board, path, words)
            if word not in words_dict:
                words_dict[word] = path
            else:
                if len(words_dict[word]) < len(path):
                    words_dict[word] = path
    paths = words_dict.values()
    paths_list = list(paths)
    return paths_list


def check_path(path):
    for i in range(len(path)):
        if not (path[i][0] >= 0 and path[i][1] >= 0 and path[i][0] <= 3 and path[i][1] <= 3):
            return False
        for j in range(i + 1, len(path)):
            if path[i] == path[j]:
                return False
    if len(path) > 1:
        for i in range(len(path) - 1):
            if abs(int(path[i][0]) - int(path[i + 1][0])) > 1:
                return False
            if abs(int(path[i][1]) - int(path[i + 1][1])) > 1:
                return False
    return True

import requests
import logging
import string
import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict


def get_text(url):
    """Returns content of Url resource

    Args:
        url: URL String.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.text
    except requests.RequestException as e:
        logging.error(e)


def remove_punctuation(text):
    """Returns text cleaned from punctuation symbols
    
    Args:
        text: Content string
    """
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    """Maps words with its count unit
    
    Args:
        word: String.
    """
    return word, 1


def shuffle_function(mapped_values):
    """Combines words and their count units list
    
    Args:
        mapped_values: Tuple of word and its single count unit
    """
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    """Sums up count units of word
    
    Args:
        key_values: Dict items with word and its count units
    """
    key, values = key_values
    return key, sum(values)


def map_reduce(text):
    """Returns dict of words and their counts
    
    Args:
        text: Content string
    """
    text = remove_punctuation(text)
    words = text.split()

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def visualize_top_words(words_count):
    """Visualizes top 10 words by their count
    
    Args:
        words_count: Dict of words and their counts
    """
    top_words = dict(sorted(words_count.items(),
                     key=lambda x: x[1], reverse=True)[:10])
    fig, ax = plt.subplots()
    words = top_words.keys()
    y_pos = np.arange(len(words))
    counts = top_words.values()

    ax.barh(y_pos, counts, align='center')
    ax.set_yticks(y_pos, labels=words)
    ax.invert_yaxis()
    ax.set_xlabel('Frequency')
    ax.set_title('Top 10 Most Frequent Words')

    plt.show()


if __name__ == '__main__':
    logging.basicConfig(filename='logs.txt')
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        result = map_reduce(text)
        visualize_top_words(result)
    else:
        logging.error("Помилка: Не вдалося отримати вхідний текст.")
        print("Помилка: Не вдалося отримати вхідний текст.")

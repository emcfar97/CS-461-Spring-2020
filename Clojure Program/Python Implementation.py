from math import log2
from timeit import timeit
from  multiprocessing import Pool

def entropy(stream, threads):
    
    if threads == 1:

        frequency = map(lambda c: stream.count(c) / len(stream), set(stream))
        probability = map(lambda p: -p * log2(p), frequency)
        print(f'\t\tEntropy: {sum(probability)}')

    with Pool(threads) as p:

        frequency = p.map(stream.count, set(stream))
        frequency = [i / len(stream) for i in frequency]
        probability = p.map(log2, frequency)
        probability = [-p * pr for p, pr in zip(frequency, probability)]
        print(f'\t\tEntropy: {sum(probability)}')

def split_text(text, step):

    return [text[i:i + step] for i in range(0, len(text), step)]

def file():

    return open(
        'School\\4.Spring 2020\\Clojure Program\\WarAndPeace.txt',
        encoding='utf-8'
        ).read()

if __name__ == '__main__':

    for thread in range(7):

        print(f'{2 ** thread} threads')
        for step in range(1, 4): 

            print(f'\t{step} characters')
            for i in range(3):
                print('\t\t', timeit(
                    'entropy(split_text(file(), step), 2 ** thread)', 
                    "from __main__ import entropy, split_text, file, step, thread", 
                    number=1
                    ), " seconds")
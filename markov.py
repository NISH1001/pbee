import random
import re

from collections import defaultdict

import sys

def preprocess(text):
    text = re.sub(r'(["/])\s*', r' \1 ', text)
    return re.sub(r'\s+', ' ', text).strip()

class MarkovChain:
    def __init__(self, lookback=2):
        self.trie = defaultdict(lambda : defaultdict(int))
        self.lookback = lookback
        self.lines = []

    def train(self, lines):
        """
            Build markov model
        """
        self.lines += lines
        counter = 0
        for line in lines:
            tokens = line.split()[3:]
            tokens = preprocess(' '.join(tokens)).split()
            if not tokens:
                continue
            counter += 1
            if len(tokens) > self.lookback:
                for i in range(len(tokens) + 1):
                    a = ' '.join(tokens[max(0, i-self.lookback) : i])
                    b = ' '.join(tokens[i : i+1])
                    self.trie[a][b] += 1
        print("Total number of individual log :: {}".format(counter))
        self._build_probabilities()

    def _build_probabilities(self):
        """
            Calculate probabilities
        """
        for word, following in self.trie.items():
            total = float(sum(following.values()))
            for key in following:
                following[key] /= total

    def _sample(self, items):
        next_word = None
        t = 0.0
        for k, v in items:
            t += v
            if t and random.random() < v/t:
                next_word = k
        return next_word

    def generate(self, command):
        sentence = []
        next_word = command if command else self._sample(self.trie[''].items())
        while next_word:
            sentence.append(next_word)
            next_word = self._sample(self.trie[' '.join(sentence[-self.lookback:])].items())
        return sentence

def load_data(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line.strip())
    return lines


def main():
    data = load_data("data/log")
    mc = MarkovChain(lookback=5)
    mc.train(data)

    print(mc.trie['cd Nish / programming'])
    command = 'git push'
    command = 'cd Nish / stuff'
    completed = mc.generate(command)
    print(completed)


if __name__ == "__main__":
    main()



import numpy as np


class Brain:
    def __init__(self, input_size=7, hidden_size=8, output_size=2):
        # default: 5 sensor rays + velocity + angle = 7 inputs
        self.W1 = np.random.randn(input_size, hidden_size)
        self.W2 = np.random.randn(hidden_size, output_size)

    def forward(self, state):
        hidden = np.tanh(np.dot(state, self.W1))
        output = np.tanh(np.dot(hidden, self.W2))
        return output  # [throttle, steering]

    def mutate(self, rate=0.1):
        self.W1 += np.random.randn(*self.W1.shape) * rate
        self.W2 += np.random.randn(*self.W2.shape) * rate

    def copy(self):
        new = Brain()
        new.W1 = self.W1.copy()
        new.W2 = self.W2.copy()
        return new

    def save(self, path):
        np.savez(path, W1=self.W1, W2=self.W2)

    @staticmethod
    def load(path):
        data = np.load(path)
        b = Brain()
        b.W1 = data["W1"]
        b.W2 = data["W2"]
        return b

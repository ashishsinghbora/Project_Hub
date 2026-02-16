import numpy as np


class Brain:
    def __init__(self):
        # 7 inputs (5 sensors + velocity + angle) → 8 hidden → 2 outputs
        self.W1 = np.random.randn(7, 8)
        self.W2 = np.random.randn(8, 2)

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
        # save both weight matrices in a single .npz
        np.savez(path, W1=self.W1, W2=self.W2)

    @staticmethod
    def load(path):
        data = np.load(path)
        b = Brain()
        b.W1 = data["W1"]
        b.W2 = data["W2"]
        return b
import numpy as np

class Brain:
    def __init__(self, input_size=4, hidden_size=8, output_size=2):
        self.w1 = np.random.randn(input_size, hidden_size)
        self.w2 = np.random.randn(hidden_size, output_size)

    def forward(self, x):
        h = np.tanh(np.dot(x, self.w1))
        o = np.tanh(np.dot(h, self.w2))
        return o  # [accelerate, steer]

    def mutate(self, rate=0.1):
        self.w1 += np.random.randn(*self.w1.shape) * rate
        self.w2 += np.random.randn(*self.w2.shape) * rate

    def copy(self):
        new = Brain()
        new.w1 = self.w1.copy()
        new.w2 = self.w2.copy()
        return new

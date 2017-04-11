import numpy as np

class Network:
  def __init__(self, num_inputs, num_outputs, num_hidden, num_layers, learning_rate, should_create=True):
    self.num_inputs = num_inputs
    self.num_outputs = num_outputs
    self.num_hidden = num_hidden
    self.num_hidden_layers = num_layers
    self.learning_rate = learning_rate

    if should_create:
      self.layers = [
        np.random.normal(0.0, pow(self.num_hidden, -0.5), (self.num_hidden, self.num_inputs)),
      ]

      for i in range(self.num_hidden_layers - 1):
        self.layers.append(np.random.normal(0.0, pow(self.num_hidden, -0.5), (self.num_hidden, self.num_hidden)))

      self.layers.append(np.random.normal(0.0, pow(self.num_outputs, -0.5), (self.num_outputs, self.num_hidden)))

    self.layer_outputs = []
    self.games = []

  def activate(self, x):
    return 1 / (1 + np.exp(-x))

  def create_from_weights(self, weights):
    start = self.num_hidden * self.num_inputs
    self.layers = []
    self.layers.append(np.array(weights[:start]).reshape(self.num_hidden, self.num_inputs))

    for i in range(self.num_hidden_layers - 1):
      end = start + self.num_hidden * self.num_hidden
      self.layers.append(np.array(weights[start:end]).reshape(self.num_hidden, self.num_hidden))
      start = end

    self.layers.append(np.array(weights[start:]).reshape(self.num_outputs, self.num_hidden))

  def flatten_weights(self):
    weights = []
    for layer in self.layers:
      weights += sum(layer.tolist(), [])
    return weights

  def normalize_inputs(self, inputs):
    max_value = max(inputs)
    min_value = min(inputs)
    normalized_inputs = list(map(lambda x: (x - min_value) / (max_value - min_value), inputs))
    return normalized_inputs

  def query(self, inputs):
    self.layer_outputs = []
    self.layer_outputs = [np.array(self.normalize_inputs(inputs), ndmin=2).T]

    for layer in self.layers:
      self.layer_outputs.append(self.activate(np.dot(layer, self.layer_outputs[-1])))

    return self.layer_outputs[-1]

  def back(self, target):
    output_errors = [target - self.layer_outputs[-1]]
    for i in range(self.num_hidden_layers, -1, -1):
      output_errors.insert(0, np.dot(self.layers[i].T, output_errors[0]))

    for i in range(len(self.layers) - 1, -1, -1):
      errors = output_errors[-1]
      output_errors = output_errors[:-1]
      outputs = self.layer_outputs[-1]
      self.layer_outputs = self.layer_outputs[:-1]
      inputs = self.layer_outputs[-1]
      self.layers[i] += self.learning_rate * np.dot(errors * outputs * (1.0 - outputs), np.transpose(inputs))

    # output_errors = target - self.layer_outputs[num_outputs - 1]
    # self.who += self.learning_rate * np.dot(output_errors * self.layer_outputs[num_outputs - 1] * (1.0 - self.layer_outputs[num_outputs - 1]), np.transpose(self.layer_outputs[num_outputs - 2]))

    # output_errors = np.dot(self.who.T, output_errors)
    # for i in range(num_outputs - 2, 0, -1):
    #   self.whh[i - 1] += self.learning_rate * np.dot(output_errors * self.layer_outputs[i] * (1.0 - self.layer_outputs[i]), np.transpose(self.layer_outputs[i - 1]))
    #   if i != 1:
    #     output_errors = np.dot(self.whh[i - 1].T, output_errors)

    # output_errors = np.dot(self.wih.T, output_errors)
    # print(output_errors)
    # self.wih += self.learning_rate * np.dot(output_errors * self.layer_outputs[0] * (1.0 - self.layer_outputs[0]), np.transpose(self.input_values))

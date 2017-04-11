import numpy
import random
from collections import namedtuple
import math

Move = namedtuple('Move', 'move score')

def sigmoid(x):
  return 1 / (1 + numpy.exp(-x))

random.seed(1)

class Connection:
  identifier = 0
  def __init__(self, from_node, to_node, weight, enabled):
    # Connection.identifier += 1
    self.id = Connection.identifier
    self.from_node = from_node
    self.to_node = to_node
    self.weight = weight
    self.enabled = enabled

  def print_self(self):
    print(self.id, self.from_node, self.to_node, self.weight, self.enabled)

  def clone(self):
    return Connection(self.from_node, self.to_node, self.weight, self.enabled)

class Network:
  id = 0
  def __init__(self):
    # Network.id += 1
    self.id = Network.id
    self.network = []
    self.current_game = None
    self.node_identifier = 20
    self.outputs = {}

    # for i in range(17,21):
    #   for j in range(1,17):
    #     self.network.append(Connection(j, i, random.randint(-1, 1), True))

  def clone(self):
    new_network = Network()
    new_network.network = self.clone_connections()
    new_network.node_identifier = self.node_identifier
    return new_network
  
  def clone_connections(self):
    connections = []
    for connection in self.network:
      connections.append(connection.clone())
    return connections

  def enabled_connections(self):
    return [connection for connection in self.network if connection.enabled == True]

  def get_node_value(self, node_id, input):
    if (node_id in self.outputs):
      return self.outputs[node_id]

    highest_value = sorted(input, reverse=True)[0]
    connections = [connection for connection in self.network if connection.to_node == node_id]

    values = []
    for connection in connections:
      if (connection.enabled == True):
        if (connection.from_node <= 16):
          values.append(input[connection.from_node - 1] / highest_value * connection.weight)
        else:
          values.append(self.get_node_value(connection.from_node, input) * connection.weight)
    
    self.outputs[node_id] = sigmoid(sum(values))    
    return self.outputs[node_id]
  
  def get_output_values(self, input):
    up = Move('up', self.get_node_value(17, input))
    down = Move('down', self.get_node_value(18, input))
    left = Move('left', self.get_node_value(19, input))
    right = Move('right', self.get_node_value(20, input))

    self.outputs = {}

    return [up, down, left, right]

  def all_node_ids_in_network(self):
    ids = set()
    for connection in self.network:
      ids.add(connection.to_node)
      ids.add(connection.from_node)

    return ids

  def get_all_connections_for_node(self, node_id):
    return [connection for connection in self.enabled_connections() if connection.to_node == node_id or connection.from_node == node_id]

  # def get_nodes_after(self, node_id):
  #   result = []
  #   connections = [connection for connection in self.network if connection.enabled == True and connection.from_node == node_id]
  #   for connection in connections:
  #     result.append(connection.to_node)
  #     result += self.get_nodes_after(connection.to_node)
  #   return set(result)
    
  def get_nodes_before(self, node_id):
    result = []
    connections = [connection for connection in self.enabled_connections() if connection.to_node == node_id]
    for connection in connections:
      result.append(connection.from_node)
      result += self.get_nodes_before(connection.from_node)
    
    return set(result)
    

  def possible_new_connections(self, target_node_id):
    if target_node_id > 16 and target_node_id < 21:
      return []

    node_ids_in_node_path = [target_node_id]
    node_ids_in_node_path += self.get_nodes_before(target_node_id)
    node_ids_in_node_path += [connection.to_node for connection in self.get_all_connections_for_node(target_node_id) if connection.from_node == target_node_id]
    node_ids_in_node_path = set(node_ids_in_node_path)
    
    all_node_ids = self.all_node_ids_in_network()

    possible_node_connections = [node_id for node_id in all_node_ids if node_id not in node_ids_in_node_path and node_id > 16]

    return possible_node_connections

  def get_connection(self, from_node, to_node):
    connection = [connection for connection in self.network if connection.from_node == from_node and connection.to_node == to_node]
    if (len(connection) == 1):
      connection = connection[0]
    
    return connection
      

  def add_new_connection(self, from_node, to_node):
    # find if that connection already exists and is just disabled
    connection = self.get_connection(from_node, to_node)
    if connection:
      connection.enabled = True
    else:
      self.network.append(Connection(from_node, to_node, random.randint(-1, 1), True))

  def add_node_on_connection(self, connection):
    self.node_identifier += 1
    old_node = connection.to_node
    connection.to_node = self.node_identifier
    connection.weight = 1
    self.add_new_connection(self.node_identifier, old_node)

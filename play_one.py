import numpy as np
from matrix_network import Network
from game import Game
from collections import namedtuple
import operator
import json

np.random.seed(1)

networks_file = open('./networks.txt', 'r+')

Move = namedtuple('Move', 'move score')

print('Lets play!')

np.seterr(all='ignore')

def play_network(network):
  for i in range(10):
    game = Game()
    last_board = []
    network.games.append(game)
    network.highest_square = 0

    while game.game_over() == False:
      last_board = sum(game.board, [])
      original_moves = network.query(last_board)
      moves = sum(original_moves.tolist(), [])

      index, top_value = max(enumerate(moves), key=operator.itemgetter(1))
      if index == 0:
        game.up()
      elif index == 1:
        game.down()
      elif index == 2:
        game.left()
      elif index == 3:
        game.right()

      if sum(game.board, []) == last_board:
        target = np.copy(original_moves)
        target[index] = 0
        network.back(target)

      if game.highest_square() > 2048:
        print('it won')

    if game.highest_square() > network.highest_square:
      network.highest_square = game.highest_square()

  network.avg = sum(map(lambda x: x.highest_square(), network.games)) / len(network.games)
  return network

def create_networks():
  networks = []
  contents = networks_file.read()
  if contents:
    last_weights = json.loads(contents)
    print('Starting where we left off')
    for weights in last_weights:
      network = Network(16, 4, 32, 16, 0.2, False)
      network.create_from_weights(weights)
      networks.append(network)
  else:
    for i in range(100):
      networks.append(Network(16, 4, 32, 16, 0.2))

  return networks

def chunks(l, n):
  """Yield successive n-sized chunks from l."""
  for i in range(0, len(l), n):
      yield l[i:i + n]

def crossover(networks):
  sorted_networks = sorted(networks, key=lambda x: x.avg, reverse=True)
  best_network = sorted_networks[0]
  second_network = sorted_networks[1]

  new_networks = [best_network, second_network]

  first_weights = best_network.flatten_weights()
  second_weights = second_network.flatten_weights()

  for i in range(8):
    index = np.random.randint(0, 2623)
    new_weights = first_weights[:index] + second_weights[index:]

    network = Network(16, 4, 32, 16, 0.2, False)
    network.create_from_weights(new_weights)

    if np.random.random() <= 0.2:
      index = np.random.randint(1, len(network.layers) - 1)
      network.layers[index] = np.random.normal(0.0, pow(network.num_hidden_layers, -0.5), (network.num_hidden, network.num_hidden))

    new_networks.append(network)

  return new_networks

def main():
  networks = create_networks()
  highest_square = 0

  while highest_square < 2048:
    networks = map(play_network, networks)

    networks = sorted(networks, key=lambda x: x.highest_square)
    if networks[-1].highest_square > highest_square:
      highest_square = networks[-1].highest_square
      print('new high square', highest_square)

    print('generation average', sum(map(lambda x: x.avg, networks)) / len(networks))

    new_networks = []
    np.random.shuffle(networks)
    chunked_networks = chunks(networks, 10)
    for chunk in chunked_networks:
      new_networks += crossover(chunk)

    networks = new_networks

    networks_file.truncate()
    networks_file.write(json.dumps(map(lambda x: x.flatten_weights(), networks)))

main()

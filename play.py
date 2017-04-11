import random
import math
from network import Network
from game import Game

def find_new_connection_for_network(network):
  possible_nodes = [node_id for node_id in network.all_node_ids_in_network() if node_id < 17 or node_id > 20]
  random.shuffle(possible_nodes)

  target_node = 0
  possible_connections = []
  for node_id in possible_nodes:
    possible_connections = network.possible_new_connections(node_id)
    if len(possible_connections) > 0:
      target_node = node_id
      break

  if target_node == 0:
    return None

  return (target_node, random.choice(possible_connections))


def create_initial_networks():
  networks = []
  for i in range(100):
    network = Network()
    
    # (from_node, to_node) = find_new_connection_for_network(network)

    # network.add_new_connection(from_node, to_node)
    networks.append(network)
  
  return networks

def play_game(network):
  game = Game()
  network.current_game = game
  last_board = []

  while game.game_over() == False and last_board != sum(game.board, []):
    last_board = sum(game.board, [])
    moves = network.get_output_values(last_board)
    moves = sorted(moves, key=lambda move: move.score, reverse=True)
    top_move = moves[0].move
    if top_move == 'up':
      game.up()
    elif top_move == 'down':
      game.down()
    elif top_move == 'left':
      game.left()
    elif top_move == 'right':
      game.right()
  
  return game

def get_best_network(networks):
  return sorted(networks, key=lambda network: network.current_game.score, reverse=True)[:1][0]

def mutate_networks(networks):
  best_network = get_best_network(networks)
  new_networks = [best_network]
  for i in range(len(networks) - 1):
    new_network = best_network.clone()

    change = random.random()
    if change < .1:
      connection = find_new_connection_for_network(new_network)
      if connection == None:
        connection = random.choice(new_network.network)
        new_network.add_node_on_connection(connection)
      else:
        (from_node, to_node) = connection
        new_network.add_new_connection(from_node, to_node)
    elif change < .2:
      connection = random.choice(new_network.network)
      new_network.add_node_on_connection(connection)
    else:
      connection = random.choice(new_network.enabled_connections())
      connection.weight = random.random()
    
    new_networks.append(new_network)

  return new_networks

    
    
def chunks(l, n):
  """Yield successive n-sized chunks from l."""
  for i in range(0, len(l), n):
      yield l[i:i + n]  

def main():
  highest_square = 0
  networks = create_initial_networks()

  while highest_square < 2048:
    for network in networks:          
      play_game(network)

    best_network = get_best_network(networks)
    if (best_network.current_game.highest_square() > highest_square):
      best_network.current_game.print_board()
      print(best_network.current_game.highest_square(), best_network.current_game.score)
      highest_square = best_network.current_game.highest_square()

    chunked_networks = chunks(networks, 10)
    
    new_networks = []
    for chunk in chunked_networks:
      new_networks.append(mutate_networks(chunk))

    new_networks = sum(new_networks, [])
    random.shuffle(new_networks)
    networks = new_networks

  
  

main()
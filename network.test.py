from unittest import TestCase
from network import Network

# get_node_value
# get_output_value
#   all_node_ids_in_network
#   get_all_connections_for_node
#   get_nodes_before
#   possible_new_connections
#   get_connection
#   add_new_connection
#   add_node_on_connection

t = TestCase()


################################
# get_connection
################################
network = Network()

# can get a connection from node ids
connection = network.get_connection(network.network[0].from_node, network.network[0].to_node)
t.assertIs(connection, network.network[0])

# returns an empty list when the connection doesn't exist
connection = network.get_connection(100, 101)
t.assertEqual(len(connection), 0)

################################
# add_node_on_connection
################################
network = Network()

network.network[0].enabled = True
from_node = network.network[0].from_node
to_node = network.network[0].to_node
network.add_node_on_connection(network.network[0])

# Modifies the existing connection to point to the new neuron
connection = network.get_connection(from_node, network.node_identifier)
t.assertIs(connection, network.network[0])
t.assertIsNotNone(connection)
t.assertEqual(connection.weight, 1)

# creates a new connection from the new neuron to the old neuron
connection = network.get_connection(network.node_identifier, to_node)
t.assertIsNotNone(connection)


##################################
# add_new_connection
##################################
network = Network()

# enables a connection if one already exists
num_connections = len(network.network)
t.assertFalse(network.network[0].enabled)

network.add_new_connection(network.network[0].from_node, network.network[0].to_node)

t.assertTrue(network.network[0].enabled)
t.assertEqual(num_connections, len(network.network))

# creates a new connection if one does not already exist
network.node_identifier += 1
network.add_new_connection(network.node_identifier, 18)
connection = network.get_connection(network.node_identifier, 18)

t.assertEqual(connection.from_node, network.node_identifier)
t.assertEqual(connection.to_node, 18)
t.assertEqual(num_connections + 1, len(network.network))

###################################
# all_node_ids_in_network
###################################
network = Network()

for i in range(len(network.network)):
  connection = network.network[i]
  connection.enabled = True
  network.add_node_on_connection(connection)
  network.add_node_on_connection(connection)

node_ids = network.all_node_ids_in_network()
for i in range(1,network.node_identifier):
  t.assertIn(i, node_ids)



##################################
# get_all_connections_for_node
##################################
network = Network()

network.network[0].enabled = True
network.add_node_on_connection(network.network[0])

for i in range(17,21):
  network.add_new_connection(network.node_identifier, i)

for i in range(1, 17):
  network.add_new_connection(i, network.node_identifier)

connections = network.get_all_connections_for_node(network.node_identifier)
t.assertEqual(len(connections), 20)


###################################
# get_nodes_before
###################################
network = Network()

network.network[0].enabled = True

target_node = network.network[0].to_node

network.add_node_on_connection(network.network[0])
network.add_new_connection(2, network.node_identifier)

nodes = network.get_nodes_before(target_node)

t.assertIn(1, nodes)
t.assertIn(2, nodes)
t.assertIn(network.node_identifier, nodes)


#####################################
# possible_new_connections
#####################################
network = Network()

network.network[0].enabled = True

network.add_node_on_connection(network.network[0])
target_node = network.node_identifier

network.add_new_connection(2, target_node)
network.add_node_on_connection(network.network[len(network.network) - 1])

network.add_node_on_connection(network.network[0])

possible_connections = network.possible_new_connections(target_node)

t.assertEquals(len(possible_connections), 3)

for i in range(17, 21):
  t.assertIn(i, possible_connections)
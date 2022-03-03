from py2neo import Graph,Node,Relationship
neo_graph = Graph("http://localhost:7474",     username="neo4j",     password="neo4j")
test_node_1 = Node("Person",name = "test_node_1") # 注意：这里不要加“label=”，否则label会以属性的形式展示，而非标签
test_node_2 = Node("Person",name = "test_node_2")
neo_graph.create(test_node_1)
neo_graph.create(test_node_2)
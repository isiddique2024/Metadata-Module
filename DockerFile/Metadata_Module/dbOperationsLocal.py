from neo4j import GraphDatabase
from statusFeed import statusFeed

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "12345678")


# def create_digitalTwin(driver, nameOfNode, missionProfile, yearBuilt):
#     with driver.session() as session:
#         session.run(
#             """
#             CREATE 
#             (tempName:digitalTwin:Aircrafts {name: $name, missionProfile: $missionProfile, yearBuilt: $yearB}),
#             (f414:digitalTwin:jetEngine {name: 'General Electric F414', missionProfile: 'Jet Engine'})
#             CREATE (tempName)-[:HAS_ENGINE]->(f414)
#             """,
#             {
#                 "name": nameOfNode,
#                 "missionProfile": missionProfile,
#                 "yearB": yearBuilt
#             }
#         )


def add2nodesRelation(driver, node1,relation,node2):
    with driver.session() as session:
        session.run(
            f"""
            CREATE 
            (node1:digitalTwin:Aircrafts {{name: $nameofNode1}}),
            (node2:digitalTwin:jetEngine {{name: $nameofNode2}})
            
            CREATE (node1)-[:{relation}]->(node2)
            """,
            {
                "nameofNode1": node1,
                "nameofNode2": node2
            }
        )

        statusFeed.messageBuilder("123456","Metadata has been stored to Neo4j", "N/A")




# with GraphDatabase.driver(URI, auth=AUTH) as driver:
#     nameOfNode = input('What is the node name? : ')
#     missionProfile = input('What is the Mission Profile? : ')
#     yearBuilt = input('What is the year built? : ')
#     create_digitalTwin(driver,nameOfNode,missionProfile,yearBuilt)



nodes_relation = ["F18, ENGINE_OF, G414", "Boeing, ENGINE_OF, RR304"]

nodesArray = [nodes.split(",") for nodes in nodes_relation]

print(nodesArray)
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    for eachItem in nodesArray:
        #assign variable here 
        node1, relation, node2 = eachItem
        print(node1,relation,node2)
        add2nodesRelation(driver,node1,relation,node2)






# (f18lo:learnerObject:Aircrafts {name: 'F/A - 18 SuperHornet_LO'}), 
#             (f414:digitalTwin:jetEngine {name: 'General Electric F414', missionProfile: 'Jet engine'})


    # def checkIfNodeExists(node1,relation,node2):
    #       if node1 & node2 & relation exists:
    #             doNothing and return message "Nodes and Relations exists"
    #       elif node1 & node2 does not exist:
    #             createNodes_Relations(node1,relation,node2)
    #       elif node1 & node2 exists BUT relation doesNot exist
    #             addRelation(node1,relation,node2)
    #       elif node1 exists:
    #             addRelationAndOneNode(node2,relation)
    #       else node2 exists
    #             addRelationAndOneNode(node1,relation)

    #This function adds one New node and creates realtion with one other existing nodes
    # def addRelationAndOneNode(node,realtion):
    #     query statement for adding relation to one existing node and creating relationship
    #
    # This function adds new relation to two existing nodes             
    # def addRelation(node1, realtion, node2):
    #     query statement for adding relation to two existing node
    #  
    # This function creates two nodes and adds relations            
    # def createNodes_Relations(node1, relationParam, node2):
    #       querystatement for create
    #             """
    #             create(n1;Node1name,nodeType .... then node 2 n2:node2Name,nodeType)
    #             """
    #             
    #             create relation
    #             """
    #             n1 has relation:relationParam with n2
    #             
    #             """
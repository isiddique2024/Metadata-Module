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
def getAllNodes():
    with driver.session() as session:
        query = """MATCH (n) RETURN n LIMIT 100"""
        result = session.run(query)
        
        # Extract and print all nodes
        for record in result:
            node = record["n"]
            print(node)
   




def updateNodes():
    with driver.session() as session:
        print("Executing query to find node with name ' GE414'...")
        nodeToLookFor = input(f"Enter the name of the node to update: ")
        # Query to find the node
        query = """MATCH (tNode:digitalTwin {name: $nodeToLookFor}) RETURN tNode"""
        result = session.run(query, {"nodeToLookFor": nodeToLookFor})

        found_any = False

        for record in result:
            tNode = record["tNode"]
            print("Node found:", tNode)  # Debugging: Print the node details
            found_any = True
            
            # Ask user for the new name
            newName = input(f"Enter the new name for the node: ")

            # Update query using the internal ID of the node to ensure you're updating the correct node
            queryUpdate = """
            MATCH (tNode) 
            SET tNode.name = $newName
            RETURN tNode
            """

            # Run the update query with the node ID and new name as parameters
            resultNew = session.run(queryUpdate, {"newName": newName})
            
            # Print the updated node
            for updatedRecord in resultNew:
                updatedNode = updatedRecord["tNode"]
                print("Updated Node:", updatedNode)

        if not found_any:
            print("No nodes were found with the name ' GE414'.")




def add2nodesRelation(driver, node1,relation,node2):
    with driver.session() as session:
        query = f"""
            MERGE (node1:digitalTwin:Aircraft {{name: $nameofNode1}})
            MERGE (node2:digitalTwin:Engine {{name: $nameofNode2}})
            MERGE (node1)<-[:`has_{relation}`]-(node2)
            MERGE (node2)<-[:`{relation}_of`]-(node1)
        """ 
        session.run(query, {
            "nameofNode1": node1,
            "nameofNode2": node2
        })
        # session.run(
        #     f"""
        #     MERGE (node1:digitalTwin {{name: $nameofNode1}})
        #     MERGE (node2:digitalTwin {{name: $nameofNode2}})
        #     MERGE (node1)<-[:{{$relationHas}}]-(node2)
        #     MERGE (node2)<-[:{{relationOf}}]-(node1)
        #     """,
        #     {
        #         "nameofNode1": node1,
        #         "nameofNode2": node2,
        #         "relationHas": "has_" + relation,
        #         "relationOf": relation + "_of"
        #     }
        # )
        relString = node1 + " has the relationship of " + relation + " with " + node2
        statusFeed.messageBuilder("123456","Metadata has been stored to Neo4j: " + relString, "N/A")


#Node properties 
#digitalTwin
    #tmname:primaryNodeType(DT):SecondaryType(Aircraft,ship,etc): Properties MissionProfilemnam

#learnerObject
    #tname:primaryNodeType(LO):mediaType(pdf,img/jpeg,etc):fileLocation:contentID

# with GraphDatabase.driver(URI, auth=AUTH) as driver:
#     nameOfNode = input('What is the node name? : ')
#     missionProfile = input('What is the Mission Profile? : ')
#     yearBuilt = input('What is the year built? : ')
#     create_digitalTwin(driver,nameOfNode,missionProfile,yearBuilt)




# nodes_relation = ["F18, ENGINE_OF, G414", "Boeing, ENGINE_OF, RR304"]

def store_relationship():
    relationships = []  # array to store relationships

    # First object input from user
    nameofNode1 = input("Enter object: ")

    # Loop
    while True:
        # Input for the relationship and the next object
        relationship = input(f"Enter the relationship for '{nameofNode1}': ")
        nameofNode2 = input(f"Enter the next object: ")

        # Stores and formats inputted string into the relationships list
        relationship_string = f"{nameofNode1},{relationship},{nameofNode2}"
        relationships.append(relationship_string)

        # Prompts user to enter more objects or end input
        additional_input = input("Do you want to add another object? (yes or no): ").lower()

        # Ends process if the user says 'no more'
        if additional_input == 'no':
            break

        # Moves to next object in the loop
        nameofNode1 = nameofNode2

    # Output the relationships and nodes array
    # print("Relationships and nodes array:")
    # print(relationships)
    return relationships

# 




with GraphDatabase.driver(URI, auth=AUTH) as driver:
    updateNodes()
    # getAllNodes()
    # nodesArray = [nodes.split(",") for nodes in store_relationship()]

    # for eachItem in nodesArray:
    #     #assign variable here 
    #     node1, relation, node2 = eachItem
    #     print(node1)
    #     print(node2)

    #     add2nodesRelation(driver,node1,relation,node2)






# (f18lo:learnerObject:Aircrafts {name: 'F/A - 18 SuperHornet_LO'}), 
#             (f414:digitalTwin:jetEngine {name: 'General Electric F414', missionProfile: 'Jet engine'})


#    def checkIfNodeExists(node1,relation,node2):
#       if node1 & node2 & relation exists:
#             doNothing and return message "Nodes and Relations exists"
#       elif node1 & node2 does not exist:
#             createNodes_Relations(node1,relation,node2)
#       elif node1 & node2 exists BUT relation doesNot exist
#             addRelation(node1,relation,node2)
#       elif node1 exists:
#             addRelationAndOneNode(newNode,relation,existingNode)
#       else node2 exists
#             addRelationAndOneNode(newNode,relation,existingNode)


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
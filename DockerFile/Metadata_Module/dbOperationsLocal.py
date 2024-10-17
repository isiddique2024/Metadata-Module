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
   



def nodesRelation():
    with driver.session() as session:
 
        nodeToLookFor = input(f"Enter the name of the node to search: ")
        # Query to find the node
        query = """MATCH (tNode:digitalTwin {name: $nodeToLookFor}) RETURN tNode"""
        result = session.run(query, {"nodeToLookFor": nodeToLookFor})

        found_any = False

        for record in result:
            tNode = record["tNode"]
            print("Node found:", tNode)  # Debugging: Print the node details
            found_any = True
            
            # Create query for all relationships from this node 
      
            queryFindRelationFrom = """
            MATCH (tNode {name: $nodeName})-[r]->(connectedNode)
            RETURN tNode, type(r) AS relationshipType, connectedNode
            """

            # Run the update query with the node ID and new name as parameters
        resultNew = session.run(queryFindRelationFrom,  {"nodeName": nodeToLookFor})

        # Print the relationships
        for record in resultNew:
            tNode = record["tNode"]
            relationshipType = record["relationshipType"]
            connectedNode = record["connectedNode"]
            
            print(f"Node: {tNode['name']} -> [{relationshipType}] -> {connectedNode['name']}")

        if not found_any:
            print("No Relationships were found")

def nodeTraceback():
    with driver.session() as session:
        # Get the node name from user input
        nodeToLookFor = input("Enter the name of the node to search: ")
        
        # Query to find the node
        query = """MATCH (tNode:LO {name: $nodeToLookFor}) RETURN tNode"""
        result = session.run(query, {"nodeToLookFor": nodeToLookFor})

        found_any = False

        for record in result:
            tNode = record["tNode"]
            print("Node found:", tNode)  # Debugging: Print the node details
            found_any = True
            
            # Create query for all relationships from this node in a continuous path
            queryFindRelationFrom = """
            MATCH path = (LO:LO {name: $nodeToLookFor})-[*]->(endNode)
            RETURN LO, nodes(path) AS nodeChain, relationships(path) AS relationChain, length(path) AS pathLength
            ORDER BY length(path) DESC
            LIMIT 1
            """

            # Run the query to find the longest path from the found node
            resultNew = session.run(queryFindRelationFrom, {"nodeToLookFor": nodeToLookFor})

            # Track nodes to avoid repeats and ensure a single continuous path
            visited = set()

            # Print the relationships in a tree-like structure
            for record in resultNew:
                learnerObject = record["LO"]  # Extract the learner object
                nodeChain = record["nodeChain"]  # List of nodes along the path
                relationChain = record["relationChain"]  # List of relationships along the path
                
                # Print starting node
                tree_output = f"{learnerObject['name']}"
                
                # Loop through the path and print each node and its connecting relationship
                for i in range(len(relationChain)):
                    fromNode = nodeChain[i]
                    toNode = nodeChain[i + 1]
                    relationshipType = relationChain[i].type
                    
                    # Add to visited to prevent loops
                    if toNode.element_id not in visited:
                        tree_output += f" -> [{relationshipType}] -> {toNode['name']}"
                        visited.add(toNode.element_id)

                print(tree_output)
        
        if not found_any:
            print("No node found with the specified name.")



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


#"node1+DT,relation,node2+LO"
#Node properties 
#digitalTwin
    #tmname:primaryNodeType(DT):SecondaryType(Aircraft,ship,etc): Properties MissionProfile, name

def add2nodesRelation(driver, node1array,relation,node2array):

    if (len(node1array) >= 2):
        primaryType = node1array[1]
        secondaryType = node1array[2]
        missionProfile = node1array[3]

        primaryType2 = node2array[1]
        secondaryType2 = node2array[2]
        missionProfile2 = node2array[3]
        
        if (node2array[1] == "learnerObject"):
            learnerObject = node2array[1]
            mediaType = node2array[2]
            location = node2array[3]
            contentID = node2array[4]

    



    with driver.session() as session:
        query1 = f"""
            MERGE (node1:`{primaryType}`:`{secondaryType}` {{name: $nameofNode1, missionProfile: $missionProfile}})
            MERGE (node2:`{primaryType2}`:`{secondaryType2}` {{name: $nameofNode2, missionProfile: $missionProfile2}})
            MERGE (node1)<-[:`has_{relation}`]-(node2)
            MERGE (node2)<-[:`{relation}_of`]-(node1)
            """
        if (node2array[1] == "learnerObject"):
            query2 = f"""
                MERGE (node1:`{primaryType}`:`{secondaryType}` {{name: $nameofNode1, missionProfile: $missionProfile}})
                MERGE (node2:`{learnerObject}`:`{mediaType}` {{name: $nameofNode1, location: $location, contentID: $contentID}})
                MERGE (node1)<-[:`has_{relation}`]-(node2)
                MERGE (node2)<-[:`{relation}_of`]-(node1)
                """
        
        if(node2array[1] == "learnerObjct"):
            session.run(query2, {
                "nameofNode1": node1array[0],
                "nameofNode2": node2array[0],
                "missionProfile": missionProfile,
                "location": location,
                "contentID": contentID
            })
        else:         
            session.run(query1, {
                "nameofNode1": node1array[0],
                "nameofNode2": node2array[0],
                "missionProfile": missionProfile,
                "missionProfile2":missionProfile2
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
    #tmname:primaryNodeType(DT):SecondaryType(Aircraft,ship,etc): Properties MissionProfile, name

#learnerObject
    #tname:primaryNodeType(LO):mediaType(pdf,img/jpeg,etc):Properties fileLocation:contentID

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

    # updateNodes()
    # getAllNodes()
    # nodesArray = [nodes.split(",") for nodes in store_relationship()]

    # for eachItem in nodesArray:
    #     #assign variable here 
    #     node1, relation, node2 = eachItem
    #     #node1 = F22+DT+Aircraft
    #     node1array =  node1.split("+")
    #     node2array = node2.split("+")
    #     print(node1array)
    #     print(node2array)
    #     # print(node1)
    #     # print(node2)

    #     add2nodesRelation(driver,node1array,relation,node2array)
    # nodesRelation()
    nodeTraceback()



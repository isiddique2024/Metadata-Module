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

# def nodeTraceback():
#     with driver.session() as session:
#         # Get the node name from user input
#         nodeToLookFor = input("Enter the name of the node to search: ")
        
#         # Query to find the node
#         query = """MATCH (tNode:LO {name: $nodeToLookFor}) RETURN tNode"""
#         result = session.run(query, {"nodeToLookFor": nodeToLookFor})

#         found_any = False

#         for record in result:
#             tNode = record["tNode"]
#             print("Node found:", tNode)  # Debugging: Print the node details
#             found_any = True
            
#             # Start the traversal from the initial learner object node
#             current_node = tNode
#             tree_output = f"{current_node['name']}"
#             visited = set()
#             visited.add(current_node.element_id)

#             while current_node:
#                 # Query to find the first outgoing relationship from the current node
#                 queryFindNext = """
#                 MATCH (current:LO {name: $currentName})-[r]->(nextNode)
#                 RETURN current, r, nextNode LIMIT 1
#                 """
                
#                 resultNext = session.run(queryFindNext, {"currentName": current_node["name"]})
                
#                 found_next = False

#                 for nextRecord in resultNext:
#                     relationshipType = nextRecord["r"].type
#                     nextNode = nextRecord["nextNode"]

#                     # Check if the next node is already visited (to prevent loops)
#                     if nextNode.element_id in visited:
#                         current_node = None  # Stop traversal
#                         break

#                     # Add to the visited set and update the tree output
#                     tree_output += f" -> [{relationshipType}] -> {nextNode['name']}"
#                     visited.add(nextNode.element_id)
                    
#                     # Move to the next node and continue the traversal
#                     current_node = nextNode
#                     found_next = True
#                     break

#                 if not found_next:
#                     current_node = None  # End traversal if no more outgoing relationships

#             # Print the final tree output
#             print(tree_output)

#         if not found_any:
#             print("No node found with the specified name.")

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
            
            # Create query for all relationships from this node 
            queryFindRelationFrom = """
            MATCH path = (LO:LO {name: $nodeToLookFor})<-[*]-(endNode)
            RETURN LO, nodes(path) AS nodeChain, relationships(path) AS relationChain, length(path) AS pathLength
            """

            # Run the query to find the relationships from the found node
            resultNew = session.run(queryFindRelationFrom, {"nodeToLookFor": nodeToLookFor})


   
            for record in resultNew:
                learnerObject = record["LO"]  # Extract the learner object
                nodeChain = record["nodeChain"]  # List of nodes along the path
                relationChain = record["relationChain"]  # List of relationships along the path
                
                # Print starting node
                # print(f"Learner Object: {learnerObject['name']}")
                
                # Loop through the path and print each node and its connecting relationship
                for i in range(len(relationChain)):
                    relationshipType = relationChain[i].type  # Get the type of the relationship
                    fromNode = nodeChain[i]  # Get the current node
                    toNode = nodeChain[i + 1]  # Get the next node
                    
                print(f"{fromNode['name']} -> [{relationshipType}] -> {toNode['name']}")
        
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
def addLearnerRelation(node1array, relation, node2array):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        learnerObject = node1array[1]
        mediaType = node1array[2]
        location = "TEST"
        contentID = "TEST"

        primaryType2 = node2array[1]
        secondaryType2 = node2array[2]
        missionProfile2 = "TEST"

        with driver.session() as session:
            query = f"""
                MERGE (node1:`{learnerObject}`:`{mediaType}` {{name: $nameofNode1, location: $location, contentID: $contentID}})
                MERGE (node2:`{primaryType2}`:`{secondaryType2}` {{name: $nameofNode2, missionProfile: $missionProfile2}})
                MERGE (node1)<-[:`has_{relation}`]-(node2)
                MERGE (node2)<-[:`{relation}_of`]-(node1)
            """
            session.run(query, {
                "nameofNode1": node1array[0],
                "nameofNode2": node2array[0],
                "location": location,
                "contentID": contentID,
                "missionProfile2": missionProfile2
            })


def addDigitalTwinRelation(node1array, relation, node2array):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        primaryType1 = node1array[1]
        secondaryType1 = node1array[2]
        missionProfile1 = "TEST"

        primaryType2 = node2array[1]
        secondaryType2 = node2array[2]
        missionProfile2 = "TEST"

        with driver.session() as session:
            query = f"""
                MERGE (node1:`{primaryType1}`:`{secondaryType1}` {{name: $nameofNode1, missionProfile: $missionProfile1}})
                MERGE (node2:`{primaryType2}`:`{secondaryType2}` {{name: $nameofNode2, missionProfile: $missionProfile2}})
                MERGE (node1)<-[:`has_{relation}`]-(node2)
                MERGE (node2)<-[:`{relation}_of`]-(node1)
            """
            session.run(query, {
                "nameofNode1": node1array[0],
                "nameofNode2": node2array[0],
                "missionProfile1": missionProfile1,
                "missionProfile2": missionProfile2
            })

        statusFeed.messageBuilder("TEST","Metadata has been stored to Neo4j ", "Details")
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
        # relString = node1 + " has the relationship of " + relation + " with " + node2
        # statusFeed.messageBuilder("123456","Metadata has been stored to Neo4j: " + relString, "N/A")


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


class nodeBuilder:
    def packageParser(package):
        # with GraphDatabase.driver(URI, auth=AUTH) as driver:
            #node 0 is learner node 
            #index 1 is node 1 index 2 is relation index 3 is node 2 
            #  
            # updateNodes()
            # getAllNodes()
            # nodesArray = [nodes.split(",") for nodes in store_relationship()]
        node1array = package[0]
        # print(node1array)
        relation = package[1][0]
        # print(relation)
        node2array = package[2]
        # print(node2array)
        addLearnerRelation(node1array, relation, node2array)
        del package[0:2] 

       
 # Remove 3 elements since node1array, relation, node2array are used

        counter = 0
        size = len(package)

        # Run the loop as long as there are at least 3 elements in the package
        while size >= 3:
            # print(f"Counter: {counter}")
            counter += 2

            node1array = package[0]
            # print(node1array)
            relation = package[1][0]
            # print(relation)
            node2array = package[2]
            addDigitalTwinRelation(node1array, relation, node2array)
            del package[0:2]  # Remove 3 elements for consistency

            # Update size after modifying package
            size = len(package)

             
            
               
            

if __name__ == "__main__":
    package = [['docName', 'learnerObject', 'pdf'], ['learnerObject'], ['STFD650 steam turbines', 'digitalTwin', 'Engine'], ['engine'], ['USS Missouri', 'digitalTwin', 'Marine'], ['generator'], ['DG5000 generators,', 'digitalTwin', 'ElectricGenerator']]
    # package = [['docName', 'learnerObject', 'pdf'],['learnerObject'], ['FE718 engine', 'digitalTwin', 'Engine']]
    nodeBuilder.packageParser(package)
    # for eachItem in package:
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
    # nodeTraceback()

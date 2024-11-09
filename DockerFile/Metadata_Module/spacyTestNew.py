import traceback
import spacy
from spacy.tokens import Doc


# Register a custom attribute for inferred relations
if not Doc.has_extension("relations"):
    Doc.set_extension("relations", default=[])

# Define the relationship extraction component
class TypeBasedRelationExtractor:
    def __call__(self, doc):
        entities = {"digitalTwinAircraft": [], "digitalTwinEngine": [],"digitalTwinElectricGenerator": [], "digitalTwinGround": [], "digitalTwinMarine":[]}
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent)

        relations = []
        for aircraft in entities["digitalTwinAircraft"]:
            for engine in entities["digitalTwinEngine"]:
                # relations.append({"relation": "has_engine", "head": aircraft.text, "tail": f" {engine.text}"})
                relations.append({"relation": "engine"})
        for ground in entities["digitalTwinGround"]:
            for engine in entities["digitalTwinEngine"]:
                # relations.append({"relation": "has_engine", "head": ground.text, "tail": f" {engine.text}"})
                 relations.append({"relation": "Engine"})
        for marine in entities["digitalTwinMarine"]:
            for engine in entities["digitalTwinEngine"]:
                # relations.append({"relation": "has_engine", "head": ground.text, "tail": f" {engine.text}"})
                 relations.append({"relation": "Engine"})
        for m in entities["digitalTwinMarine"]:
            for engine in entities["digitalTwinElectricGenerator"]:
                # relations.append({"relation": "has_engine", "head": ground.text, "tail": f" {engine.text}"})
                 relations.append({"relation": "ElectricGenerator"})
          
        print("Relations:", relations)
        
        doc._.relations = relations
        return doc

# Register the custom component
@spacy.language.Language.factory("type_based_relation_extractor")
def create_type_based_relation_extractor(nlp, name):
    return TypeBasedRelationExtractor()

# Load the trained NER model and add the relationship extractor
nlp = spacy.load("/Users/mch/Documents/Metadata-Module/metadata-module/DockerFile/Metadata_Module/custom_ner_modelREL")
nlp.add_pipe("type_based_relation_extractor", last=True)


class entityRelationExtraction:
    def analyze(sentences):
        print("analyze() called from:")
        traceback.print_stack()  # This will show the call stack leading to analyze
        print(sentences)
        nodes = []

        learnerNode = ["Howto1.pdf", "learnerObject", "pdf"]
        learnerRelation = ["learnerObject"]


        # Define relationship map for node types
        relationship_map = {
            ("digitalTwinAircraft", "digitalTwinEngine"): "engine",
            ("digitalTwinEngine", "digitalTwinAircraft"): "engine",
            ("digitalTwinGround", "digitalTwinEngine"): "engine",
            ("digitalTwinEngine", "digitalTwinGround"): "engine",
            ("digitalTwinMarine", "digitalTwinEngine"): "engine",
            ("digitalTwinEngine", "digitalTwinMarine"): "engine",
            ("digitalTwinMarine", "digitalTwinElectricGenerator"): "generator",
             ("digitalTwinElectricGenerator", "digitalTwinMarine"): "generator",
            # Add more relationships as needed
        }

        for sentence in sentences:
            doc = nlp(sentence)
            
            for ent in doc.ents:
                print(f"Entity: {ent.text}, Label: {ent.label_}")
                nodeType = ent.label_[:11]
                digitalTwinType = ent.label_[11:]
                currentNode = [ent.text, nodeType, digitalTwinType]

                # Add current node to nodes list
                nodes.append(currentNode)

                # Check for relation after every two nodes
                if len(nodes) >= 2:
                    # Get previous node and current node for relationship check
                    prev_node = nodes[-2]
                    current_node = nodes[-1]

                    # Extract their types to check relationship
                    prev_type = prev_node[1] + prev_node[2]
                    curr_type = current_node[1] + current_node[2]
                    relationship = relationship_map.get((prev_type, curr_type))

                    if relationship:
                        # Add relationship node if found in the map
                        relation_node = [relationship]
                        nodes.insert(len(nodes) - 1, relation_node)

        print("Total Nodes:")
        print(nodes)
        
        # Remove duplicate nodes
        nodesUnique = remove_duplicate_nodes(nodes)
        print("Unique Nodes:")
        # Insert learnerNode and learnerRelation at the beginning of the nodes list
        nodesUnique.insert(0, learnerRelation)
        nodesUnique.insert(0, learnerNode)

        print(nodesUnique)
        
        
        # Parse the nodes with relationships
        nodeBuilder.packageParser(nodesUnique)


def remove_duplicate_nodes(nodes):
    unique_nodes = []
    for node in nodes:
        if node not in unique_nodes:
            unique_nodes.append(node)
    print("Unique Nodes")
    print(unique_nodes)
    return unique_nodes

if __name__ == "__main__":
    print("Running as main script")
    sentences = ["This is a test sentence."]
    entityRelationExtraction.analyze(sentences)
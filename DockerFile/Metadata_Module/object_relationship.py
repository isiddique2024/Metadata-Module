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
        relationship_string = f"{nameofNode1} > {relationship} < {nameofNode2}"
        relationships.append(relationship_string)

        # Prompts user to enter more objects or end input
        additional_input = input("Do you want to add another object? (yes or no more): ").lower()

        # Ends process if the user says 'no more'
        if additional_input == 'no more':
            break

        # Moves to next object in the loop
        nameofNode1 = nameofNode2

    # Output the relationships and nodes array
    print("Relationships and nodes array:")
    print(relationships)

# Function call
store_relationship()

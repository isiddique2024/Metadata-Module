# Metadata Module

## Setting up the environment

 **Create a virtual environment** (in the main project directory):

    ```bash
    python -m venv env
    ```

2. **Activate the virtual environment**:

   - On **Windows**:
     ```bash
     cd env
     cd Scripts
     ./activate
     ```

   - On **Mac/Linux**:
     ```bash
     source env/bin/activate
     ```

3. **Navigate back to the main project directory**:
   
    ```bash
    cd ..
    cd ..
    ```

4. **Install dependencies** in the local environment:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Docker Containers

Ensure **Docker Desktop** is running if you are on Windows.

1. **Start the Docker containers**:

    ```bash
    docker-compose up --build -d
    ```

## Running the Python Scripts

1. **Start listening on port 12345**:
   
    First, navigate to the directory where `parse.py` is located and run:

    ```bash
    python parse.py
    ```

2. **Send data to port 12345** (open a new terminal):

    Navigate to the directory where `main_server.py` is located and run:

    ```bash
    python main_server.py
    ```

## Additional Notes

- Ensure Docker is running before starting the containers.
- Use separate terminal windows to run `parse.py` and `main_server.py`.
- Make sure you are in the correct directories when running the Python scripts.

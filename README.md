# wobot_submission
This code is for a Todo List API that uses FastAPI, Pydantic, and PyMongo to handle user authentication and authorization for CRUD operations on a Todo list. The code is split into several files:

. `main.py`: This is the main file that defines the FastAPI application and its routes. It uses the functions from auth.py and database.py to handle authentication and connecting to the database, respectively. It also defines the endpoints for creating, reading, updating, and deleting Todos.

. `models.py`: This file defines the Todo Pydantic model, which is used as the input payload for creating and updating Todos.

. `database.py`: This file defines the get_database function, which connects to the MongoDB database and returns a reference to the todos collection.

. `credentials.py`: This file stores the credentials (username and password) for the users of the API.

. `auth.py`: This file defines the authenticate function, which authenticates a user based on their provided username and password. If the authentication is successful, the function returns an access token that is used for authorization in the other endpoints.


## How to Use
1. Clone the repository and navigate to the cloned directory.

2. Install the required dependencies by running the following command:

    `pip install -r requirements.txt`

4. Run the main.py file using the following command:

    `uvicorn main:app --reload`
    
    The API will be available at http://localhost:8000/docs

5. Use the /login endpoint to get the access token by passing the correct username and password as described in the credentials.py file.

6. Use the access token obtained from step 5 to access the protected endpoints such as /todos. Pass the access token in the X-Token header.

7. You can now perform CRUD operations on the todo tasks.

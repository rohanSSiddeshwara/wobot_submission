from pymongo import MongoClient

def get_database():
    # Connecting to the MongoDB database
    client = MongoClient("mongodb+srv://rohan:rohan123@cluster0.6l5kjql.mongodb.net/?retryWrites=true&w=majority")
    db = client["todolist"]
    todos = db["todos"]
    return todos

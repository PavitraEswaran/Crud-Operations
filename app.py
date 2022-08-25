
from logging import exception
from flask import Flask
from flask import jsonify,request
from flask_pymongo import pymongo

app = Flask(__name__)

cluster = pymongo.MongoClient("mongodb+srv://Pavitra26:Greenfish26@cluster0.venrqwl.mongodb.net")
db = cluster.get_database('DemoDB')
db_collection = pymongo.collection.Collection(db,'Students')
print("MongoDB connected Successfully")



@app.route("/students",methods = ['GET'])
def viewStudents():
    response = {}
    try:
        student_details = db_collection.find({})
        print(student_details)
        status = {
                "statusCode":"200",
                "statusMessage":"User Data Retrieved Successfully from the Database."
        }
        result = []
        for student in student_details:
            result.append({'name':student['name'],'year':student['year'],'dept':student['dept']})
        response['data'] = result
    except Exception as ex:
        print(ex)
        status = {
                "statusCode":"400",
                "statusMessage":str(ex)
        }
    response['status'] = status
    return response


@app.route("/register",methods = ['POST'])
def registration():
    response = {}
    try:
        req_body = request.json
        db_collection.insert_one(req_body)
        print("User Data Stored Successfully in the Database.")
        status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
        }
    except Exception as ex:
        print(ex)
        status = {
            "statusCode":"400",
            "statusMessage":str(ex)
        }
    response["status"] =status
    return response


@app.route("/update",methods = ['PUT'])
def updateStudents():
    response = {}
    try:
        req_body = request.json
        db_collection.update_many({'name':req_body['old_name']},
        {"$set":{"name":req_body['name']}})
        print("User Data Updated Successfully in the Database.")
        status = {
                "statusCode":"200",
                "statusMessage":"User Data Updated Successfully in the Database."
            }
    except Exception as ex:
        print(ex)
        status = {
            "statusCode":"400",
            "statusMessage":str(ex)
        }
    response["status"] =status
    return response   

@app.route("/delete",methods = ['DELETE'])
def deleteStudents():
    response = {}
    try:
        req_body = request.json
        db_collection.delete_many({"name":req_body['name']})
        status = {
            "statusCode":"200",
            "statusMessage":"User Data Deleted Successfully in the Database."
        }
    except Exception as ex:
        print(ex)
        status = {
            "statusCode":"400",
            "statusMessage":str(ex)
        }
    response["status"] =status
    return response


if __name__ == "__main__":
    app.run(host = "127.0.0.1:5000" ,debug = True)
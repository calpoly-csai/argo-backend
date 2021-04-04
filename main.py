import pymongo
from bson.objectid import ObjectId
from MidasModel import midas_find_depth
from flask import Flask
from flask import request
import os
from PIL import Image
import base64
import numpy as np
import requests
app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://csai-editor:csaieditor@argocluster.lyc0j.mongodb.net/argo_editor?retryWrites=true&w=majority")
db = client.argo_editor
col = db["argoTour"]

@app.route("/tour", methods=["GET"])
def getTours():
    """
    Get all Tour Info
    """
    docs = col.find({})
    tours = {}
    for i in docs:
        _id = str(i.pop("_id"))
        tours[_id] = i
    return tours

@app.route("/tour", methods=["POST"])
def updateTour():
    """
    Update Tour
    """
    tourinfo = request.get_json()
    print(tourinfo)
    if "_id" in tourinfo:
        query_tour = {"_id": ObjectId(tourinfo["_id"])}
        doc = col.find_one(query_tour)
        
        if doc == None:
            #col.insert_one(tourinfo)
            print("This Tour Doesn't Exist")
            return
        else:
            # TODO: Replace Nodes Here
            print("I found the tour!")
            pass
    
    else:
        _id = col.insert_one(tourinfo)
        return str(_id.inserted_id)


@app.route("/depth", methods=["GET"])
def findDepth():
    """
    Get Image URL and return depth map
    """
    image_url = request.get_data()

    encoded_string = base64.b64encode(requests.get(image_url).content)
    im_array = midas_find_depth(encoded_string.decode("utf-8"))
   
    # Test locally 
    #im = Image.fromarray(im_array)
    #im.save("yourfile.png")
    
    return {"data": im_array.tolist()}

if __name__ == "__main__":
    app.run()



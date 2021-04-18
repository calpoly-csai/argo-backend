import pymongo
from bson.objectid import ObjectId
from MidasModel import midas_find_depth
from flask import Flask
from flask import request
import base64
import requests
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask_cors import CORS
import mongomock
import argparse
import os
import json
app = Flask(__name__)
CORS(app)

parser = argparse.ArgumentParser(description='Argo Backend Server')
parser.add_argument('-l', "--l", "-local", dest='local', action='store_const', const=True, default=False, help='Indicates if the program should run in development mode')
args = parser.parse_args()
use_local_dev = args.local
mock_server_url = "mongomock://localhost"
production_server_url = "mongodb+srv://csai-editor:csaieditor@argocluster.lyc0j.mongodb.net/argo_editor?retryWrites=true&w=majority"
client = mongomock.MongoClient() if use_local_dev else pymongo.MongoClient(production_server_url)
db = client.argo_editor
col = db["argoTour"]
if use_local_dev:
    with open(os.path.join("src", "assets", "example-tour.json")) as f:
        example_tour = json.load(f)
        col.insert_one(example_tour)

cloudinary.config( 
  cloud_name = "csai", 
  api_key = "873262435531842",
  api_secret = "CCMU1kd4H25oia151RnemiqvKHk"
)

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
            print("This Tour Doesn't Exist")
            return "This Tour Doesn't Exist", 404
        else:
            print("I found the tour!")
            del tourinfo["_id"]
            col.replace_one(query_tour, tourinfo)
            return "Tour Updated", 200
    
    else:
        _id = col.insert_one(tourinfo)
        return str(_id.inserted_id)


@app.route("/depth", methods=["GET"])
def findDepth():
    """
    Get Image URL and return depth map
    """
    # TODO update this to fetch from cloudinary directly.
    image_url = request.get_data()

    encoded_string = base64.b64encode(requests.get(image_url).content)
    im_array = midas_find_depth(encoded_string.decode("utf-8"))
   
    # Test locally 
    #im = Image.fromarray(im_array)
    #im.save("yourfile.png")
    
    return {"data": im_array.tolist()}


@app.route("/upload-image", methods=["POST"])
def uploadImage():
    """
    Upload Image to Cloudinary
    """
    
    if("image" in request.files):
        image = request.files["image"]
    else:
        print("error")

    d = cloudinary.uploader.upload(image, 
    folder = "", 
    public_id = image.filename,
    overwrite = True, 
    resource_type = "image")

    return d['secure_url']


@app.route("/upload-resource", methods=["POST"])
def uploadResource():
    """
    Upload resource to Cloudinary
    """

    if ("image" in request.files):
        resource = request.files["image"]
        resource_type = "image"
    elif ("video" in request.files):
        resource = request.files["video"]
        resource_type = "video"
    elif ("raw" in request.files):
        resource = request.files["raw"]
        resource_type = "raw"
    else:
        print("error")
        return "error"
    
    d = cloudinary.uploader.upload(resource, 
        folder = "", 
        public_id = resource.filename,
        overwrite = True, 
        resource_type = resource_type)

    return d['secure_url']



if __name__ == "__main__":
    app.run()



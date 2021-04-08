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
app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://csai-editor:csaieditor@argocluster.lyc0j.mongodb.net/argo_editor?retryWrites=true&w=majority")
db = client.argo_editor
col = db["argoTour"]

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



if __name__ == "__main__":
    app.run()



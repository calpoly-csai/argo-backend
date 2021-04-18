# Argo Backend

Server-side logic of the Argo Project.

- Manages Argo tour graphs
- Runs computationally expensive tasks
- Mounts machine learning models for general use

The [Argo Editor](https://github.com/calpoly-csai/argo-editor-frontend) updates the data in the Argo Backend. Users interact with the tour graphs via the [Argo Tour](https://github.com/calpoly-csai/virtual-tour-concept).

## Getting Started:
(Note: It's probably a good idea to use a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)! This will make sure your dependencies don't clash with each other).
1. Clone the repo : `git clone https://github.com/calpoly-csai/argo-backend.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Start development server: `python ./src/main.py -l`
   - the `-l` option launches a mock development database, so any updates you make won't change real data. The mock database is stored in memory so closing your server erases the contents of the database. The starting template can be easily updated by changing the JSON in `src/assets/example-tour.json`.

## Resources

- [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/): Runs the REST API server.
- [TensorFlow](https://www.tensorflow.org/tutorials/quickstart/beginner): For writing machine learning models.
- [Cloudinary](https://cloudinary.com/documentation/image_upload_api_reference): A service that hosts our panoramic images and path videos.
- [MongoMock](https://github.com/mongomock/mongomock): Our development database that launches with the `-l` command line option.
- [PyMongo](https://pymongo.readthedocs.io/en/stable/tutorial.html): Database API that allows us to update persistent storage in Python functions.

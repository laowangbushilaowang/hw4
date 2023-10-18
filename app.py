from flask import Flask,request


# Imports Python standard library logging
import logging
# Imports the Cloud Logging client library
import google.cloud.logging

# Instantiates a client
client = google.cloud.logging.Client()

# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
client.setup_logging()

from google.cloud import storage

from google.cloud import pubsub_v1

app = Flask(__name__)
# [START functions_helloworld_get]
HTTP_METHODS = ['GET','PUT', 'POST', 'DELETE', 'HEAD', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
@app.route('/<path:url_path>/',methods=HTTP_METHODS)
# credentials = service_account.Credentials.from_service_account_file("C:/Users/85816/Desktop/cloud_c/wbh-project-398814-ba6f7af3bfda.json")
# storage_client = storage.Client(project="myproject", credentials=credentials)

def get_file(url_path):
    from flask import abort
    if request.method in ['PUT', 'POST', 'DELETE', 'HEAD', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']:
        logging.warning("501")
        return abort(501)

    client = pubsub_v1.PublisherClient()
    # Create a fully qualified identifier of form `projects/{project_id}/topics/{topic_id}`
    topic_path = client.topic_path("wbh-project-398814", "hello_topic")

    # Data sent to Cloud Pub/Sub must be a bytestring.
    try:
        data = request.headers['X-country']
        if data in ['North Korea', 'Iran', 'Cuba', 'Myanmar', 'Iraq', 'Libya', 'Sudan', 'Zimbabwe', 'Syria']:
            data="An access from {} was denied. ".format(data).encode()
            client.publish(topic_path, data)
            logging.warning("400")
            return abort(400)
    except:
        pass
    try:
        print(url_path)
        path = url_path.split("/", 1)
        storage_client = storage.Client()
        # BUCKET_NAME="bu-ds561-wbh-b1"
        
        BUCKET_NAME = path[0]
        file_name = path[1]
        print([BUCKET_NAME,file_name])
        # if not file_name:
        #     return "File name parameter is missing", 404

        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_name)

        content = blob.download_as_text()
        return content,200
    except Exception as e:
        logging.warning("404")
        return abort(404)
if __name__=='__main__':
    app.run(host='0.0.0.0')

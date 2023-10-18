from flask import Flask,request



from google.cloud import storage

from google.cloud import pubsub_v1

app = Flask(__name__)
# [START functions_helloworld_get]
@app.route('/<path:url_path>/')
# credentials = service_account.Credentials.from_service_account_file("C:/Users/85816/Desktop/cloud_c/wbh-project-398814-ba6f7af3bfda.json")
# storage_client = storage.Client(project="myproject", credentials=credentials)

def get_file(url_path):
    from flask import abort
    if request.method in ['PUT', 'POST', 'DELETE', 'HEAD', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']:
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
        return abort(404)
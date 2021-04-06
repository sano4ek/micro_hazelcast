import random
import uuid
import requests
from flask import Flask, request

app = Flask(__name__)

messenger_service_url = "http://0.0.0.0:8089/messenger"


def get_rand_logging_client():
    return random.choice(["http://0.0.0.0:8081/logging-service", "http://0.0.0.0:8082/logging-service", "http://0.0.0.0:8083/logging-service"])


@app.route('/facade-service', methods=['GET', 'POST'])
def facade_service():
    if request.method == 'POST':
        logging_service_response = requests.post(
            url=get_rand_logging_client(),
            json={
                "uuid": str(uuid.uuid4()),
                "message": request.json.get('message')
            }
        )
        status = logging_service_response.status_code
        return app.response_class(status=status)
    else:
        logging_service_response = requests.get(get_rand_logging_client())
        messages_service_r = requests.get(messenger_service_url)
        return str(logging_service_response.text) + ' : ' + str(messages_service_r.text)


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080, debug=True)

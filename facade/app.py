import random
import uuid
import pika
import requests
from flask import Flask, request

app = Flask(__name__)

messenger_service_url = (
    "http://0.0.0.0:1122/messages", "http://0.0.0.0:1123/messages"
)


def get_rand_logging_client():
    return random.choice(["http://0.0.0.0:8011/logging-service", "http://0.0.0.0:8012/logging-service", "http://0.0.0.0:8013/logging-service"])

def get_rand_messages_service_url() -> str:
    return random.choice(messenger_service_url)

@app.route('/facade-service', methods=['GET', 'POST'])
def facade_service():
    if request.method == 'POST':
        post_msg_to_mq(request.json.get('message'))
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
        messages_service_r = requests.get(get_rand_messages_service_url())
        return str(logging_service_response.text) + ' : ' + str(messages_service_r.text)

def post_msg_to_mq(msg: str):
    mq_connection = pika.BlockingConnection(
        pika.ConnectionParameters('127.0.0.1')
    )
    channel = mq_connection.channel()
    channel.queue_declare(queue='mq_for_messages_service')
    channel.basic_publish(
        exchange='', routing_key="mq_for_messages_service",
        body=msg,
    )
    print(f"[x] Sent: {msg}")
    mq_connection.close()


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=1345, debug=True)

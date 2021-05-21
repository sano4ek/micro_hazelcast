import hazelcast
from flask import Flask, request

app = Flask(__name__)


@app.route('/logging-service', methods=['GET', 'POST'])
def logger():
    if request.method == 'POST':
        print(f'\n --- post request from facade --- \n {request.json}\n')
        distributed_map = client.get_map('distr_map')
        distributed_map.set(str(request.json['uuid']), str(request.json['message']))
        print('--- SUCCESSFULLY SAVED ---')
        return app.response_class(status=200)
    else:
        distributed_map = client.get_map('distr_map')
        messages = distributed_map.values().result()
        print('\n --- get request from facade --- \n')
        return ','.join([msg for msg in messages]) or ''


if __name__ == '__main__':
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=["127.0.0.1:5703"]
    )
    app.run(host='0.0.0.0', port=8013, debug=True)

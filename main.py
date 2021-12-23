import json
import time
import requests
import random

app_file = '/home/ilya/BeamWork/SomeShitForNftGallery/randomoracle/build/wasi/shaders/app.wasm'
cid = '335a8471e06d986cb287065445d402f93e201a752ca161fd23bff4092279e9ec'
wallet_api_address = 'http://0.0.0.0:10011/api/wallet'


class GalleryRequest:
    def __init__(self, user_key, id):
        self.user_key = user_key
        self.id = id


def set_oracle_value(gallery_request_to_fulfill, value):
    requests.get(wallet_api_address,
                 data='{"jsonrpc":"2.0","id":"get_requests","method":"invoke_contract","params":'
                      + '{{"contract_file":"{app_file}","args":'.format(app_file=app_file)
                      + '"role=user,action=save_value,cid={cid},value={value},key={key},id={id}"}}}}'.format(
                     cid=cid,
                     value=value,
                     key=gallery_request_to_fulfill.user_key,
                     id=gallery_request_to_fulfill.id)
                 )


gallery_requests = dict()
while True:
    r = requests.get(wallet_api_address,
                     data='{"jsonrpc":"2.0","id":"get_requests","method":"invoke_contract","params":'
                          + '{{"contract_file":"{app_file}","args":'.format(app_file=app_file)
                          + '"role=user,action=get_oracle_requests,cid={cid}"}}}}'.format(cid=cid)
                     )

    b = '{' + r.json()['result']['output'] + '}'
    parsed_requests = json.loads(b)['values']
    for parsed_request in parsed_requests:
        gallery_request = GalleryRequest(user_key=parsed_request[0]['Value Info']['value.request_id.requester_key'],
                                         id=parsed_request[0]['Value Info']['value.request_id.id_in_requester'])
        if gallery_request not in gallery_requests:
            n = random.randint(0, 36893488147419103231)
            gallery_requests[gallery_request] = n
            set_oracle_value(gallery_request, n)

    time.sleep(5000)

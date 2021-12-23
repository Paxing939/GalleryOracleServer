import subprocess
import json
import time
import ast
import os
import requests

get_role = 'user'
get_action = 'get_requests'
cid = '19bda81c54f0e578cffe31b369067ff3f4581f96f6d4c43cc61d43fb8a8d49e2'
b = 'cd /home/ilya/'
base_command = 'cd "/home/ilya/Downloads/linux-beam-wallet-cli-masternet-6.1.11422 (1)/beam-wallet-masternet/";' \
               + f' ./beam-wallet-masternet shader --shader_app_file=app.wasm --shader_args="role={get_role},' \
               + f'action={get_action},cid={cid}" -n 127.0.0.1:10007'

# while True:
# s = ''
# s = subprocess.check_output(['ls'])
# # json.loads(s)
# print(s)

# process = subprocess.Popen(base_command.split(), shell=True, stdout=subprocess.PIPE)
# time.sleep(5)
# stdout = process.communicate()
# for s in stdout:
#     print('STDOUT:{}'.format(s))
# os.system(base_command)

# "contract_file":"/your contract/",

while True:
    r = requests.get('http://0.0.0.0:10000/api/wallet',
                     # data='{"jsonrpc":"2.0","id":"get_requests","method":"invoke_contract","params":'
                     #      + '{"contract_file":"/home/ilya/BeamWork/SomeShitForNftGallery/randomoracle/build/wasi/shaders/app.wasm","args":'
                     #      + '"role=user,action=get_oracle_requests,cid=335a8471e06d986cb287065445d402f93e201a752ca161fd23bff4092279e9ec"}}'
                     data='{"jsonrpc":"2.0","id":"view_contracts","method":"invoke_contract","params":{"contract_file":"/home/ilya/BeamWork/SomeShitForNftGallery/randomoracle/build/wasi/shaders/app.wasm","args":"role=manager,action=view_contracts"}}'
                     )

    # current_requests = json.loads(r.text())#['result']['output']['values']

    values = ast.literal_eval(json.loads(json.dumps(r.json()))['result']['output'].split(' ')[1][:-1])

    if len(values) != 0:
        for value in values:
            print(value)

    time.sleep(5000)

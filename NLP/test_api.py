import requests, time

conver = ['alo',
            'alo',
            'hà đông',
            'anh không biết nữa em ạ'
        ]
sender_id = eval(requests.get(url='http://localhost:5631/apis/init').content)['sender_id']
print (sender_id)      
for mess in conver:
    print ('Client: ', mess)
    data = {'sender_id': sender_id,
            'message': mess}
    res = eval(requests.post(url = 'http://localhost:5631/apis/conver', json=data).content)
    print ('Bot: ', res['text'])
    print ('--------------')
    # time.sleep(2)
import requests
import json

hostName = 'http://localhost:5001/'
r = requests.get('http://127.0.0.1:5001/chain')
print (r.text)

params = {
	"from": "abcde12345",
	"to": "12345abcde",
	"diseaseID": "0987654321123456",
	"docLink": "http://www.knsbnksdsdssn.com",
    "hash":"2112312"
}

r = requests.post(hostName+'submitRecord', data=json.dumps(params))
print(r.text)


params = {
	"from": "abcde12345",
	"to": "12345abcdeshdishd",
	"diseaseID": "0987654321123456",
	"docLink": "http://www.knsbnksdsdssn.com",
    "hash":"2112312"
}

r = requests.post(hostName+'submitRecord', data=json.dumps(params))
print(r.text)

params = {
	"from": "abcde12345",
	"to": "12345abcdefg",
	"diseaseID": "0987654321123456",
	"docLink": "http://www.knsbnksdssdsdsdssn.com",
    "hash":"2112312"
}

r = requests.post(hostName+'submitRecord', data=json.dumps(params))
print(r.text)

params = {
	"from": "abcde12345",
	"to": "12345abcdefghsh",
	"diseaseID": "0987654321123456",
	"docLink": "http://www.ksadwnsbnksdsdssn.com",
    "hash":"2112312"
}
r = requests.post(hostName+'submitRecord', data=json.dumps(params))
print(r.text)

r = requests.get(hostName+'mine')
print(r.text)


params = {
    "from": "12345abcdefghsh",
    "to": "abcde123456789",
    "hospitalId": "abcde12345",
    "diseaseId": "0987654321123456"
}

r = requests.post(hostName+'grantAccess', data=json.dumps(params))
print(r.text)

import requests

url = 'http://127.0.0.1:9000/predict'
payload ={
    'text' : 'hi i am onkar calling from pune or banglore',
    'language':'odia',
    'sample_rate':"16000", 
    'length':"0.9", 
    'speaker_name':'capri_speaker_meghana',
    'file_name':'test.wav', 
    'name':['onakr', 'pune', 'banglore']
}
resp = requests.post(url=url, json=payload)
print(resp)
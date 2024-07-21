import requests

url = 'https://www.4byte.directory/api/v1/signatures/?format=json&hex_signature=0x2cead560'
# url = 'https://www.4byte.directory/api/v1/signatures/?hex_signature=0x2cead560'

r = requests.get(url)
# r.encoding = 'utf-8'
# print(r.json()['text_signature'])

dict = r.json()

print(type(dict))
print(dict['results'][0]['text_signature'])
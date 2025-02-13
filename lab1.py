import json

#visa sita bloka uzsirasyti kaip stringa ir naudoti python kad ji konvertuoti i dictionary

x = '{"firstName": "Matas", "lastName": "Arlauskas", "age": "22", "city": "Vilnius"}'

y = json.loads(x)

print(y);
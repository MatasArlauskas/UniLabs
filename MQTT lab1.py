import json

x = '{"firstName": "Matas", "lastName": "Arlauskas", "age": "22", "city": "Vilnius"}'

y = json.loads(x)

print(y);

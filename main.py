import json

print(json.dumps({'a': 1, 'k': 4, 'b': 2}, sort_keys=True, indent=4))
# read a file
with open('resources/data/kataster.json', 'r') as katasterfile:
    data = katasterfile.read()

# parse the file
obj = json.loads(data);
print(json.dumps(obj['features'], indent=4))
print(type(obj))
print(json.dumps(obj['features'][0]['geometry'], indent=4))

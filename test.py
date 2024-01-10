import json

file_path = './archive/arxiv-metadata-oai-snapshot.json'

s = set()
with open(file_path, 'r') as file:
    for line in file:
        try:
            data = json.loads(line)
            s.add(data['categories'])
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

print(s)
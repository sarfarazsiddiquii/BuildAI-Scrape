import json

# Load the JSON data from the file
with open('urls.json', 'r') as file:
    data = json.load(file)

# Use a set to track unique links and a list to store the cleaned data
unique_links = set()
cleaned_data = []

for item in data:
    link = item['link']
    if link not in unique_links:
        unique_links.add(link)
        cleaned_data.append(item)

# Write the cleaned data back to the JSON file
with open('urls.json', 'w') as file:
    json.dump(cleaned_data, file, indent=4)

print(f"Removed duplicates. {len(cleaned_data)} unique links saved.")
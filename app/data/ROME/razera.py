import requests
import json

# Endpoint of the GraphQL server
url = 'https://rome4-api-dev-wyew76oo4a-ew.a.run.app/'

# Base query without pagination arguments
query = """
query AllSkillDomain($page: Int, $limit: Int) {
  allKnowHowDomain(page: $page, limit: $limit) {
    narrower {
      prefLabel {
        value
      }
    }
  }
}
"""

# Function to fetch data with pagination
def fetch_all_data(url, query, items_per_page):
    all_data = []
    page = 1
    total_fetched = 0

    while True:
        # Set the pagination variables as headers
        variables = {
            'page': page,
            'limit': 10,
        }
        
        response = requests.post(url, json={'query': query, "variables" : variables})

        if response.status_code == 200:
            data = response.json()
            all_data.extend(data['data']['allKnowHowDomain'])
            total_fetched += len(data['data']['allKnowHowDomain'])

            # Assuming we know there are ~1000 results, we stop if we have fetched them all
            if  len(data['data']['allKnowHowDomain']) < 10:
                break

            page += 1
        else:
            print("Query failed to run by returning code of {}. {}".format(response.text, query))
            break

    return all_data

# Call the function to fetch all data
complete_data = fetch_all_data(url, query, 100) # Adjust the number of items per page if needed
with open("app/data/ROME/knowHowDomains.json", 'w', encoding='utf-8') as json_file:
    json.dump(complete_data, json_file, indent=4, ensure_ascii=False)

# Print the total number of items fetched
print(f'Total items fetched: {len(complete_data)}')

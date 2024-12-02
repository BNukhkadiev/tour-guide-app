import os
from SPARQLWrapper import SPARQLWrapper, JSON


FILE_NAME = 'requests.sparql'

# Function to load queries from the file
def load_queries(file_name=FILE_NAME):
    # Dynamically construct the file path relative to the current script
    current_dir = os.path.dirname(__file__)  # Directory of the current script
    file_path = os.path.join(current_dir, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Queries file not found: {file_path}")

    # Read the queries from the file
    with open(file_path, "r") as f:
        content = f.read()

    queries = {}
    query_blocks = content.split("\n\n")  # Separate queries by empty lines
    for block in query_blocks:
        lines = block.strip().split("\n")
        query_name = lines[0].strip()
        query_body = "\n".join(lines[1:]).strip()
        queries[query_name] = query_body

    return queries


# Function to execute a query
def execute_query(query, location_name):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = query.replace("CITY_NAME", location_name)  # Replace placeholder with location name
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        print(f"Error executing query: {e}")
        return []

# Function to get city information
# def get_city_info(queries, location_name):
#     city_info_query = queries.get("CITY_INFO_QUERY")
#     city_info_results = execute_query(city_info_query, location_name)
#     city_info = []
#     for result in city_info_results:
#         city_info.append({
#             "city": result["city"]["value"],
#             "population": result["population"]["value"],
#             "area": result["area"]["value"]
#         })
#     return city_info

def get_city_info(queries, location_name):
    city_info_query = queries.get("CITY_INFO_QUERY")
    city_info_results = execute_query(city_info_query, location_name)
    city_info = []
    for result in city_info_results:
        city_info.append({
            "city": result["city"]["value"],
            "population": result["population"]["value"],
            "area": result["area"]["value"]
        })
    return city_info

# Function to get cultural sites
def get_cultural_sites(queries, location_name):
    cultural_sites_query = queries.get("CULTURAL_SITES_QUERY")
    cultural_sites_results = execute_query(cultural_sites_query, location_name)
    cultural_sites = []
    for result in cultural_sites_results:
        cultural_sites.append({
            "siteLabel_en": result.get("siteLabel_en", {}).get("value", "No description available"),
            "siteLabel_de": result.get("siteLabel_de", {}).get("value", "No description available"),
            "description_en": result.get("description_en", {}).get("value", "No description available"),
            "description_de": result.get("description_de", {}).get("value", "No description available"),
            "image": result.get("image", {}).get("value", "No image available")
        })
    return cultural_sites


queries = load_queries(FILE_NAME)
# print(get_cultural_sites(queries=queries, location_name='Aachen'))
print(get_city_info(queries=queries, location_name='Berlin'))



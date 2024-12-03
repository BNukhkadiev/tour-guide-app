from tour_guide import app
from flask import render_template, request
from kg_models.sparql_loader import load_queries, get_cultural_sites, get_city_info

# Load queries once when the app starts
queries = load_queries('requests.sparql')

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        city = request.form['city']  # Get the city name from the form

        # Pass both city info and attractions to the results page
        return render_template('results.html', city_info = get_city_info(queries, city), attractions = get_cultural_sites(queries, city),city=city)
    
    # Render the index page for GET requests
    return render_template('index.html')



# def get_tourist_attractions(city):
#     sparql = SPARQLWrapper("https://dbpedia.org/sparql")
#     query = f"""
#     SELECT ?attraction ?attractionLabel WHERE {{
#         ?attraction dbo:location dbr:{city} ;
#                     rdf:type dbo:TouristAttraction .
#         ?attraction rdfs:label ?attractionLabel .
#         FILTER (lang(?attractionLabel) = 'en')
#     }}
#     LIMIT 10
#     """
#     sparql.setQuery(query)
#     sparql.setReturnFormat(JSON)
#     results = sparql.query().convert()
#     attractions = [
#         result['attractionLabel']['value'] for result in results["results"]["bindings"]
#     ]
#     return attractions
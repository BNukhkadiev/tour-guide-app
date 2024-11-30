from tour_guide import app
from flask import render_template, request
from SPARQLWrapper import SPARQLWrapper, JSON


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        city = request.form['city']
        attractions = get_tourist_attractions(city)
        attractions = ['mall', 'joungsbusch', 'crack']
        return render_template('results.html', city=city, attractions=attractions)
    return render_template('index.html')



def get_tourist_attractions(city):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    query = f"""
    SELECT ?attraction ?attractionLabel WHERE {{
        ?attraction dbo:location dbr:{city} ;
                    rdf:type dbo:TouristAttraction .
        ?attraction rdfs:label ?attractionLabel .
        FILTER (lang(?attractionLabel) = 'en')
    }}
    LIMIT 10
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    attractions = [
        result['attractionLabel']['value'] for result in results["results"]["bindings"]
    ]
    return attractions
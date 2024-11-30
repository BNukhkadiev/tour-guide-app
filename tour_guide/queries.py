"""
"""




"""
SELECT ?museum ?label ?description WHERE {
  ?museum dbo:location dbr:Rome ;  # Replace "dbr:Rome" with your city of interest.
          rdf:type dbo:Museum ;
          rdfs:label ?label ;
          dbo:abstract ?description .
  FILTER (lang(?label) = "en" && lang(?description) = "en")
}
"""
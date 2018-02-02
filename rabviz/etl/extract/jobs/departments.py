import validators

query = """
	PREFIX rdfs:     <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX blocal:   <http://vivo.brown.edu/ontology/vivo-brown/>
	PREFIX foaf:     <http://xmlns.com/foaf/0.1/>
	SELECT DISTINCT ?dept ?name
	WHERE {
		?dept a foaf:Organization .
		?dept a blocal:BrownThing .
		?dept rdfs:label ?label .
		BIND(str(?label) as ?name) .
	}
"""

destination = "departments.csv"

def validate(rows):
	header = [ 'dept', 'name' ]
	validated = validators.validate_header(rows, header)
	validated = [ validators.validate_uri(row, 0) for row in validated ]
	validated = validators.validate_unique(validated, 0)
	return validated

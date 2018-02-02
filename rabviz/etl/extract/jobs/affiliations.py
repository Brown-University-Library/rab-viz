import validators

query = """
	PREFIX blocal:   <http://vivo.brown.edu/ontology/vivo-brown/>
	PREFIX vivo:     <http://vivoweb.org/ontology/core#>
	SELECT ?id ?dept ?rank
	WHERE {
		?id a vivo:FacultyMember .
		?id a blocal:BrownThing .
		?id vivo:personInPosition ?pos .
		?pos vivo:positionInOrganization ?dept .
		OPTIONAL {?pos vivo:rank ?rank .}
	}
"""

destination = "affiliations.csv"

def validate(rows):
    header = [ 'id', 'dept', 'rank' ]
    validated = validators.validate_header(rows, header)
    validated = [ validators.validate_shortid_uri(row, 0) for row in validated ]
    validated = [ validators.validate_rab_uri(row, 1) for row in validated ]
    return validated

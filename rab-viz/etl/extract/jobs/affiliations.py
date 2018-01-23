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
import validators

query = """
    PREFIX rdfs:     <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX blocal:   <http://vivo.brown.edu/ontology/vivo-brown/>
    PREFIX foaf:     <http://xmlns.com/foaf/0.1/>
    PREFIX vivo:     <http://vivoweb.org/ontology/core#>
    SELECT ?id ?last ?first ?label ?title ?org
    WHERE {
      ?id a vivo:FacultyMember .
      ?id a blocal:BrownThing .
      ?id foaf:lastName ?last .
      ?id foaf:firstName ?first .
      ?id rdfs:label ?label .
      ?id vivo:preferredTitle ?title .
      OPTIONAL {?id blocal:primaryOrgLabel ?org .}
    }
    """

destination = "faculty.csv"


def validate(rows):
    test_head = [ 'id', 'last', 'first', 'label', 'title', 'org' ]
    validated = validators.validate_header(rows, test_head)
    required_fields = [ test_head.index(i) for i in test_head[:-1] ]
    validated = [ validators.validate_required(row, required_fields)
                    for row in validated ]
    validated = [ validators.validate_shortid_uri(row, 0) for row in validated ]
    return validated

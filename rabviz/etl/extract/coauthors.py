from etl.validate import validate_data, validate_dataset

query = """
    PREFIX bcite:    <http://vivo.brown.edu/ontology/citation#>
    PREFIX blocal:   <http://vivo.brown.edu/ontology/vivo-brown/>
    PREFIX vivo:     <http://vivoweb.org/ontology/core#>
    SELECT ?fac1 ?fac2 ?cite
    WHERE {
        ?cite a bcite:Citation .
        ?cite bcite:hasContributor ?fac1 .
        ?cite bcite:hasContributor ?fac2 .
        ?fac1 a vivo:FacultyMember .
        ?fac1 a blocal:BrownThing .
        ?fac2 a vivo:FacultyMember .
        ?fac2 a blocal:BrownThing .
        FILTER (?fac1 != ?fac2)
    }
"""

destination = "coauthors.csv"

def validate(rows):
    header = [ 'fac1', 'fac2', 'cite' ]
    validated = validate_dataset.header(rows, header)
    validated = [ validate_data.shortid_uri(row, 0) for row in validated ]
    validated = [ validate_data.shortid_uri(row, 1) for row in validated ]
    validated = [ validate_data.rab_uri(row, 2) for row in validated ]
    validated = validate_dataset.column_equality(validated, 0, 1)
    return validated

from etl.validate import validate_data, validate_dataset

query = """
    PREFIX vivo:     <http://vivoweb.org/ontology/core#>
    SELECT ?faculty ?collaborator
    WHERE
    {
          ?faculty vivo:hasCollaborator ?collaborator. 
          ?faculty a vivo:FacultyMember .
          ?faculty a blocal:BrownThing .
          ?collaborator a vivo:FacultyMember .
          ?collaborator a blocal:BrownThing .
    }
    """

destination = "collaborators.csv"


def validate(rows):
    test_head = [ 'faculty', 'collaborator' ]
    validated = validate_dataset.header(rows, test_head)
    validated = [ validate_data.shortid_uri(row, 0) for row in validated ]
    validated = [ validate_data.shortid_uri(row, 1) for row in validated ]
    return validated

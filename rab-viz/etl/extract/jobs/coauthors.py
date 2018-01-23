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

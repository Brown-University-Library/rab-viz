from app import app
from .models import ChordDeptViz

@app.route('/')
@app.route('/index')
def index():
	viz = ChordDeptViz.query.filter_by(deptid="http://vivo.brown.edu/individual/org-brown-univ-dept84").first()
	return viz.facultydata
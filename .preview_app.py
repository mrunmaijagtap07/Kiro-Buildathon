import os
from flask import Flask
from jinja2 import Environment, FileSystemLoader

PROJ = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(os.path.join(PROJ, "templates")))

def url_for(endpoint, **values):
    if endpoint == "static":
        return "/static/" + values.get("filename", "")
    return "#"

class Args(dict):
    def get(self, k, d=None): return super().get(k, d)

class Req:
    endpoint = "main.home"
    args = Args()

def get_flashed_messages(*a, **k): return []

env.globals.update(url_for=url_for, request=Req(), session={}, get_flashed_messages=get_flashed_messages)

stats = {"approved_projects": 1248, "departments": 14, "tag_count": 67, "faculty_count": 142}
def mk(title, dept, year, guide, tags):
    return {"project_id": 1, "title": title, "dept_name": dept, "academic_year": year,
            "guide_name": guide, "tags": [{"tag_name": t} for t in tags]}
recent = [
    mk("Crop Disease Detection Using Deep Learning", "Information Technology", 2026, "Dr. A. Sharma", ["Python","TensorFlow","OpenCV"]),
    mk("Smart Campus Monitoring System", "Electronics", 2026, "Dr. P. Mehta", ["Arduino","IoT","MySQL"]),
    mk("Online Examination System", "Computer Science", 2026, "Dr. R. Nair", ["Flask","MySQL","JavaScript"]),
    mk("Student Performance Analytics Dashboard", "Information Technology", 2026, "Dr. S. Rao", ["Python","Pandas","Power BI"]),
]

app = Flask(__name__, static_folder=os.path.join(PROJ, "static"), static_url_path="/static")

@app.route("/")
def home():
    return env.get_template("home.html").render(stats=stats, recent_projects=recent)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5055)

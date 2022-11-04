from flask import Flask, render_template, request, redirect, send_file
from extractors.saramin import extract_saramin_jobs
from extractors.jobkorea import extract_jobkorea_jobs
from extractors.file import save_to_file

app = Flask("JobScrapper")

@app.route("/")
def home():
    return render_template("home.html", name="bibi")

db = {}

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db :
        jobs = db[keyword]
    else:
        saramin = extract_saramin_jobs(keyword)
        jobkorea = extract_jobkorea_jobs(keyword)
        jobs = saramin + jobkorea
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword not in db :
    return redirect(f"/search?keyword={keyword}")
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv", as_attachment=True)


app.run("0.0.0.0")
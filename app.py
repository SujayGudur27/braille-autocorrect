from flask import Flask, request, render_template_string
from sujay_gudur_braille_autocorrect import autocorrect_system  # Make sure your script is importable

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Braille Autocorrect</title>
<h2>Braille QWERTY Input</h2>
<form method=post>
  <textarea name=input rows=4 cols=50 placeholder="Enter QWERTY braille like: qw,do,kp,kp,od odk,od,k,kp,dp"></textarea><br>
  <input type=submit value=Convert>
</form>
{% if result %}
<h3>Output:</h3>
<p><b>{{ result }}</b></p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        qwerty_input = request.form["input"]
        result = autocorrect_system(qwerty_input)
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(debug=True)

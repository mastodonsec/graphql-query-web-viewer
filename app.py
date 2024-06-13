from flask import Flask, render_template
import requests
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': 'Bearer YOUR_GITHUB_TOKEN'}
    query = """
    query {
      repository(owner: "im-sandbox-tamb", name: "ghas-copilot-labs") {
        vulnerabilityAlerts(first: 100) {
          nodes {
            securityVulnerability {
              severity
            }
          }
        }
      }
    }
    """
    response = requests.post(url, headers=headers, json={'query': query})
    data = response.json()

    # Count the number of alerts for each severity level
    counts = {}
    for alert in data['data']['repository']['vulnerabilityAlerts']['nodes']:
        severity = alert['securityVulnerability']['severity']
        if severity not in counts:
            counts[severity] = 0
        counts[severity] += 1

    # Create a bar chart with Plotly
    data = [go.Bar(x=list(counts.keys()), y=list(counts.values()))]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
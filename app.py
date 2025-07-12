
#comment
from flask import Flask, render_template
import requests
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://api.github.com/graphql'
    bearer_token = os.environ['BEARER_TOKEN'] #setup your bearer token as an environment variable
    headers =  {'Authorization': f'Bearer {bearer_token}'}
    query = """
    #Replace ORG_NAME and REPO_NAME with your organization and repository you want to run the query against it.
    query {
      repository(owner: "ORG_NAME", name: "REPO_NAME") { 
        vulnerabilityAlerts(first: 100) {
          nodes {
            securityVulnerability {
                package {
                    name
                }
              severity
              advisory {
                description
                identifiers {
                    type
                    value
                }   
              }
            }
          }
        }
      }
    }
    """
    response = requests.post(url, headers=headers, json={'query': query})
    data = response.json()
    print(data) # for debugging purposes
    print(response.status_code) # for debugging purposes

    # Count the number of alerts for each severity level
    counts = {}
    for alert in data['data']['repository']['vulnerabilityAlerts']['nodes']:
        severity = alert['securityVulnerability']['severity']
        if severity not in counts:
            counts[severity] = 0
        counts[severity] += 1

    # Create a bar chart with Plotly with x as the severity levels and y as the counts
    data = [go.Bar(x=list(counts.keys()), y=list(counts.values()))]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)

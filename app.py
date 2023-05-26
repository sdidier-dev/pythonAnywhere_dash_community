from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import git
from flask import request

app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server

@server.route('/git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./app')
    origin = repo.remotes.origin
    repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200

data = {
    'x': ['Cat', 'Dog'] * 9,
    'y': [1, 2, 3, 4, 5, 6, 9, 8, 7, 6, 5, 4, 5, 5, 5, 5, 5, 5],
    'color': [*["increase"] * 6, *["decrease"] * 6, *["unchanged"] * 6],
    'facet_col': [*["10 minutes"] * 2, *["30 minutes"] * 2, *["60 minutes"] * 2] * 3,
}

fig = px.bar(data, x="x", y="y", color="color", facet_col="facet_col")

# little customisations
fig.for_each_annotation(lambda a: a.update(text=''))# remove the facet titles
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
fig.update_yaxes(title_text="", ticks="outside", linecolor="black", row=1, col=1)

# To modify the gaps between subplots, you can modify the domain of their xaxis
def domains_calculator(gap, n_plot):
    """
    little helper to calculate the range of subplots domains
    """
    plot_width = (1 - (n_plot-1) * gap) / n_plot
    return [
        [i * (plot_width + gap), i * (plot_width + gap) + plot_width]
        for i in range(n_plot)
    ]

domains = domains_calculator(gap=0.05, n_plot=3)

fig.update_xaxes(title_text="10 minutes", domain=domains[0], row=1, col=1)
fig.update_xaxes(title_text="30 minutes", domain=domains[1], row=1, col=2)
fig.update_xaxes(title_text="60 minutes", domain=domains[2], row=1, col=3)

# and to modify the gap between the subplots bars, you can modify their width
fig.update_traces(width=1)

app.layout = html.Div(
    [
        dcc.Graph(id="graph-scatergl", figure=fig),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
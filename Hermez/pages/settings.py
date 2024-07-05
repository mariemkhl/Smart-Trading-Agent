import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from wordcloud import WordCloud
import base64
from io import BytesIO
import random

# Finance-focused sample text
default_text = """
Stocks, trading, market watch, investment, portfolio, dividends, bear market, bull market, 
exchange, Wall Street, TUNINDEX20, Tunisia, TUNINDEX, buy low, sell high, trading volume, 
liquidity, bonds, commodities, cryptocurrency, risk management, financial planning, 
capital gains, market trends, indices, futures, options, hedge funds, asset allocation
"""

# Function to generate word cloud image
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    image = wordcloud.to_image()
    with BytesIO() as buffer:
        image.save(buffer, 'png')
        return base64.b64encode(buffer.getvalue()).decode()

# Hugging Face image path (assuming it's in the assets folder)
hugging_face_logo = 'assets/hugging_face.png'

def settings_layout(text=default_text):
    img = generate_wordcloud(text)
    img_src = "data:image/png;base64,{}".format(img)
    return html.Div([
        html.H1("Finance Word Cloud Visualization"),
        html.Img(src=app.get_asset_url(hugging_face_logo), style={'width': '100px', 'height': 'auto'}),
        dcc.Graph(
            figure={
                'data': [{'type': 'image', 'source': img_src}],
                'layout': {
                    'xaxis': {'visible': False},
                    'yaxis': {'visible': False},
                    'images': [{
                        'source': img_src,
                        'xref': 'x',
                        'yref': 'y',
                        'x': 0.5,
                        'y': 0.5,
                        'sizex': 1,
                        'sizey': 1,
                        'xanchor': 'center',
                        'yanchor': 'middle',
                        'layer': 'below'
                    }]
                }
            },
            id='word-cloud'
        ),
        dbc.Button("Generate Word Cloud", id='generate-button', n_clicks=0, color="primary")
    ])

# Dash app setup
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

@app.callback(
    Output('word-cloud', 'figure'),
    [Input('generate-button', 'n_clicks')]
)
def update_word_cloud(n):
    if n is None:
        raise dash.exceptions.PreventUpdate

    # Introduce variability in the text
    random_suffix = " " + str(random.randint(0, 10000))
    new_text = default_text + random_suffix
    
    img = generate_wordcloud(new_text)
    img_src = "data:image/png;base64,{}".format(img)
    return {
        'data': [{'type': 'image', 'source': img_src}],
        'layout': {
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'images': [{
                'source': img_src,
                'xref': 'x',
                'yref': 'y',
                'x': 0.5,
                'y': 0.5,
                'sizex': 1,
                'sizey': 1,
                'xanchor': 'center',
                'yanchor': 'middle',
                'layer': 'below'
            }]
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)

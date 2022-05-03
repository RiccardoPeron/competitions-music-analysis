import csv
import pandas as pd
import plotly.graph_objects as go
from tqdm import tqdm

df = pd.read_csv('results.csv', header=0)
index = list(df.columns)

tracks = index[0]

x = [track[:5] for track in df[tracks]]

fig = go.Figure()
fig.update_layout(title='Essentia extractor plot',
                  xaxis_title='song',
                  yaxis_title='value')

for id in tqdm(index):
    if id != tracks and 'stdev' not in id:
        y = [track for track in df[id]]
        if not all(v == 0 for v in y):
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    name=id
                )
            )

fig.write_html("OST_results/essentia_features_plot.html")
fig.show()

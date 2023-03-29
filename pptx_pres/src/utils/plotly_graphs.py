# Created by Thierry Tran
# Created on 22 December 2022
# Create functions to generate Plotly graphs

import plotly.graph_objects as go


def pie_chart(labs:list, vals:list, colours: list, width: int, height: int):
    data = go.Pie(labels=labs, values=vals)
    layout = go.Layout(autosize=False, width=width, height=height,
                       legend={'font': dict(family="Arial", size=40)})
    fig = go.Figure(data=[data], layout=layout)
    fig.update_traces(textfont_size=40, marker={'colors': colours})
    return fig


def bar_chart(labs: list, vals: dict, colour: dict, width: int, height: int):
    trace = []
    for key in vals:
        temp = go.Bar(name=key, x=labs, y=vals[key], marker={'color': colour[key]})
        trace.append(temp)

    layout = go.Layout(autosize=False, width=width, height=height,
                       legend={'font': dict(family="Arial", size=40)}, plot_bgcolor='rgba(0,0,0,0)')
    fig = go.Figure(data=trace, layout=layout)
    fig.update_traces(textfont_size=40)
    return fig


def stacked_bar_chart(labs: list, vals: dict, colour: dict, width: int, height: int):
    fig = bar_chart(labs, vals, colour, width, height)
    fig.update_layout(barmode='stack')
    return fig


def scatter_plot(val_x: dict, val_y: dict, colour: dict, mode: dict, width: int, height: int):
    trace = []
    for key in val_x:
        temp = go.Scatter(x=val_x[key], y=val_y[key], name=key, mode=mode[key], marker={'color': colour[key]})
        trace.append(temp)

    layout = go.Layout(autosize=False, width=width, height=height,
                       legend={'font': dict(family="Arial", size=40)}, plot_bgcolor='rgba(0,0,0,0)')
    fig = go.Figure(data=trace, layout=layout)
    fig.update_traces(textfont_size=40)

    return fig


if __name__ == '__main__':

    import os
    import plotly.io as pio

    # Internal module
    from src.dataload.json_objects import load_json

    current_dir = os.path.dirname(os.path.abspath("__file__"))
    sqt_colours = load_json(os.path.join(current_dir, 'data', 'sqt_colours.json'), "r")
    pio.renderers.default = "browser"

    labels = ['Base Salary', 'Bonuses', 'Benefits', 'Allowances']
    values = [25_000, 5_000, 500, 1_000]
    marker_colors = [sqt_colours['allstate_navy'], sqt_colours['allstate_light_blue'], sqt_colours['allstate_blue'],
                     sqt_colours['accent_coral']]

    dict_values_multiple = {'Person X': [25_000, 5_000, 500, 1_000], 'Person Y': [55_000, 2_000, 1_500, 100]}
    dict_values_single = {'Person X': [25_000, 5_000, 500, 1_000]}
    dict_colours_mulitple = {'Person X': sqt_colours['allstate_navy'], 'Person Y': sqt_colours['allstate_light_blue']}
    dict_colours_single = {'Person X': sqt_colours['allstate_navy']}

    mode = {'Person X': 'lines', 'Person Y': 'markers'}
    val_x = {'Person X': [12_000, 24_000, 500, 2_000], 'Person Y': [15_000, 6_000, 5_500, 900]}
    val_y = {'Person X': [24_000, 34_000, 900, 5_000], 'Person Y': [4_000, 7_000, 9_500, 880]}

    pie_chart(labels, values, marker_colors, 1500, 1000).show()
    bar_chart(labels, dict_values_single, dict_colours_single, 1500, 1000).show()
    bar_chart(labels, dict_values_multiple, dict_colours_mulitple, 1500, 1000).show()
    stacked_bar_chart(labels, dict_values_multiple, dict_colours_mulitple, 1500, 1000).show()
    scatter_plot(val_x, val_y, dict_colours_mulitple, mode, 1500, 1000).show()

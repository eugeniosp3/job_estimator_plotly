# dgphm

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import date
import re

todays_date = date.today()

app = dash.Dash()
server = app.server



app.layout = html.Div([
    html.Label('Home Construction Year Estimate'),
    html.Br(),
    html.Br(),
    dcc.Dropdown(id='const-year',
        options=[{'label': 'Around {A}'.format(A=x), 'value': x} for x in range(1900, todays_date.year, 20)],
    searchable=False
),
    html.Br(),
    html.Label('Square Footage of Space'),
    html.Br(),
    html.Br(),

    dcc.Slider(
        id='sq-feet',
        min=0,
        max=10,
        marks={i: '{} Sq Feet'.format(i * 500) for i in range(11)},
        value=0,
    ),

    html.Br(),
    html.Label('Types of Units In Home'),
    html.Br(),
    html.Br(),

    dcc.Checklist(id='unit-type',
        options=[
            {'label': 'Window Unit', 'value': 'Window Unit'},
            {'label': 'Gas Heater', 'value': 'Gas Heater'},
            {'label': 'Electric Heater', 'value': 'Electric Heater'},
            {'label': 'Electric Cooler', 'value': 'Electric Cooler'},
            {'label': 'Electric Two-in-One', 'value': 'Electric Two-in-One'}
        ],
        labelStyle={'display': 'inline-block'}),
    html.Br(),
    html.Label('Bedrooms'),
    html.Br(),
    html.Br(),

    dcc.Slider(
        id='rooms-number',
        min=0,
        max=9,
        marks={i: '{} Rooms'.format(i) for i in range(10)},
        value=3,
    ),

    html.Div(id='output-element'),
    html.Br(),
    html.Br(),
    html.Div(id='cost-holder')


]
    ,



)


@app.callback(
    Output('cost-holder', 'children'),
    [Input('const-year', 'value'),
     Input('unit-type', 'value'),
     Input('rooms-number', 'value'),
     Input('sq-feet', 'value'),])
def update_output(year_value, unit_type, rooms_number, sq_feet):

    est_multiplier = 0
    yc = year_value

    if yc <= 1960:
        est_multiplier = 1.45
    else:
        est_multiplier = 1.2
    print('yc: ', yc)



    print(unit_type)


    sf = sq_feet * 500
    print('sq feet', sf)
    if sf <= 1500:
        est_multiplier += 1.5
    if sf >= 1500 and sf <= 2500:
        est_multiplier += 1.85
    if sf > 2500:
        est_multiplier += 2.15

    unit_dictionary = {'Window Unit': 300, 'Gas Heater': 1500, 'Electric Heater': 800,
                       'Electric Cooling': 480, 'Electric Heater & Cooling': 1500}
    unit_cost = unit_dictionary[unit_type[0]]
    print(unit_cost)


    rn = rooms_number
    print(rn)

    if rn <= 4:
        est_multiplier += .35
    else:
        est_multiplier += .75

    final_cost = unit_cost * est_multiplier

    return 'Estimated Total (+/- 10% of Actual): {}'.format(final_cost)






if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)

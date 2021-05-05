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
    html.Label('Size of System to be Replaced'),
    html.Br(),
    html.Br(),

    dcc.RadioItems(
        id='system_size',
        options=[
            {'label': '.5-1.5 Tons', 'value': '0'},
            {'label': '2-3.5 Tons', 'value': '1'},
            {'label': '4-6 Tons', 'value': '2'},
            {'label': '6.5+ Tons', 'value': '3'},

        ],
        labelStyle={'display': 'inline-block'},
        value=''
    ),
    html.Br(),
    html.Br(),
    html.Label('How old is the system?'),
    html.Br(),
    html.Br(),
    dcc.RadioItems(
        id='sys-age',
        options=[
            {'label': '0-3 Years', 'value': '0'},
            {'label': '4-8 Years', 'value': '1'},
            {'label': '9-14 Years', 'value': '2'},
            {'label': '15+ Years', 'value': '3'},

        ],
        labelStyle={'display': 'inline-block'},
        value=''),
    html.Br(),
    html.Br(),
    html.Label('How many stories is the home (excluding basement)?'),
    html.Br(),
    html.Br(),
    dcc.RadioItems(
        id='stories_q',
        options=[
            {'label': '1 Floor', 'value': '0'},
            {'label': '2 Floors', 'value': '1'},
            {'label': '3 Floors', 'value': '2'},
            {'label': '4+ Floors', 'value': '3'}],

    ),
    html.Br(),
    html.Br(),
    html.Label('Approximate Home Construction Year'),
    html.Br(),
    html.Br(),
    dcc.Slider(id='const-year',
               min=1880,
               max=2020,
               value='',
               marks={x: 'Before {A}'.format(A=x) for x in range(1880, 2040, 20)},
               ),
    html.Label('Are there pets at home?'),
    html.Br(),
    html.Br(),
    dcc.RadioItems(
        id='pet-yesno',
        options=[
            {'label': 'Yes', 'value': '1'},
            {'label': 'No', 'value': '0'}
        ],
        labelStyle={'display': 'inline-block'},
        value=''),

    html.Br(),
    html.Label('Type of Unit'),
    html.Br(),
    html.Br(),

    dcc.RadioItems(
        id='unit-type',
        options=[
            {'label': 'Window Unit', 'value': 'Window Unit'},
            {'label': 'Gas Heater', 'value': 'Gas Heater'},
            {'label': 'Electric Heater', 'value': 'Electric Heater'},
            {'label': 'Electric Cooler', 'value': 'Electric Cooling'},
            {'label': 'Electric Two-in-One', 'value': 'Electric Heater & Cooling'}
        ],
        labelStyle={'display': 'inline-block'},
    ),
    html.Br(),
    html.Label('Number of Rooms (Bed/Office/Play)'),
    html.Br(),
    html.Br(),

    dcc.RadioItems(
        id='rooms_check',
        options=[
            {'label': '1-3 Rooms', 'value': '1to3'},
            {'label': '4-6 Rooms', 'value': '4to6'},
            {'label': '7+ Rooms', 'value': '7ormore'}
        ],
        value='',
        labelStyle={'display': 'inline-block'},
    ),

    html.Div(id='output-element'),
    html.Br(),
    html.Br(),
    html.Div(id='cost-holder'),
    html.Br(),
    html.Br(),


]
    ,

)


@app.callback(
    Output('cost-holder', 'children'),
    [Input('const-year', 'value'),
     Input('unit-type', 'value'),
     Input('rooms-number', 'value'),
     Input('sq-feet', 'value'), ])
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
    app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)

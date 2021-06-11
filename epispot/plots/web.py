"""
The `web` module contains various web-based plotting mechanisms.
These plotting mechanisms use `plotly` to generate in-browser plots of epispot models.
`plotly` is a required dependency for these modules. If you haven't already, install it with:
```shell
pip install plotly
```

## Structure:

- model
"""

from . import px


def model(Model, time_frame, starting_state=None, compartments=None, names=None, show_susceptible=False, log=False, colors=None):
    """
    Plots the results of one model using `plotly`.
    The results are displayed in-browser via a `localhost`.
    There are various ways to customize the generated plots by modifying
    the time frame or compartments displayed.

    - Model: An `epispot.models.Model` object
    - time_frame: A `range()` describing the time period to plot
    - starting_state: (default:inherited) Initial model state (see `epispot.models.Model.integrate` parameter `starting_state`)
    - compartments: (default:all) The indices of the compartments in the model to plot; 
                    all other compartments will be hidden
    - names: (default:`Model.layer_names`) A list of names for each of the compartments (**cannot be `'index'` or `'value'`**)
    - show_susceptible: (`=False`) Boolean value describing whether or not to plot the Susceptible compartment.\
                                   **This assumes that the Susceptible compartment is the first in `Model`**\
                                   Note:\
                                   > This can potentially result in less visibility for other compartments
                                   > since usually the Susceptible compartment comprises of many, many
                                   > more individuals than the other compartments combined.
    - log: (`=False`) Boolean value indicating whether or not to use a logarithmic scale when plotting `Model`
    - colors: (default:plotly default) A list of CSS-valid colors to cycle through in the plot
    - return: `plotly` figure (display in-browser with `.show()`)
    """

    DataFrame = {}
    System = Model.integrate(time_frame, starting_state=starting_state)
    
    # parameter substitutions
    if compartments is None:
        compartments = range(len(Model.layers))
    
    if names is None:
        names = Model.layer_names
    
    # setup
    for name in names:
        DataFrame[name] = []
    
    for day in System:
        for i, compartment in enumerate(day):
            DataFrame[names[i]].append(compartment)
    
    if not show_susceptible:
        del DataFrame[names[0]]

    if not colors:
        colors = px.colors.qualitative.Alphabet

    # plotting
    Figure = px.line(DataFrame, 
                    labels={
                        'index': 'Time (in days)',
                        'value': 'Compartment Population'
                    }, 
                    title='Compartment Populations over Time',
                    color_discrete_sequence=colors, 
                    template='plotly_white',
                    log_y=log)
    return Figure
    

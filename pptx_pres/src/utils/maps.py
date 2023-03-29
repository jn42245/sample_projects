# Created by Thierry Tran
# Created on 24 December 2022
# Create functions to generate maps

import matplotlib
import matplotlib.pyplot as plt
import geopandas
from pathlib import Path


def highlight_countries_world(facecol: str, edgecol: str, line_width: int, coun_highlight: dict,
                              output_path: Path, continent: bool = False, continent_str: str = 'Africa',
                              cities: bool = False, c_marker: str = 'o',
                              c_color: str = 'red', c_mark_size: int = 10):
    matplotlib.use('Agg')
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres')).to_crs(4326)

    if continent:
        ax = world[world.continent == continent_str].plot(facecolor=facecol, edgecolor=edgecol,
                                                          linewidth=line_width, column=None, categorical=False,
                                                          legend=False, figsize=(25, 25))
    else:
        ax = world.plot(facecolor=facecol, edgecolor=edgecol,
                        linewidth=line_width, column=None, categorical=False, legend=False, figsize=(25, 25))
        if cities:
            towns = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))
            towns.plot(ax=ax, marker=c_marker, color=c_color, markersize=c_mark_size)

    for x in coun_highlight:
        world[world.name == x].plot(color=coun_highlight[x], ax=ax)

    ax.set_axis_off()
    plt.savefig(output_path, dpi=100)
    return plt


if __name__ == '__main__':
    import os

    wk_dir = os.path.dirname(os.path.abspath('__file__'))

    # World map with cities
    eur_countries_highlight = {'Italy': 'red',
                               'France': 'blue'}
    highlight_countries_world('gainsboro', 'black', 1, eur_countries_highlight,
                              Path(os.path.join(wk_dir, 'output', 'maps', 'example_1.jpeg')), cities=True)

    # Continent map
    afr_countries_highlight = {'South Africa': 'red',
                               'Morocco': 'blue',
                               'Nigeria': 'green'}
    highlight_countries_world('gainsboro', 'black', 1, afr_countries_highlight,
                              Path(os.path.join(wk_dir, 'output', 'maps', 'example_2.jpeg')), continent=True,
                              continent_str='Africa')

aligned_treemap
========

Pure Python implementation of the squarify treemap layout algorithm.
----
Squarified Treemap Layout

    by Uri Laserson, uri.laserson@gmail.com

Implements algorithm from Bruls, Huizing, van Wijk, "Squarified Treemaps"
(but not using their pseudocode)


----
Weight Balanced Treemap Layout

    by Tony Tong, tony.tong@punchh.com

Implements a regular one-level treemap generation algorithm by finding optimal
split that minimizes the weight (size) imbalances between two sub-groups.



----
Aligned Treemap Layout

    by Tony Tong, tony.tong@punchh.com

Expands from the above weight balanced treemap by introducing x and y alignment
values, such that the rectangles are also aligned in the x and y axis.
The x_align nad y_align are purely for alignment purposes, therefore, as long
as they can each be sorted it should work.  If you need to reverse the alignment,
simply multiply the alignment values by -1.

Installation
------------

Compatible with Python 3.

    pip install aligned_treemap


Usage
-----
First, prepare the data.  Here assume the source data is in a pandas dataframe.

```python
from aligned_treemap import treemap

sizes = data.population
x_align = data.frequency.astype('float')
y_align = data.monetary.astype('float')
```

```python
from aligned_treemap import treemap

treemap.aligned_treemap(data.population, x_align=x_align, y_align=y_align, x=0, y=0, dx=100, dy=100, labels=data.tier)
```

The direct output is a list of dictionaries with each element defining a rectangular box. 
```json
[
    {
        "x": 0,
        "y": 0,
        "dx": 19.043630079337937,
        "dy": 27.498323741409173,
        "label": "hibernating",
        "value": 523.6679051332723
    },
    {
        "x": 19.043630079337937,
        "y": 0,
        "dx": 20.863052902012598,
        "dy": 27.498323741409177,
        "label": "low_value_frequent",
        "value": 573.6989829336886
    },
    {
        "x": 0,
        "y": 27.498323741409173,
        "dx": 21.919353697296845,
        "dy": 23.193831368385766,
        "label": "tending_to_lapse",
        "value": 508.3937933591061
    },
    {
        "x": 21.919353697296845,
        "y": 27.498323741409173,
        "dx": 17.98732928405369,
        "dy": 23.19383136838576,
        "label": "new nurturing_customer",
        "value": 417.1950821819682
    },
    {
        "x": 0,
        "y": 50.69215510979494,
        "dx": 39.906682981350535,
        "dy": 5.892048946750852,
        "label": "new frequent",
        "value": 235.13212942858655
    },
    {
        "x": 0,
        "y": 56.58420405654579,
        "dx": 39.906682981350535,
        "dy": 40.869978208638315,
        "label": "nurturing_customer",
        "value": 1630.985263826834
    },
    {
        "x": 0,
        "y": 97.4541822651841,
        "dx": 30.77577115516497,
        "dy": 2.5458177348158912,
        "label": "new potential_loyalist",
        "value": 78.34950400945434
    },
    {
        "x": 30.77577115516497,
        "y": 97.4541822651841,
        "dx": 8.911945115725468,
        "dy": 2.5458177348158912,
        "label": "new big_spender",
        "value": 22.688187927319756
    },
    {
        "x": 39.68771627089044,
        "y": 97.4541822651841,
        "dx": 0.21896671046009605,
        "dy": 2.5458177348157647,
        "label": "big_spender",
        "value": 0.5574493348235812
    },
    {
        "x": 39.906682981350535,
        "y": 0,
        "dx": 53.188895530331436,
        "dy": 57.202888669347544,
        "label": "frequent",
        "value": 3042.5584694671065
    },
    {
        "x": 93.09557851168196,
        "y": 0,
        "dx": 6.904421488318029,
        "dy": 57.20288866934758,
        "label": "loyal_joe",
        "value": 394.9528537225073
    },
    {
        "x": 39.906682981350535,
        "y": 57.20288866934755,
        "dx": 57.50321696789497,
        "dy": 42.79711133065245,
        "label": "champion",
        "value": 2460.971578445664
    },
    {
        "x": 97.4098999492455,
        "y": 57.20288866934755,
        "dx": 2.5901000507544936,
        "dy": 42.79711133065264,
        "label": "new champion",
        "value": 110.84880022966912
    }
]
```

Similarly, to call the standard weight balanced treemap construction:
```python
from aligned_treemap import treemap

treemap.treemap(data.population, x=0, y=0, dx=100, dy=100, labels=data.tier)
```

Output:
```json
[
    {
        "x": 0,
        "y": 0,
        "dx": 55.035300479127706,
        "dy": 55.283762294002656,
        "label": "frequent",
        "value": 3042.5584694671065
    },
    {
        "x": 0,
        "y": 55.283762294002656,
        "dx": 55.035300479127706,
        "dy": 44.716237705997344,
        "label": "champion",
        "value": 2460.971578445664
    },
    {
        "x": 55.035300479127706,
        "y": 0,
        "dx": 44.964699520872294,
        "dy": 36.27257117707953,
        "label": "nurturing_customer",
        "value": 1630.985263826834
    },
    {
        "x": 55.035300479127706,
        "y": 36.27257117707953,
        "dx": 44.96469952087231,
        "dy": 12.75887505191448,
        "label": "low_value_frequent",
        "value": 573.6989829336886
    },
    {
        "x": 55.035300479127706,
        "y": 49.03144622899401,
        "dx": 22.81507979361966,
        "dy": 22.952709780998372,
        "label": "hibernating",
        "value": 523.6679051332723
    },
    {
        "x": 77.85038027274737,
        "y": 49.03144622899401,
        "dx": 22.149619727252635,
        "dy": 22.952709780998376,
        "label": "tending_to_lapse",
        "value": 508.3937933591061
    },
    {
        "x": 55.035300479127706,
        "y": 71.98415600999238,
        "dx": 14.891397965050372,
        "dy": 28.01584399000762,
        "label": "new nurturing_customer",
        "value": 417.1950821819682
    },
    {
        "x": 69.92669844417807,
        "y": 71.98415600999238,
        "dx": 14.097481905716448,
        "dy": 28.01584399000762,
        "label": "loyal_joe",
        "value": 394.9528537225073
    },
    {
        "x": 84.02418034989452,
        "y": 71.98415600999238,
        "dx": 15.975819650105475,
        "dy": 14.71800099014226,
        "label": "new frequent",
        "value": 235.13212942858655
    },
    {
        "x": 84.02418034989452,
        "y": 86.70215700013463,
        "dx": 8.335848169570918,
        "dy": 13.297842999865363,
        "label": "new champion",
        "value": 110.84880022966912
    },
    {
        "x": 92.36002851946544,
        "y": 86.70215700013463,
        "dx": 7.639971480534557,
        "dy": 10.255208963682197,
        "label": "new potential_loyalist",
        "value": 78.34950400945434
    },
    {
        "x": 92.36002851946544,
        "y": 96.95736596381683,
        "dx": 7.456758735198065,
        "dy": 3.0426340361831645,
        "label": "new big_spender",
        "value": 22.688187927319756
    },
    {
        "x": 99.81678725466351,
        "y": 96.95736596381683,
        "dx": 0.18321274533649223,
        "dy": 3.042634036184319,
        "label": "big_spender",
        "value": 0.5574493348235812
    }
]
```

The rectangles can be easily plotted using, for example,
[d3.js](http://d3js.org/).

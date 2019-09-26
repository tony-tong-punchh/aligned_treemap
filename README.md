aligned_treemap
========

Pure Python implementation of the squarify treemap layout algorithm.

version: 1.0.0

#### Weight Balanced Treemap Layout

by Tony Tong, ttong@pro-ai.org

Implements a regular one-level treemap generation algorithm by finding optimal
split that minimizes the weight (size) imbalances between two sub-groups.


#### Aligned Treemap Layout
    
by Tony Tong, ttong@pro-ai.org

Expands from the above weight balanced treemap by introducing x and y alignment
values, such that the rectangles are also aligned in the x and y axis.
The x_align nad y_align are purely for alignment purposes, therefore, as long
as they can each be sorted it should work.  If you need to reverse the alignment,
simply multiply the alignment values by -1.


#### Squarified Treemap Layout

by Uri Laserson, uri.laserson@gmail.com

Implements algorithm from Bruls, Huizing, van Wijk, "Squarified Treemaps"
(but not using their pseudocode)


Installation
------------

Compatible with Python 3.

    pip install aligned_treemap


Usage
-----
First, prepare the data.  Here assume the source data is in a pandas dataframe.
![alt text](tabulated_data.png "Sample Data with Customer RFM Segmentation")

```python
from aligned_treemap import treemap
import matplotlib
import numpy as np

cmap = matplotlib.cm.get_cmap('GnBu')
c = [cmap(i) for i in range(256)]

# sizes = data.population
# labels = data.tier
# x_align = data.monetary
# y_align = data.recency
data.color = np.array(c)[list(map(int, data.monetary*255))]

treemap.aligned_treemap(
    sizes=data.population, 
    x_align=data.frequency, 
    y_align=data.monetary, 
    x=0, 
    y=0, 
    dx=100, 
    dy=100, 
    labels=data.tier,
    colors=data.color,
)
```

The direct output is a list of dictionaries with each element defining a rectangular box. 
```
[
  {
    "x": 0,
    "y": 0,
    "dx": 13.95819452037271,
    "dy": 28.295411211389347,
    "label": "loyal_joe",
    "value": 14170.0,
    "color": [
      0.9686274509803922,
      0.9882352941176471,
      0.9411764705882353,
      1.0
    ]
  },
  {
    "x": 13.95819452037271,
    "y": 0,
    "dx": 18.507167159404553,
    "dy": 28.295411211389343,
    "label": "hibernating",
    "value": 18788.0,
    "color": [
      0.9686274509803922,
      0.9882352941176471,
      0.9411764705882353,
      1.0
    ]
  },
    ......
    ......
  {
    "x": 94.69248015227211,
    "y": 95.72527497244653,
    "dx": 5.307519847728027,
    "dy": 4.274725027553465,
    "label": "new big_spender",
    "value": 814.0,
    "color": [
      0.03137254901960784,
      0.25098039215686274,
      0.5058823529411764,
      1.0
    ]
  }
]
```

Similarly, to call the standard weight balanced treemap constructor:
```python
treemap.treemap(
    sizes=data.population, 
    x=0, 
    y=0, 
    dx=100, 
    dy=100, 
    labels=data.tier, 
    color=data.color,
)
```

Output:
```
[
  {
    "x": 0,
    "y": 0,
    "dx": 55.035300479127706,
    "dy": 55.283762294002656,
    "label": "frequent",
    "value": 109160.0,
    "color": [
      0.485121107266436,
      0.801045751633987,
      0.7677047289504038,
      1.0
    ]
  },
  {
    "x": 0,
    "y": 55.283762294002656,
    "dx": 55.035300479127706,
    "dy": 44.716237705997344,
    "label": "champion",
    "value": 88294.0,
    "color": [
      0.23860053825451752,
      0.6269896193771627,
      0.7870818915801615,
      1.0
    ]
  },
  ......
  ......
  {
    "x": 99.81678725466351,
    "y": 96.95736596381683,
    "dx": 0.18321274533649223,
    "dy": 3.042634036184319,
    "label": "big_spender",
    "value": 20.0,
    "color": [
      0.03137254901960784,
      0.25098039215686274,
      0.5058823529411764,
      1.0
    ]
  }
]
```

Similary, to call the original squarify treemap constructor:
```python
treemap.squarify(
    data.population, 
    x=0, 
    y=0, 
    dx=100, 
    dy=100, 
    labels=data.tier, 
    colors=data.color,
)
```

To use the embedded plot function that uses `matplotlib` simply do the following:
```
fig, ax = plt.subplots(figsize=(18, 16))
treemap.plot(data.population, kind='aligned_treemap', norm_x=100, norm_y=100, \
    x_align=x_align, y_align=y_align, labels=data.tier, pad=False, alpha=0.7, ax=ax)
plt.axis('off')
```
![alt text](aligned_treemap.png "Sample Aligned Treemap with Customer RFM Segmentation")


The rectangles can be easily plotted using, for example,
[d3.js](http://d3js.org/).

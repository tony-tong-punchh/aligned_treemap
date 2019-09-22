"""
Various Treemaps Generation Algorithms

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
"""
import numpy as np


# INTERNAL FUNCTIONS not meant to be used by the user
def pad_rectangle(rect):
    if rect["dx"] > 2:
        rect["x"] += 1
        rect["dx"] -= 2
    if rect["dy"] > 2:
        rect["y"] += 1
        rect["dy"] -= 2


def layoutrow(sizes, x, y, dx, dy, labels=None, values=None):
    # generate rects for each size in sizes
    # dx >= dy
    # they will fill up height dy, and width will be determined by their area
    # sizes should be pre-normalized wrt dx * dy (i.e., they should be same units)
    covered_area = sum(sizes)
    width = covered_area / dy
    rects = []
    for i, size in enumerate(sizes):
        rects.append(
            {
                "x": x,
                "y": y,
                "dx": width,
                "dy": size / width,
                "label": labels[i] if labels else None,
                "value": values[i] if values else None,
            }
        )
        y += size / width
    return rects


def layoutcol(sizes, x, y, dx, dy, labels=None, values=None):
    # generate rects for each size in sizes
    # dx < dy
    # they will fill up width dx, and height will be determined by their area
    # sizes should be pre-normalized wrt dx * dy (i.e., they should be same units)
    covered_area = sum(sizes)
    height = covered_area / dx
    rects = []
    for i, size in enumerate(sizes):
        rects.append(
            {
                "x": x,
                "y": y,
                "dx": size / height,
                "dy": height,
                "label": labels[i] if labels else None,
                "value": values[i] if values else None,
            }
        )
        x += size / height
    return rects


def layout(sizes, x, y, dx, dy, labels=None, values=None):
    return (
        layoutrow(sizes, x, y, dx, dy, labels, values) if dx >= dy else layoutcol(sizes, x, y, dx, dy, labels, values)
    )


def leftoverrow(sizes, x, y, dx, dy):
    # compute remaining area when dx >= dy
    covered_area = sum(sizes)
    width = covered_area / dy
    leftover_x = x + width
    leftover_y = y
    leftover_dx = dx - width
    leftover_dy = dy
    return leftover_x, leftover_y, leftover_dx, leftover_dy


def leftovercol(sizes, x, y, dx, dy):
    # compute remaining area when dx >= dy
    covered_area = sum(sizes)
    height = covered_area / dx
    leftover_x = x
    leftover_y = y + height
    leftover_dx = dx
    leftover_dy = dy - height
    return leftover_x, leftover_y, leftover_dx, leftover_dy


def leftover(sizes, x, y, dx, dy):
    return leftoverrow(sizes, x, y, dx, dy) if dx >= dy else leftovercol(sizes, x, y, dx, dy)


def worst_ratio(sizes, x, y, dx, dy):
    return max([max(rect["dx"] / rect["dy"], rect["dy"] / rect["dx"]) for rect in layout(sizes, x, y, dx, dy)])


# Public API's
def squarify(sizes, x, y, dx, dy, labels, values):
    """Compute treemap rectangles.

    Given a set of values, computes a treemap layout in the specified geometry
    using an algorithm based on Bruls, Huizing, van Wijk, "Squarified Treemaps".
    See README for example usage.

    Parameters
    ----------
    sizes : list-like of numeric values
        The set of values to compute a treemap for. `sizes` must be positive
        values sorted in descending order and they should be normalized to the
        total area (i.e., `dx * dy == sum(sizes)`)
    x, y : numeric
        The coordinates of the "origin".
    dx, dy : numeric
        The full width (`dx`) and height (`dy`) of the treemap.
    labels: list-like of strings
        Text labels corresponding to sizes
    values: list-like of values
        Numerical values corresponding to sizes

    Returns
    -------
    list[dict]
        Each dict in the returned list represents a single rectangle in the
        treemap. The order corresponds to the input order.
    """
    sizes = list(map(float, sizes))
    labels = list(labels)
    values = list(values)

    if len(sizes) == 0:
        return []

    if len(sizes) == 1:
        return layout(sizes, x, y, dx, dy, labels, values)

    # figure out where 'split' should be
    i = 1
    while i < len(sizes) and worst_ratio(sizes[:i], x, y, dx, dy) >= worst_ratio(sizes[: (i + 1)], x, y, dx, dy):
        i += 1
    current, current_labels, current_values = sizes[:i], labels[:i], values[:i]
    remaining, remaining_labels, remaining_values = sizes[i:], labels[i:], values[i:]

    (leftover_x, leftover_y, leftover_dx, leftover_dy) = leftover(current, x, y, dx, dy)
    return layout(current, x, y, dx, dy, current_labels, current_values) + squarify(
        remaining, leftover_x, leftover_y, leftover_dx, leftover_dy, remaining_labels, remaining_values
    )


def padded_squarify(sizes, x, y, dx, dy, labels, values):
    """Compute padded treemap rectangles.

    See `squarify` docstring for details. The only difference is that the
    returned rectangles have been "padded" to allow for a visible border.
    """
    rects = squarify(sizes, x, y, dx, dy, labels, values)
    for rect in rects:
        pad_rectangle(rect)
    return rects


def normalize_sizes(sizes, dx, dy):
    """Normalize list of values.

    Normalizes a list of numeric values so that `sum(sizes) == dx * dy`.

    Parameters
    ----------
    sizes : list-like of numeric values
        Input list of numeric values to normalize.
    dx, dy : numeric
        The dimensions of the full rectangle to normalize total values to.

    Returns
    -------
    list[numeric]
        The normalized values.
    """
    total_size = sum(sizes)
    total_area = dx * dy
    sizes = map(float, sizes)
    sizes = map(lambda size: size * total_area / total_size, sizes)
    return list(sizes)


def weight_imbalance(sizes, i):
    """Calculate the weight imbalance between two subgroups separated at index i"""
    sizes = list(sizes)
    if i == 0 or i == len(sizes) - 1 or i == len(sizes):
        return sum(sizes)
    elif 0 < i < len(sizes) - 1:
        return abs(sum(sizes[:i]) - sum(sizes[i:]))
    else:
        raise IndexError(f"Split index {i} out of range for sizes with len of {len(sizes)}")


def argmin_weight_imbalance(sizes):
    """Find optimal index for splitting
    Returns the split index that minimized the weight imbalance between the
    two split sub-groups
    """
    sizes = list(sizes)
    last_weight_imbalance = sum(sizes)
    i = 1
    while i <= len(sizes) - 1:
        w_imb = weight_imbalance(sizes, i)
        if w_imb > last_weight_imbalance:
            break
        last_weight_imbalance = w_imb
        i += 1
    return i - 1


def split(head, x, y, dx, dy):
    """Split the area define by x, y, dx, dy into two rectangular boxes
    along the longer axis

    Returns two split rectanges (x1, y1, dx1, dy1), (x2, y2, dx2, dy2)
    """
    covered_area = sum(head)
    if dx >= dy:
        print("Split along x")
        width = covered_area / dy
        return (x, y, width, dy), (x + width, y, dx - width, dy)
    else:
        print("Split along y")
        height = covered_area / dx
        return (x, y, dx, height), (x, y + height, dx, dy - height)


def treemap(sizes, x, y, dx, dy, labels, values):
    """Compute treemap rectangles with min weight imbalances for each split.

    The difference to squarify algorithm is that this treemap generator does
    not consider aspect ratio as a crition.

    Parameters
    ----------
    sizes : list-like of numeric values
        The set of values to compute a treemap for. `sizes` must be positive
        values sorted in descending order and they should be normalized to the
        total area (i.e., `dx * dy == sum(sizes)`)
    x, y : list-like of numeric values
        The set of values are used to align the relative locations of each rectangle.
    dx, dy : numeric
        The full width (`dx`) and height (`dy`) of the treemap.
    labels: list-like of strings
        Text labels corresponding to sizes
    values: list-like of values
        Numerical values corresponding to sizes

    Returns
    -------
    list[dict]
        Each dict in the returned list represents a single rectangle in the
        treemap. The order corresponds to the input order.
    """
    sizes = list(map(float, sizes))
    labels = list(labels)
    values = list(values)

    if len(sizes) == 0:
        return []

    if len(sizes) == 1:
        return layout(sizes, x, y, dx, dy, labels, values)

    i = argmin_weight_imbalance(sizes)
    head, head_labels, head_values = sizes[:i], labels[:i], values[:i]
    tail, tail_labels, tail_values = sizes[i:], labels[i:], values[i:]

    head_rect, tail_rect = split(head, x, y, dx, dy)
    return treemap(head, *head_rect, head_labels, head_values) + treemap(tail, *tail_rect, tail_labels, tail_values)


def aligned_treemap(sizes, x_align, y_align, x, y, dx, dy, labels, values):
    """Compute treemap rectangles while aligning to x and y axes values.

    The key difference of aligned_treemap from treemap is that additional
    x_align and y_align list of values are passed in to help define the
    relative locations of the rectances along x and y axes.

    Parameters
    ----------
    sizes : list-like of numeric values
        The set of values to compute a treemap for. `sizes` must be positive
        values sorted in descending order and they should be normalized to the
        total area (i.e., `dx * dy == sum(sizes)`)
    x_align, y_align
        list-like values for x-dim and y-dim used for aligning the blocks
    x, y : list-like of numeric values
        The set of values are used to align the relative locations of each rectangle.
    dx, dy : numeric
        The full width (`dx`) and height (`dy`) of the treemap.
    labels: list-like of strings
        Text labels corresponding to sizes
    values: list-like of values
        Numerical values corresponding to sizes

    Returns
    -------
    list[dict]
        Each dict in the returned list represents a single rectangle in the
        treemap. The order corresponds to the input order.
    """
    print("Size of sizes: ", len(sizes))
    if len(sizes) == 0:
        return []

    if len(sizes) == 1:
        return layout(sizes, x, y, dx, dy, labels, values)

    sizes = np.array(list(map(float, sizes)))
    x_align = np.array(list(map(float, x_align)))
    y_align = np.array(list(map(float, y_align)))
    labels = np.array(list(labels))
    values = np.array(list(values))

    idx = np.argsort(x_align) if dx >= dy else np.argsort(y_align)
    sizes = sizes[idx]
    x_align = x_align[idx]
    y_align = y_align[idx]
    labels = labels[idx]
    values = values[idx]
    print(idx)
    print(sizes)
    print(x_align)
    print(y_align)
    print(labels)
    print(values)

    i = argmin_weight_imbalance(sizes)
    head, head_x_align, head_y_align, head_labels, head_values = (
        sizes[:i],
        x_align[:i],
        y_align[:i],
        labels[:i],
        values[:i],
    )
    tail, tail_x_align, tail_y_align, tail_labels, tail_values = (
        sizes[i:],
        x_align[i:],
        y_align[i:],
        labels[i:],
        values[i:],
    )
    print("Size of head: ", len(head))
    print("Size of tail: ", len(tail))

    head_rect, tail_rect = split(head, x, y, dx, dy)

    return aligned_treemap(head, head_x_align, head_y_align, *head_rect, head_labels, head_values) + aligned_treemap(
        tail, tail_x_align, tail_y_align, *tail_rect, tail_labels, tail_values
    )


def plot(
    sizes,
    kind="squarify",
    norm_x=100,
    norm_y=100,
    x_align=None,
    y_align=None,
    color=None,
    labels=None,
    values=None,
    ax=None,
    pad=False,
    bar_kwargs=None,
    text_kwargs=None,
    **kwargs,
):
    """Plotting with Matplotlib.

    Parameters
    ----------
    sizes
        input for squarify
    kind
        'squarify', 'treemap', or 'ordered', default is 'squarify'
    norm_x, norm_y
        x and y values for normalization
    x_align, y_align
        list-like values for x-dim and y-dim used for aligning the blocks
    color
        color string or list-like (see Matplotlib documentation for details)
    labels
        list-like used as label text
    values
        list-like used as value text (in most cases identical with sizes argument)
    ax
        Matplotlib Axes instance
    pad
        draw rectangles with a small gap between them
    bar_kwargs : dict
        keyword arguments passed to matplotlib.Axes.bar
    text_kwargs : dict
        keyword arguments passed to matplotlib.Axes.text
    **kwargs
        Any additional kwargs are merged into `bar_kwargs`. Explicitly provided
        kwargs here will take precedence.

    Returns
    -------
    matplotlib.axes.Axes
        Matplotlib Axes
    """

    import matplotlib.pyplot as plt

    if ax is None:
        ax = plt.gca()

    if color is None:
        import matplotlib.cm
        import random

        cmap = matplotlib.cm.get_cmap()
        color = [cmap(random.random()) for i in range(len(sizes))]

    if bar_kwargs is None:
        bar_kwargs = {}
    if text_kwargs is None:
        text_kwargs = {}
    if len(kwargs) > 0:
        bar_kwargs.update(kwargs)

    normed = normalize_sizes(sizes, norm_x, norm_y)

    if kind == "squarify":
        if pad:
            rects = padded_squarify(normed, 0, 0, norm_x, norm_y, labels, values)
        else:
            rects = squarify(normed, 0, 0, norm_x, norm_y, labels, values)
    elif kind == "treemap":
        rects = treemap(normed, 0, 0, norm_x, norm_y, labels, values)
    elif kind == "aligned_treemap":
        assert (
            x_align is not None and y_align is not None
        ), "x_align and y_align need to be provided for aligned_treemap"
        rects = aligned_treemap(normed, x_align, y_align, 0, 0, norm_x, norm_y, labels, values)

    x = [rect["x"] for rect in rects]
    y = [rect["y"] for rect in rects]
    dx = [rect["dx"] for rect in rects]
    dy = [rect["dy"] for rect in rects]
    labels = [rect["label"] for rect in rects]
    values = [rect["value"] for rect in rects]
    print(labels)
    print(values)

    ax.bar(x, dy, width=dx, bottom=y, color=color, label=labels, align="edge", **bar_kwargs)

    if not values is None:
        va = "center" if labels is None else "top"

        for v, r in zip(values, rects):
            x, y, dx, dy = r["x"], r["y"], r["dx"], r["dy"]
            ax.text(x + dx / 2, y + dy / 2, v, va=va, ha="center", **text_kwargs)

    if not labels is None:
        va = "center" if values is None else "bottom"
        for l, r in zip(labels, rects):
            x, y, dx, dy = r["x"], r["y"], r["dx"], r["dy"]
            ax.text(x + dx / 2, y + dy / 2, l, va=va, ha="center", **text_kwargs)

    ax.set_xlim(0, norm_x)
    ax.set_ylim(0, norm_y)

    return ax

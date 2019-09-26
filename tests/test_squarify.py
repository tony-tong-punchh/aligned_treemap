from aligned_treemap.treemap import normalize_sizes, squarify


expected = [
    {"dy": 433, "dx": 327.715_355_805_243_4, "x": 0, "y": 0},
    {"dy": 330.086_267_605_633_8, "dx": 372.284_644_194_756_6, "x": 327.715_355_805_243_4, "y": 0},
    {"dy": 102.913_732_394_366_2, "dx": 215.097_794_423_637_1, "x": 327.715_355_805_243_4, "y": 330.086_267_605_633_8},
    {"dy": 102.913_732_394_366_2, "dx": 68.941_600_776_806_77, "x": 542.813_150_228_880_5, "y": 330.086_267_605_633_8},
    {"dy": 80.401_353_433_098_54, "dx": 88.245_248_994_312_73, "x": 611.754_751_005_687_4, "y": 330.086_267_605_633_8},
    {"dy": 22.512_378_961_267_67, "dx": 88.245_248_994_312_4, "x": 611.754_751_005_687_4, "y": 410.487_621_038_732_3},
]


def test_squarify():
    x = 0.0
    y = 0.0
    width = 700.0
    height = 433.0
    values = [500, 433, 78, 25, 25, 7]
    values = normalize_sizes(values, width, height)
    observed = squarify(values, x, y, width, height)
    assert len(observed) == len(expected)
    for (o, e) in zip(observed, expected):
        assert len(o) == 4
        assert set(o.keys()) == set(["dx", "dy", "x", "y"])
        assert o["dx"] == e["dx"]
        assert o["dy"] == e["dy"]
        assert o["x"] == e["x"]
        assert o["y"] == e["y"]

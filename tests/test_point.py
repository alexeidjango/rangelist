from __future__ import absolute_import, unicode_literals

from rangelist.point import Point, NEG_INF, INF


def test_point():
    assert str(Point('-inf')) == '-inf'
    assert str(Point(3)) == '3'

    assert INF == INF
    assert NEG_INF == NEG_INF
    assert INF > NEG_INF
    assert NEG_INF < INF
    assert not INF > INF
    assert not NEG_INF < NEG_INF
    assert not INF < INF
    assert not NEG_INF < NEG_INF

    regular_point = Point(5)
    assert regular_point < Point(10)
    assert regular_point > Point(3)

    assert regular_point > NEG_INF
    assert NEG_INF < regular_point

    assert regular_point < INF
    assert INF > regular_point

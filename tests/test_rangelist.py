from __future__ import absolute_import, unicode_literals

import pytest

from rangelist.point import NEG_INF, INF, Point
from rangelist.rangeitem import RangeItem
from rangelist.rangelist import RangeList


def test_eq():
    assert RangeList() == RangeList()


def test_insert_non_intersecting():
    range_list = RangeList()
    items = [
        RangeItem('-inf', 0),
        RangeItem(3, 4),
        RangeItem(5, 'inf'),
        RangeItem(1, 2),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem('-inf', 0),
        RangeItem(1, 2),
        RangeItem(3, 4),
        RangeItem(5, 'inf'),
    ]


def test_insert_intersecting():
    # Simple intersection
    range_list = RangeList()
    items = [
        RangeItem(0, 2),
        RangeItem(1, 3),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(0, 3)
    ]

    # Boundary intersection
    range_list = RangeList()
    items = [
        RangeItem(0, 1),
        RangeItem(1, 3),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(0, 3)
    ]

    # Excluded intersection
    range_list = RangeList()
    items = [
        RangeItem(0, 1, right_excluded=True),
        RangeItem(1, 3),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(0, 1, right_excluded=True),
        RangeItem(1, 3, left_excluded=True)
    ]

    # Partial intersection with inclusion
    range_list = RangeList()
    items = [
        RangeItem(0, 2, right_excluded=True),
        RangeItem(1, 3, left_excluded=True),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(0, 1, right_excluded=True),
        RangeItem(1, 2, left_excluded=True, right_excluded=True),
        RangeItem(2, 3, left_excluded=True)
    ]

    range_list = RangeList()
    items = [
        RangeItem(1, 3, left_excluded=True),
        RangeItem(0, 2, right_excluded=True),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(0, 1, right_excluded=True),
        RangeItem(1, 2, left_excluded=True, right_excluded=True),
        RangeItem(2, 3, left_excluded=True)
    ]

    # Full intersection
    range_list = RangeList()
    items = [
        RangeItem(0, 1, right_excluded=True),
        RangeItem(0, 1, right_excluded=True),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(0, 1, right_excluded=True)
    ]

    # Full intersection of existing item
    range_list = RangeList()
    items = [
        RangeItem(0, 10),
        RangeItem(2, 5),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(0, 10)
    ]

    # Partial intersection of new item
    range_list = RangeList()
    items = [
        RangeItem(2, 5),
        RangeItem(0, 10),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(0, 10)
    ]

    # Partial intersection with multiple items
    range_list = RangeList()
    items = [
        RangeItem(0, 1),
        RangeItem(2, 3),
        RangeItem(4, 5),
        RangeItem(-1, 6)
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(-1, 6)
    ]

    # Full intersection of existing item with exclusion
    range_list = RangeList()
    items = [
        RangeItem(0, 10),
        RangeItem(2, 5, left_excluded=True, right_excluded=True),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(0, 2, right_excluded=True),
        RangeItem(2, 5, left_excluded=True, right_excluded=True),
        RangeItem(5, 10, left_excluded=True)
    ]

    range_list = RangeList()
    items = [
        RangeItem(2, 5, left_excluded=True, right_excluded=True),
        RangeItem(0, 10),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(0, 2, right_excluded=True),
        RangeItem(2, 5, left_excluded=True, right_excluded=True),
        RangeItem(5, 10, left_excluded=True)
    ]

    # Intersection with exclusion with multiple items

    range_list = RangeList()
    items = [
        RangeItem(1, 5, left_excluded=True, right_excluded=True),
        RangeItem(6, 10, left_excluded=True, right_excluded=True),
        RangeItem(4, 7, left_excluded=True, right_excluded=True),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(1, 4, left_excluded=True, right_excluded=True),
        RangeItem(4, 5, left_excluded=True, right_excluded=True),
        RangeItem(5, 6, left_excluded=True, right_excluded=True),
        RangeItem(6, 7, left_excluded=True, right_excluded=True),
        RangeItem(7, 10, left_excluded=True, right_excluded=True),
    ]

    # A nightmare
    range_list = RangeList()
    items = [
        RangeItem(NEG_INF, 10, right_excluded=True),
        RangeItem(3, INF, left_excluded=True),
        RangeItem(4, 11, left_excluded=True, right_excluded=True),
        RangeItem(3, 4)
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(NEG_INF, 3, right_excluded=True),
        RangeItem(3, 4, left_excluded=True, right_excluded=True),
        RangeItem(4, 10, left_excluded=True, right_excluded=True),
        RangeItem(10, 11, left_excluded=True, right_excluded=True),
        RangeItem(11, INF, left_excluded=True),
    ]

    range_list = RangeList()
    items = [
        RangeItem(3, 4, left_excluded=True, ),
        RangeItem(3, 4),
    ]
    for item in items:
        range_list.insert(item)
    assert range_list.items() == [
        RangeItem(3, 4, left_excluded=True),
    ]


def test_add_point():
    # add a point outside interval
    range_list = RangeList([
        RangeItem(1, 2),
        RangeItem(5, 6)
    ])
    range_list.insert(Point(3))
    assert range_list.items() == [
        RangeItem(1, 2),
        RangeItem(3, 3),
        RangeItem(5, 6)
    ]

    # verify infinity cannot be added
    with pytest.raises(AssertionError):
        range_list.insert(INF)
    with pytest.raises(AssertionError):
        range_list.insert(NEG_INF)

    # add a point to the middle of the interval
    range_list = RangeList([
        RangeItem(1, 4),
    ])
    range_list.insert(Point(3))
    assert range_list.items() == [
        RangeItem(1, 4),
    ]

    # add a point to a non-excluded bound
    range_list = RangeList([
        RangeItem(1, 4),
    ])
    range_list.insert(Point(4))
    assert range_list.items() == [
        RangeItem(1, 4),
    ]

    # add a point to an excluded bound
    range_list = RangeList([
        RangeItem(1, 4, right_excluded=True),
    ])
    range_list.insert(Point(4))
    assert range_list.items() == [
        RangeItem(1, 4),
    ]

    # add a point to an excluded 2-bound
    # add a point to an excluded bound
    range_list = RangeList([
        RangeItem(1, 4, right_excluded=True),
        RangeItem(4, 5, left_excluded=True)
    ])
    range_list.insert(Point(4))
    assert range_list.items() == [
        RangeItem(1, 5),
    ]

    r = RangeList()
    r.insert(RangeItem(0, 4))
    r.insert(RangeItem(5, 10, left_excluded=True))
    r.insert(RangeItem(2, 8))  # note that this range overlaps existing, but point 5 is excluded
    assert r.items() == [
        RangeItem(0, 5, right_excluded=True),
        RangeItem(5, 10, left_excluded=True)
    ]


def test_contains_point():
    range_list = RangeList()
    assert Point(3) not in range_list

    range_list = RangeList([RangeItem(1, 3)])
    assert Point(2) in range_list
    assert Point(1) in range_list
    assert Point(3) in range_list

    range_list = RangeList([RangeItem(1, 3, left_excluded=True, right_excluded=True)])
    assert Point(2) in range_list
    assert Point(1) not in range_list
    assert Point(3) not in range_list

    range_list = RangeList([
        RangeItem(1, 3, right_excluded=True),
        RangeItem(3, 5, left_excluded=True),
    ])
    assert Point(3) not in range_list
    assert Point(2) in range_list
    assert Point(4) in range_list

    range_list = RangeList([
        RangeItem(1, 1),
    ])
    assert Point(1) in range_list


def test_contains_range():
    ranges = [
        RangeItem(NEG_INF, 3),
        RangeItem(10, 12, right_excluded=True),
        RangeItem(15, 20, left_excluded=True),
        RangeItem(25, INF, left_excluded=True)
    ]
    range_list = RangeList(ranges)

    for range_item in ranges:
        assert range_item in range_list

    assert RangeItem(NEG_INF, 2) in range_list
    assert RangeItem(1, 2) in range_list
    assert RangeItem(2, 2) in range_list
    assert RangeItem(3, 3) in range_list

    assert RangeItem(2, 4) not in range_list
    assert RangeItem(5, 6) not in range_list
    assert RangeItem(15, 20) not in range_list

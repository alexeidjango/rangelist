from __future__ import absolute_import, unicode_literals

import pytest

from rangelist.rangeitem import RangeItem


def test_bounds():
    with pytest.raises(AssertionError):
        RangeItem(3, 1)
    with pytest.raises(AssertionError):
        RangeItem('inf', '-inf')
    with pytest.raises(AssertionError):
        RangeItem(1, '-inf')
    with pytest.raises(AssertionError):
        RangeItem('inf', 1)
    assert RangeItem('-inf', 5, left_excluded=True, right_excluded=False).left_excluded is False
    assert RangeItem(5, 'inf', left_excluded=True, right_excluded=True).right_excluded is False


def test_eq():
    for left in ('-inf', 1):
        for right in (5, 'inf'):
            for left_excluded in (True, False):
                for right_excluded in (True, False):
                    assert (
                        RangeItem(left, right, left_excluded, right_excluded) ==
                        RangeItem(left, right, left_excluded, right_excluded)
                    )
    assert RangeItem(1, 5, False, True) != RangeItem(1, 5, True, True)
    assert RangeItem(1, 5, True, False) != RangeItem(1, 5, True, True)
    assert RangeItem('-inf', 5, False) == RangeItem('-inf', 5, True)
    assert RangeItem(5, 'inf', True, False) == RangeItem(5, 'inf', True, True)


def test_contains_point():
    assert 1 in RangeItem(1, 6)
    assert 3 in RangeItem(1, 6)
    assert 6 in RangeItem(1, 6)
    assert 1 not in RangeItem(1, 6, left_excluded=True)
    assert 6 not in RangeItem(1, 6, right_excluded=True)
    assert 5 in RangeItem('-inf', 6)
    assert 5 in RangeItem(3, 'inf')
    assert '-inf' in RangeItem('-inf', 1)
    assert 'inf' in RangeItem(1, 'inf')


def test_contains_range():
    assert RangeItem(1, 5) in RangeItem(0, 6)
    assert RangeItem(1, 5, left_excluded=True, right_excluded=True) in RangeItem(1, 5)
    assert RangeItem('-inf', 1) in RangeItem('-inf', 2)
    assert RangeItem(1, 'inf') in RangeItem(0, 'inf')
    assert RangeItem(1, 2) in RangeItem(1, 2)
    assert RangeItem(1, 2, left_excluded=True) in RangeItem(1, 2, left_excluded=True)
    assert RangeItem('-inf', 'inf') in RangeItem('-inf', 'inf')


def test_repr():
    assert str(RangeItem(1, 5)) == '[1, 5]'
    assert str(RangeItem(1, 5, left_excluded=True)) == '(1, 5]'
    assert str(RangeItem(1, 5, right_excluded=True)) == '[1, 5)'
    assert str(RangeItem(1, 5, left_excluded=True, right_excluded=True)) == '(1, 5)'


def test_gte_point():
    assert 1 > RangeItem(0, 1, right_excluded=True)
    assert not 1 > RangeItem(0, 1, right_excluded=False)
    assert not 0.5 > RangeItem(0, 1)
    assert 1 >= RangeItem(0, 1)


def test_gte_range():
    assert RangeItem(2, 3) > RangeItem(0, 1)
    assert not RangeItem(1, 2) > RangeItem(0, 1)  # they have intersection
    assert not RangeItem(1, 3) > RangeItem(0, 2)
    assert RangeItem(1, 2, left_excluded=True) > RangeItem(0, 1)
    assert RangeItem(1, 2) > RangeItem(0, 1, right_excluded=True)

    assert RangeItem(3, 4) > RangeItem('-inf', 0)
    assert not RangeItem('-inf', 0) > RangeItem(3, 4)


def test_lte_point():
    assert 0 < RangeItem(0, 1, left_excluded=True)
    assert not 0 < RangeItem(0, 1)
    assert not 0.5 < RangeItem(0, 1)
    assert 0 <= RangeItem(0, 1)


def test_lte_range():
    assert RangeItem(0, 1) < RangeItem(2, 3)
    assert not RangeItem(0, 1) < RangeItem(1, 2)  # they have intersection
    assert not RangeItem(0, 2) < RangeItem(1, 3)
    assert RangeItem(0, 1) < RangeItem(1, 2, left_excluded=True)
    assert RangeItem(0, 1, right_excluded=True) < RangeItem(1, 2)

    assert RangeItem('-inf', 0) < RangeItem(3, 4)
    assert not RangeItem(3, 4) < RangeItem('-inf', 0)


def test_add():
    assert RangeItem(0, 1) + RangeItem(1, 2) == RangeItem(0, 2)
    assert RangeItem('-inf', 0) + RangeItem(0, 'inf') == RangeItem('-inf', 'inf')
    assert RangeItem(0, 2) + RangeItem(1, 3) == RangeItem(0, 3)
    assert RangeItem(1, 2) + RangeItem(1, 2) == RangeItem(1, 2)
    assert RangeItem(0, 5) + RangeItem(1, 3) == RangeItem(0, 5)
    assert RangeItem(1, 3) + RangeItem(0, 5) == RangeItem(0, 5)


def test_intersects_with():
    assert RangeItem(0, 1).intersects_with(RangeItem(0, 1))
    assert RangeItem(0, 2).intersects_with(RangeItem(1, 3))
    assert RangeItem('-inf', 2).intersects_with(RangeItem(1, 2))
    assert RangeItem(2, 'inf').intersects_with(RangeItem(0, 3))
    assert RangeItem('-inf', 'inf').intersects_with(RangeItem('-inf', 'inf'))
    assert not RangeItem(0, 1).intersects_with(RangeItem(2, 3))
    assert not RangeItem(0, 1).intersects_with(RangeItem(1, 2, left_excluded=True))
    assert RangeItem(0, 1).intersects_with(RangeItem(0.5, 2, left_excluded=True))
    assert not RangeItem(0, 1, right_excluded=True).intersects_with(RangeItem(1, 2))
    assert RangeItem(0, 1, right_excluded=True).intersects_with(RangeItem(0.5, 2))

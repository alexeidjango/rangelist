# Basics

Range is a continuous interval between two points (boundaries). E.g. a numeric interval, a time interval, alphabetic interval, etc. Examples of range are:

- (1; 3) – means that any number between 1 and 3 belongs to this interval, **excluding** 1 and 3.
- [1; 3] – means that any number between 1 and 3 belongs to this interval, **including** 1 and 3.
- (1; 3] – means that any number between 1 and 3 belongs to this interval, **excluding 1** and **including**  3. 

On the numeric or time scale multiple ranges can intersect or coexist. An arbitrary point on this scale can be included or excluded from the intersection of all ranges. 

The `rangelist` package, as follows from it's name, represents lists of ranges, but not just a plain list, but a proper, valid intersection of ranges on the numeric or time scale, and what's more important - tells if a point or a range belongs to the given list of ranges. 

A range is usually represented by (x; y) or [x; y] record, meaning literally 'Interval from x to y'.

Boundary points may or may not belong to the interval itself; to signify that, round or square brackets are used.

A range can be a single point, e.g. [1; 1] - this means that only 1 is in it's range. 

A continuous interval can have an excluded point. E.g. [1; 5] + (3;3) => [1; 3), (3; 5]

## Usage

There are 3 basic types: `Point`, `RangeItem` and `RangeList`.

`Point` basically represents a point, which can be an arbitrary value; there are 2 special points to represent infinity and negative infinity:

```python
>>> from rangelist.point import Point, INF, NEG_INF
>>> Point(1)
1
>>> Point(1) == Point(3)
False
>>> Point(1) == Point(1)
True
>>> Point(3) > Point(1)
True
>>> INF
inf
>>> NEG_INF
-inf
>>> INF > Point(999)
True

```

`RangeItem` represents a single range:

```python
>>> from rangelist.rangeitem import RangeItem
>>> RangeItem(1, 3, left_excluded=False, right_excluded=True)
[1, 3)
>>> 1 in RangeItem(1, 3, left_excluded=False, right_excluded=True)
True
>>> 2 in RangeItem(1, 3, left_excluded=False, right_excluded=True)
True
>>> 3 in RangeItem(1, 3, left_excluded=False, right_excluded=True)
False
```

Range items support basic math operations such as inclusion, equality and intersection checks. It's also possible to test a point for inclusion into given range:

```python
>>> RangeItem(1, 3) in RangeItem(0, 4)
True
>>> RangeItem(1, 3) == RangeItem(1, 3)
True
>>> RangeItem(1, 3) > RangeItem(-1, 0)
True
>>> RangeItem(1, 3).intersects_with(RangeItem(-1, 0))
False
>>> RangeItem(1, 3).intersects_with(RangeItem(-1, 2))
True
>>> 2 in RangeItem(1, 3)
True

```

`RangeList` represents intersection of multiple `RangeItem`objects, honouring their boundaries:

1. Add 2 ranges with **included** boundaries, and then add a range that overlaps both ranges, hence it will create a single, continuous range:

   ```python
   >>> r = RangeList()
   >>> r.insert(RangeItem(0, 2))
   >>> r
   ['[0, 2]']
   >>> r.insert(RangeItem(10, 20))
   >>> r
   ['[0, 2]', '[10, 20]']
   >>> r.insert(RangeItem(1, 11))
   >>> r
   ['[0, 20]']
   ```

2. Add 2 ranges, one range has excluded boundary. Then add a range that overlaps both. In this case excluded boundary point must stay excluded (ranges will break):

   ```python
   >>> r = RangeList()
   >>> r.insert(RangeItem(0, 4))
   >>> r
   ['[0, 4]']
   >>> r.insert(RangeItem(5, 10, left_excluded=True))
   >>> r
   ['[0, 4]', '(5, 10]']
   >>> r.insert(RangeItem(2, 8))  # note that this range overlaps existing, but point 5 is excluded
   >>> r
   ['[0, 5)', '(5, 10]']
   ```

3. Just a bit more complex example, when we overlap 2 ranges with excluded boundaries:

   ```python
   >>> r = RangeList()
   >>> r.insert(RangeItem(1, 4, left_excluded=True, right_excluded=True))
   >>> r
   ['(1, 4)']
   >>> r.insert(RangeItem(3, 6, left_excluded=True, right_excluded=True))
   >>> r
   ['(1, 3)', '(3, 4)', '(4, 6)']
   >>> 2 in r
   True
   >>> 3 in r
   False
   >>> 4 in r
   False
   >>> 5 in r
   >>> RangeItem(4.5, 5.5) in r
   True
   >>> RangeItem(4, 6) in r
   False
   >>> RangeItem(4, 6, left_excluded=True, right_excluded=True) in r
   True
   ```

# Real world application

Consider 2 examples:

1. Range intersection on the numeric scale. Suppose we want to program system of equations:

   - x < -5
   - x ≠2
   - x > - 1

   and then be able to test if an arbitrary point satisfies these equations.

    Let's create a range intersection with `rangelist`

   ```python
   >>> from rangelist.rangelist import RangeList
   >>> from rangelist.rangeitem import RangeItem
   >>> from rangelist.point import INF, NEG_INF
   >>> 
   >>> range_items = [
   ...     RangeItem(NEG_INF, -5, right_excluded=True),
   ...     RangeItem(2, 2, left_excluded=True, right_excluded=True),
   ...     RangeItem(-1, INF, left_excluded=True),
   ... ]
   >>> 
   >>> range_list = RangeList(range_items)
   >>> range_list
   ['[-inf, -5)', '(-1, 2)', '(2, inf]']
   >>> -10 in range_list
   True
   >>> -5 in range_list  # should be False, since -5 is not included
   False
   >>> -3 in range_list  # should be False, it's outside of any interval
   False
   >>> 0 in range_list  # should be True
   True
   >>> 10 in range_list  # should be True
   True
   ```

2. Timescale. Suppose we're building a system that sends notifications to customers, and each customer has their own rules when to send or not send them notifications. Suppose a customer wants notifications to be sent from 8am sharp to 10am, and from 1pm to 8pm excluding lunch time 2:30pm - 3pm. Let's build a range list for this example, and then we can test an arbitrary time to see if it fits customer's expectations:

   ```python
   >>> r = RangeList()
   >>> r.insert(RangeItem(dt.time(8, 0), dt.time(10, 0), right_excluded=True))
   >>> r.insert(RangeItem(dt.time(13, 0), dt.time(14, 30), right_excluded=True))
   >>> r.insert(RangeItem(dt.time(15, 0), dt.time(20, 0), right_excluded=True))
   >>> r
   ['[08:00:00, 10:00:00)', '[13:00:00, 14:30:00)', '[15:00:00, 20:00:00)']
   >>> dt.time(8, 0) in r
   True
   >>> dt.time(10, 0) in r
   False
   >>> dt.time(14, 0) in r
   True
   >>> dt.time(14, 30) in r
   False
   >>> dt.time(20, 30) in r
   False
   ```

# Installation

Best way to install is using `pip`: `pip install rangelist`
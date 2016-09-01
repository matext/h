# -*- coding: utf-8 -*-

"""
Matchers for use in tests.

This module contains objects which can be used to write tests which are easier
to read, especially when using assertions against :py:class:`mock.Mock`
objects. Each matcher defines an __eq__ method, allowing instances of these
matchers to be used wherever you would usually pass a plain value.

For example, imagine you wanted to ensure that the `set_value` method of the
`foo` mock object was called exactly once with an integer. Previously you
would have to do something like:

    assert foo.set_value.call_count == 1
    assert isinstance(foo.set_value.call_args[0][0], int)

By using the `instance_of` matcher you can simply write:

    foo.set_value.assert_called_once_with(matchers.instance_of(int))

As a bonus, the second test will print substantially more useful debugging
output if it fails, e.g.

    E       AssertionError: Expected call: set_value(<instance of <type 'int'>>)
    E       Actual call: set_value('a string')

"""
from pyramid import httpexceptions


class any_callable(object):  # noqa: N801
    """An object __eq__ to any callable object."""

    def __eq__(self, other):
        """Return ``True`` if ``other`` is callable, ``False`` otherwise."""
        return callable(other)


class instance_of(object):  # noqa: N801
    """An object __eq__ to any object which is an instance of `type_`."""

    def __init__(self, type_):
        self.type = type_

    def __eq__(self, other):
        return isinstance(other, self.type)

    def __repr__(self):
        return '<instance of {!r}>'.format(self.type)


class iterable_with(object):  # noqa: N801
    """An object __eq__ to any iterable which yields `items`."""

    def __init__(self, items):
        self.items = items

    def __eq__(self, other):
        return list(other) == self.items

    def __repr__(self):
        return '<iterable with {!r}>'.format(self.items)


class mapping_containing(object):  # noqa: N801
    """An object __eq__ to any mapping with the passed `key`."""

    def __init__(self, key):
        self.key = key

    def __eq__(self, other):
        try:
            other[self.key]
        except (TypeError, KeyError):
            return False
        else:
            return True

    def __repr__(self):
        return '<mapping containing {!r}>'.format(self.key)


class redirect_302_to(object):
    """Matches any HTTPFound redirect to the given URL."""

    def __init__(self, location):
        self.location = location

    def __eq__(self, other):
        if not isinstance(other, httpexceptions.HTTPFound):
            return False
        return other.location == self.location


class redirect_303_to(object):
    """Matches any HTTPSeeOther redirect to the given URL."""

    def __init__(self, location):
        self.location = location

    def __eq__(self, other):
        if not isinstance(other, httpexceptions.HTTPSeeOther):
            return False
        return other.location == self.location


class unordered_list(object):
    """
    Matches a list with the same items in any order.

    Matches any list that contains the same items as the given list
    (and no more), regardless of order.

    """

    def __init__(self, items):
        self.items = items

    def __eq__(self, other):
        return len(self.items) == len(other) and set(self.items) == set(other)

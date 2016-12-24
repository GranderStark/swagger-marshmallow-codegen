# -*- coding:utf-8 -*-
import logging
from collections import namedtuple
from .langhelpers import load_function
logger = logging.getLogger(__name__)


Pair = namedtuple("Pair", "type,format")

# TODO: correct mapping

TYPE_MAP = {
    Pair(type="string", format="time"): "marshmallow.fields:Time",
    Pair(type="string", format="date-time"): "marshmallow.fields:DateTime",
    Pair(type="string", format="date"): "marshmallow.fields:Date",
    Pair(type="string", format="uuid"): "marshmallow.fields:UUID",
    Pair(type="string", format=None): "marshmallow.fields:String",
    Pair(type="number", format="decimal"): "marshmallow.fields:Decimal",
    Pair(type="number", format="float"): "marshmallow.fields:Float",
    Pair(type="number", format="integer"): "marshmallow.fields:Integer",
    Pair(type="integer", format=None): "marshmallow.fields:Integer",
    Pair(type="boolean", format=None): "marshmallow.fields:Boolean",
}


class FormatDispatcher(object):
    path_map = TYPE_MAP
    def_map = None  # singleton

    @classmethod
    def load_def_map(cls, path_map):
        return {pair: load_function(path) for pair, path in path_map.items()}

    def __init__(self):
        if self.__class__.def_map is None:
            self.__class__.load_def_map(self.__class__.path_map)

    def dispatch(self, pair):
        return self.path_map.get(pair) or self.path_map.get((pair[0], None))
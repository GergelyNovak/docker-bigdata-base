#!/usr/bin/env python
import os

import sys

import errno
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import subprocess

class Services:
    def __init__(self, consul):
        self.RESERVERD = consul

    def __getattr__(self, item):
        return self.RESERVERD.catalog.service(item)[1]


def template(key, value, consul):
    template = Environment(
        undefined=StrictUndefined,
        variable_start_string="{{",
        variable_end_string="}}"
    ).from_string(value.decode("utf-8"))
    services = Services(consul)
    return template.render({'env': os.environ, 'service': services}).encode("utf-8")


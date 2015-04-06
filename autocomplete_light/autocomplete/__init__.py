from django import VERSION

if VERSION < (1, 9):
    from .shortcuts import *

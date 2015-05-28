import sys
import string
import __builtin__

from Infix import Infix
from Symbol import Symbol
from Variable import Variable
from FSymbol import FSymbol
from LOperator import LOperator
from KB import KB

"""Symbolic global constants, like. 'None', 'NOT_FOUND', etc."""

__all__ = [
    'Symbol','NOT_GIVEN','NOT_FOUND','AND','OR','NOT','IF','IFF','THEN','WHEN','FSymbol','Variable','FWRule','BWRule','unify','kb','rename_variables','rename_copy', 'defvar', 'defvarp', 'internal_types'
]

sys.setrecursionlimit(1000000000)

# Defining variables, functional symbols and logic operators
def defvar(var):
    command = "__builtin__."+var+"=Variable('"+var+"')"
    exec command

def defsym(sym):
    command = "__builtin__."+sym+"=FSymbol('"+sym+"')"
    exec command

def deflop(lop):
    command = "__builtin__."+lop+"=LOperator('"+lop+"')"
    exec command

# checks if a given symbol is already definend

THEN = Infix(lambda x,y:KB.__kb__.make_fc_rule(x,y))
IF = Infix(lambda x,y:KB.__kb__.make_bc_rule(x,y))
#THAT = Infix(lambda x,y:KB.__kb__.make_and_concept(x,y))

NOT_GIVEN   = Symbol("NOT_GIVEN")
NOT_FOUND   = Symbol("NOT_FOUND")

#This function sets up common variable names
#and logic operators and returns a new KB
#possibly to be extended

def init():
    kb=KB()
    # initializing standard variables
    # variables are uppercase letters
    defvar('_')
    for var in string.uppercase:
        defvar(var)
        defvar(var+"1")
        defvar(var+"2")
        defvar(var+"3")
    # initializing built-in logic operators
    # this operators are reserved for the python AI module
    # a variant of the manchester OWL syntax is used for description logic
    defsym("is_a")
    defsym("builtin_type")
    defsym("default_value")
    defsym("has_type")
    defsym("has_range")
    defsym("has_domain")
    defsym("one_of")
    defsym("subclass_of")
    defsym("equivalent_to")
    defsym("disjoint_with")
    deflop("AND")
    deflop("OR")
    deflop("NOT")
    # standard operators of the OWL Manchester Syntax
    deflop("SOME")
    deflop("ONLY")
    deflop("MIN")
    deflop("MAX")
    deflop("EXACTLY")
    deflop("VALUE")
    deflop("IFF")
    deflop("ONLYSAME")
    return(kb)

# Infix builtin operators
__builtin__.IF= IF
__builtin__.THEN= THEN
__builtin__.THAT= THAT

# internal types symbols
defsym("bools")
defsym("strs")
defsym("ints")
defsym("floats")
internal_types = [ints, bools, strs, floats]
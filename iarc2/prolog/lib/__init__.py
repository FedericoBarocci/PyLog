import __builtin__

from structs import Infix
from prolog import KB

IF = Infix(lambda x,y:KB.__kb__.make_bc_rule(x,y))
__builtin__.IF= IF
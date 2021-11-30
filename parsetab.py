
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'FUNC HALT MOV OPERATOR RESISTERcmd : MOV RESISTER RESISTERcmd : FUNC OPERATOR RESISTERcmd : HALT'
    
_lr_action_items = {'MOV':([0,],[2,]),'FUNC':([0,],[3,]),'HALT':([0,],[4,]),'$end':([1,4,7,8,],[0,-3,-1,-2,]),'RESISTER':([2,5,6,],[5,7,8,]),'OPERATOR':([3,],[6,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'cmd':([0,],[1,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> cmd","S'",1,None,None,None),
  ('cmd -> MOV RESISTER RESISTER','cmd',3,'p_mov','asmyacc.py',51),
  ('cmd -> FUNC OPERATOR RESISTER','cmd',3,'p_func','asmyacc.py',56),
  ('cmd -> HALT','cmd',1,'p_halt','asmyacc.py',58),
]

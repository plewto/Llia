# llia.util.undostack
# 2016.04.21

from __future__ import print_function

from llia.constants import MAX_UNDO


class UndoItem(object):

    def __init__(self, action, payload):
        self.action = action
        self.payload = payload

    def __str__(self):
        return str((self.action,self.payload))

        
class _Stack(object):

    def __init__(self, maxdepth=MAX_UNDO):
        self.maxdepth = maxdepth
        self.stack = []

    def clear(self):
        self.stack = []
        
    def push(self, action, payload):
        self.stack.append(UndoItem(action, payload))
        if len(self) > self.maxdepth:
            self.stack = self.stack[1:]

    def pop(self):
        return self.stack.pop()
        
    def __len__(self):
        return len(self.stack)

    def is_empty(self):
        return len(self) == 0

    def top(self):
        if self.is_empty():
            return ""
        else:
            return self.stack[-1].action

    def dump(self, prefix, tab=0):
        pad = " "*4*tab
        pad2 = pad + " "*4
        acc = "%s%s\n" % (pad, prefix)
        for i,item in enumerate(self.stack):
            acc += "%s[%d] %s\n" % (pad2, i, item.action)
        return acc
        

class UndoRedoStack(object):
    """Combined Undo and Redo stacks."""
    
    def __init__(self, maxdepth=MAX_UNDO):
        """Construct new UndoRedoStack instance."""
        self._undo_stack = _Stack(maxdepth)
        self._redo_stack = _Stack(maxdepth)

    def clear(self):
        self._undo_stack.clear()
        self._redo_stack.clear()
        
    def undo_depth(self):
        """Return number of undo actions."""
        return len(self._undo_stack)

    def redo_depth(self):
        """Return number of redo actions."""
        return len(self._redo_stack)

    def push_undo(self, action, payload):
        """
        Push new undo state.
        If stack grows beyond constants.MAX_UNDO, remove most stale item.
        ARGS:
          action  - String, descriptive text
          payload - Data to be restored.
        """
        self._undo_stack.push(action, payload)
        
    def undo_top(self):
        """
        Returns description of next undo.
        If there are no more undos return empty string "".
        """
        return self._undo_stack.top()

    def redo_top(self):
        """
        Returns description of next redo.
        If there are no more redos return empty-string "".
        """
        return self._redo_stack.top()

    def pop_undo(self, state=None):
        """
        Pop the next undo state and place current state on redo stack.
        
        ARGS:
          state - redo state data

        RETURNS:
          an instance of UndoItem

        Raise IndexError if undo stack is empty.
        """
        ta = self._undo_stack.pop()
        if state:
            self._redo_stack.push(ta.action, state)
        return ta
    
    def push_redo(self, action, payload):
        """
        Push new redo state.
        If stack grows beyond constants.MAX_UNDO, remove most stale item.
        ARGS:
          action  - String, descriptive text
          payload - Data to be restored.
        """
        self._redo_stack.push(action, payload)

    
    def pop_redo(self, state=None):
        """
        Pop the next redo state and place current state on undo stack.

        ARGS:
          state - undo state data

        RETURNS:
          an instance of UndoItem

        Raise IndexEror if redo stack is empty.
        """
        ta = self._redo_stack.pop()
        if state:
            self._undo_stack.push(ta.action, state)
        return ta

    def dump(self, tab=0):
        acc = self._undo_stack.dump("UNDO:", tab)
        acc += self._redo_stack.dump("REDO:", tab)
        return acc
        
def test():
    stk = UndoRedoStack(maxdepth=3)
    stk.push("Natural", [0,1,2,3,4])
    stk.push("Primes", [2,3,5,7])
    stk.push("Squares", [0,1,4,9,16])
    stk.push("Triangles", [0,1,3,6,10])
    print(stk.dump())
    print()
    stk = UndoRedoStack(maxdepth=3)
    stk.push("Natural", [0,1,2,3,4])
    stk.push("Primes", [2,3,5,7])
    print(stk.undo_top())
    print(stk.pop_undo(["Alpha", "Beta"]))
    print(stk.dump())
    print(stk.pop_redo())
        

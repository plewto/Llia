/*
 * stack.sc 2015.11.13
 * Defines Stack and Queue classes.
 */
 


SuperStack : Object {
  var stk;

  *new {
    ^super.new.init;
  }

  init {
    stk = List[];
  }

  clear {
    stk.removeAll;
  }

  depth {
    ^stk.size;
  }

  isEmpty {
    ^this.depth == 0;
  }

  pop {|n=nil|
	  if (n == nil,
		  {
			  ^stk.pop;
		  },{
			  stk.remove(n);
			  ^n;
		  });
  }

}

  
/* 
 * FILO Stack 
*/
Stack : SuperStack {

	*new {
		^super.new.init;
	}

	top {
		var n = this.depth;
		^stk.at(n-1);
	}

	push {
		arg obj;
		stk.add(obj);
	}

}


/*
 * FIFO Queue
 */
Queue : SuperStack {

	*new {
	  ^super.new.init;
	}
	
	init {
	  stk = List[];
	}
	
	top {
	  ^stk.at(0);
	}
	
	push {
	  arg obj;
	  stk.addFirst(obj);
	}

}
		

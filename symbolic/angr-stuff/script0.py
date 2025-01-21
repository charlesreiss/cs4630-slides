import resource
resource.setrlimit(resource.RLIMIT_AS, (1024 * 1024 * 1024*19, 1024 * 1024 * 1024* 19))

import angr
import claripy

p = angr.Project("./example0", load_options={'auto_load_libs': False})

foo_addr = p.loader.main_object.get_symbol('foo').rebased_addr
input_a = claripy.BVS('initial_a', 32)
input_b = claripy.BVS('initial_b', 32)
init_state = p.factory.call_state(foo_addr, input_a, input_b)

simgr = p.factory.simulation_manager(init_state)
print("before step:", simgr)
print(f"RIP={simgr.active[0].regs.rip} versus {foo_addr:#x}")
print(f"EAX={simgr.active[0].regs.eax}")
simgr.step()
print("after step:", simgr)
simgr.step()
print("after step:", simgr)
state = simgr.deadended[0]
print("EAX=",state.regs.eax)
state.solver.add(state.regs.eax == 10)
print(state.solver.eval(input_a), state.solver.eval(input_b))
state.solver.add(input_b != 0)
print(state.solver.eval(input_a), state.solver.eval(input_b))


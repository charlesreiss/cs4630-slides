import resource
resource.setrlimit(resource.RLIMIT_AS, (1024 * 1024 * 1024*19, 1024 * 1024 * 1024* 19))

import angr
import claripy

p = angr.Project("./example1", load_options={'auto_load_libs': False})

foo_addr = p.loader.main_object.get_symbol('foo').rebased_addr
INTERESTING_addr = p.loader.main_object.get_symbol('INTERESTING').rebased_addr
input_a = claripy.BVS('initial_a', 32)
input_b = claripy.BVS('initial_b', 32)
init_state = p.factory.call_state(foo_addr, input_a, input_b)

simgr = p.factory.simulation_manager(init_state)
print("at beginning:", simgr)
simgr.explore(find=INTERESTING_addr)
print("after explore:", simgr)
for state in simgr.found:
    found_a = state.solver.eval(input_a)
    found_b = state.solver.eval(input_b)
    print(f'(a, b) = ({found_a}, {found_b})')

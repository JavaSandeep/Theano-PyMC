from theano import compile, gof
from theano.gof import TopoOptimizer
from theano.typed_list.basic import Append, Extend, Insert, Remove, Reverse


@gof.local_optimizer([Append, Extend, Insert, Reverse, Remove], inplace=True)
def typed_list_inplace_opt(fgraph, node):
    if (
        isinstance(node.op, (Append, Extend, Insert, Reverse, Remove))
        and not node.op.inplace
    ):

        new_op = node.op.__class__(inplace=True)
        new_node = new_op(*node.inputs)
        return [new_node]
    return False


compile.optdb.register(
    "typed_list_inplace_opt",
    TopoOptimizer(typed_list_inplace_opt, failure_callback=TopoOptimizer.warn_inplace),
    60,
    "fast_run",
    "inplace",
)

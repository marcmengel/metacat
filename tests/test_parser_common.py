from env import env

from metacat.mql.meta_evaluator import MetaEvaluator
from metacat.mql.mql10 import _Parser, MQLQuery

class mock_file:
    def __init__(self, md):
        self.md = md
    def metadata(self):
        return self.md

def eval_expr(e, md):
    """ evaluate an expression for the given metadata ... """
    f = mock_file(md)
    me = MetaEvaluator()
    pe = MQLQuery.parse(f"files where ( {e} ) ")
    print("repr(pe.Tree.D['query'].__dict__)", repr(pe.Tree.D['query'].__dict__))
    return me( f, pe.Tree.D['query'].Wheres )


def test_exp_1():
    assert( eval_expr("c.n1 == 10", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_2():
    assert( not eval_expr("c.n1 != 10", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_3():
    assert( eval_expr("c.n2 == 20", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_4():
    assert( not eval_expr("c.n2 != 20", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_5():
    assert( eval_expr("c.n1 in (9,10,11)", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_6():
    assert( eval_expr("c.n1 in 9:11", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_5():
    assert( not eval_expr("c.n1 not in (9,10,11)", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_6():
    assert( not eval_expr("c.n1 not in 9:11", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_7():
    assert( eval_expr("c.n1 present", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_8():
    assert( not eval_expr("c.n1 not present", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_9():
    assert( eval_expr("10 in c.n1", {"c.n1": [8,9,10], "c.n2": 20} ) )

def test_exp_10():
    assert( eval_expr("6 not in c.n1", {"c.n1": [8,9,10], "c.n2": 20} ) )


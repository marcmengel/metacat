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
    return me( f, pe.Tree.D['query'].Wheres )

# testing == and != 

def test_exp_1():
    assert( eval_expr("c.n1 == 10", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_2():
    assert( not eval_expr("c.n1 != 10", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_3():
    assert( eval_expr("c.n2 == 20", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_4():
    assert( not eval_expr("c.n2 != 20", {"c.n1": 10, "c.n2": 20} ) )

# testing various "in" combinations

def test_exp_5():
    assert( eval_expr("c.n1 in (9,10,11)", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_6():
    assert( eval_expr("c.n1 in 9:11", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_5():
    assert( not eval_expr("c.n1 not in (9,10,11)", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_6():
    assert( not eval_expr("c.n1 not in 9:11", {"c.n1": 10, "c.n2": 20} ) )

# test present

def test_exp_7():
    assert( eval_expr("c.n1 present", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_8():
    assert( not eval_expr("c.n1 not present", {"c.n1": 10, "c.n2": 20} ) )

# test reverse in

def test_exp_9():
    assert( eval_expr("10 in c.n1", {"c.n1": [8,9,10], "c.n2": 20} ) )

def test_exp_10():
    assert( not eval_expr("6 in c.n1", {"c.n1": [8,9,10], "c.n2": 20} ) )

def test_exp_10_1():
    assert( eval_expr("6 not in c.n1", {"c.n1": [8,9,10], "c.n2": 20} ) )

def test_exp_10_2():
    assert( not eval_expr("6 in c.n1", {"c.n1": [8,9,10], "c.n2": 20} ) )

# test less/greater/equal

def test_exp_11():
    assert( eval_expr("c.n1 <= 10", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_12():
    assert( eval_expr("c.n1 >= 10", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_13():
    assert( eval_expr("c.n1 < 11", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_13():
    assert( eval_expr("c.n1 > 9", {"c.n1": 10, "c.n2": 20} ) )

# test regex match

def test_exp_14():
    assert( eval_expr("c.s1 ~ 'a.*b'", {"c.s1": "xaxyzby", "c.n2": 20} ) )

# test and, or...

def test_exp_20():
    assert( eval_expr("(c.n1 < 11) and (c.n2 < 21)", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_21():
    assert( eval_expr("(c.n1 < 11) or (c.n2 < 10)", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_22():
    assert( eval_expr("(c.n1 < 9) or (c.n2 < 21)", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_23():
    assert( eval_expr("(c.n1 in 8:11) or (c.n2 < 19)", {"c.n1": 10, "c.n2": 20} ) )

def test_exp_23():
    assert( eval_expr("(c.n1 in (8,9,10)) or (c.n2 < 19)", {"c.n1": 10, "c.n2": 20} ) )


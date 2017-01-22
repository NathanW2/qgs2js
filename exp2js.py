from qgis.core import QgsExpression
import re

nodes = []

whenfunctions = []


def gen_func_stubs():
    funcs = QgsExpression.Functions()
    functions = []
    temp = """function %s(values, context) {
    return false;
};
"""
    for func in funcs:
        name = func.name()
        if name.startswith("$"):
            continue
        newfunc = temp % ("fnc_" + name)
        functions.append(newfunc)
    return "\n".join(functions)

def exp2func(exp):
    global whenfunctions
    whenfunctions = []
    js = walkExpression(exp.rootNode(), "Leaftlet")
    temp = """
function eval_expression(feature) { %s
    return %s;
}""" % ("\n".join(whenfunctions), js)
    data = "// QGIS EXP:"
    data += "//" + exp.dump()
    data += "JS Function:"
    data += temp
    return temp


def walkExpression(node, mapLib):
    if node.nodeType() == QgsExpression.ntBinaryOperator:
        jsExp = handle_binary(node, mapLib)
    elif node.nodeType() == QgsExpression.ntUnaryOperator:
        jsExp = handle_unary(node, mapLib)
    elif node.nodeType() == QgsExpression.ntInOperator:
        jsExp = handle_in(node, mapLib)
    elif node.nodeType() == QgsExpression.ntFunction:
        jsExp = handle_function(node, mapLib)
    elif node.nodeType() == QgsExpression.ntLiteral:
        jsExp = handle_literal(node)
    elif node.nodeType() == QgsExpression.ntColumnRef:
        jsExp = handle_columnRef(node, mapLib)
    elif node.nodeType() == QgsExpression.ntCondition:
        jsExp = handle_condition(node,mapLib)
    return jsExp

binary_ops = [
    "||", "&&",
    "==", "!=", "<=", ">=", "<", ">", "~",
    "LIKE", "NOT LIKE", "ILIKE", "NOT ILIKE", "===", "!==",
    "+", "-", "*", "/", "//", "%", "^",
    "+"
]

unary_ops = ["!", "-"]


def handle_condition(node, mapLib):
    global condtioncounts
    subexps = re.findall("WHEN(\s+.*?\s+)THEN(\s+.*?\s+)", node.dump())
    print subexps
    count = 1;
    js = ""
    for sub in subexps:
        when = sub[0].strip()
        then = sub[1].strip()
        print then
        whenpart =  QgsExpression(when)
        thenpart = QgsExpression(then)
        whenjs = walkExpression(whenpart.rootNode(), mapLib)
        thenjs = walkExpression(thenpart.rootNode(), mapLib)
        style = "if" if count == 1 else "else if"
        js += """%s %s {
          return %s
        }
        """ % (style, whenjs, thenjs)
        count += 1
    funcname = "_CASE()"
    temp = "function %s {%s};" % (funcname, js)
    whenfunctions.append(temp)
    return funcname

def handle_binary(node, mapLib):
    op = node.op()
    left = node.opLeft()
    right = node.opRight()
    retLeft = walkExpression(left, mapLib)
    retOp = binary_ops[op]
    retRight = walkExpression(right, mapLib)
    if retOp == "LIKE":
        return "(%s.indexOf(%s) > -1)" % (retLeft[:-1],
                                          re.sub("[_%]", "", retRight))
    elif retOp == "NOT LIKE":
        return "(%s.indexOf(%s) == -1)" % (retLeft[:-1],
                                           re.sub("[_%]", "", retRight))
    elif retOp == "ILIKE":
        return "(%s.toLowerCase().indexOf(%s.toLowerCase()) > -1)" % (
            retLeft[:-1],
            re.sub("[_%]", "", retRight))
    elif retOp == "NOT ILIKE":
        return "(%s.toLowerCase().indexOf(%s.toLowerCase()) == -1)" % (
            retLeft[:-1],
            re.sub("[_%]", "", retRight))
    elif retOp == "~":
        return "/%s/.test(%s)" % (retRight[1:-2], retLeft[:-1])
    elif retOp == "//":
        return "(Math.floor(%s %s %s))" % (retLeft, retOp, retRight)
    else:
        return "(%s %s %s)" % (retLeft, retOp, retRight)


def handle_unary(node, mapLib):
    op = node.op()
    operand = node.operand()
    retOp = unary_ops[op]
    retOperand = walkExpression(operand, mapLib)
    return "%s %s " % (retOp, retOperand)


def handle_in(node, mapLib):
    operand = node.node()
    retOperand = walkExpression(operand, mapLib)
    list = node.list().dump()
    retList = json.dumps(list)
    return "%s.indexOf(%s) > -1 " % (retList, retOperand)


def handle_literal(node):
    val = node.value()
    quote = ""
    if isinstance(val, basestring):
        quote = "'"
    return "%s%s%s" % (quote, unicode(val), quote)


def handle_function(node, mapLib):
    fnIndex = node.fnIndex()
    func = QgsExpression.Functions()[fnIndex]
    args = node.args().list()
    retFunc = (func.name())
    retArgs = []
    for arg in args:
        retArgs.append(walkExpression(arg, mapLib))
    retArgs = ",".join(retArgs)
    return "fnc_%s([%s], feature, context)" % (retFunc, retArgs)


def handle_columnRef(node, mapLib):
    if mapLib == "Leaflet":
        return "feature.properties['%s'] " % node.name()
    else:
        return "feature.get('%s') " % node.name()

if __name__ == "__main__":
    # exp = QgsExpression("1 = 1 AND 'Hello' LIKE '%WORLD%' OR \"ColA\" != \"COLB\"")
    # exp2func(exp)
    # exp = QgsExpression("@var1 + @var2")
    # exp2func(exp)
    # exp = QgsExpression("CASE WHEN 1 = 1 THEN 2 END OR 1 = 2")
    # exp2func(exp)
    # exp = QgsExpression("CASE WHEN 1 = 1 THEN 2 WHEN 1 = 2 THEN 2 + 2 ELSE 1 END")
    # exp2func(exp)
    # exp = QgsExpression("CASE WHEN 1 = 1 THEN 1 WHEN 1 = 2 THEN 2 ELSE 1 END OR 1 + 2 = 3")
    # exp2func(exp)
    with open("qgsfunctions.js", "w") as f:
        # Write out the functions first.
        funcs = gen_func_stubs()
        f.write(funcs)

    with open("qgsexpression.js", "w") as f:
        # Write out the expression function logic
        exp = QgsExpression("@myvar + format('some string %1 % 2', 'Hello', 'World')")
        data = exp2func(exp)
        f.write(data)

import check_dimensions

# calc.DEFAULT_FUNCTIONS = {
#     key: dimensionless_func(func)
#     for key, func in calc.DEFAULT_FUNCTIONS.iteritems()
# }
# calc.DEFAULT_FUNCTIONS['sqrt'] = lambda x: pow(x,0.5)
#
# L = Quantity(1,{"L":1})
# T = Quantity(1,{"T":1})
# M = Quantity(1,{"M":1})
#
# vars_dict_units = {
#     'h': random.uniform(2,5)*L,
#     'T': random.uniform(2,5)*T,
#     'r': random.uniform(2,5)*L,
#     'v': random.uniform(2,5)*L/T,
#     'g': random.uniform(2,5)*L/T**2
# }
# funcs_dict = {}
# expr1 = "sqrt(h^2/T^2 + v^2) + v^3/(g*h)*sin(h/r)"
# expr2 = "v^(h/r)"
#
# vars_dict = vars_dict_units
# z = calc.evaluator(vars_dict, funcs_dict, expr2)
#
# answer = "sqrt(2*h/g)*v_0"
# samples = "v_0,g,h@ 1,1,1:2,2,2 #3"

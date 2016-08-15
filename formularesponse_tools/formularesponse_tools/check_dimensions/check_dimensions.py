from collections import defaultdict
import numbers
import random
from .. import calc
from .. import functions
from feedback_messages import DEFAULT_MESSAGES
from quantities import Dimension, Quantity, DimensionMismatchError, DimensionArgumentError, IndeterminateDimensionError


def dimensionless_func(func):
    """Alter a function so that it accepts and returns dimensionless quantities.
    
    func(number) --> number
    decorated_func(quantity) --> quantity, where both input and output are dimensionless
    """
    def decorated_func(arg):
        if isinstance(arg, Quantity):
            if not arg.is_dimensionless():
                raise DimensionArgumentError(func.__name__)
            arg = arg.value
        return Quantity(func(arg), {})
    return decorated_func

dim_funcs = {
    key: dimensionless_func(func)
    for key, func in calc.DEFAULT_FUNCTIONS.iteritems()
}
dim_funcs['sqrt'] = lambda x: pow(x,0.5)

class DimensionsChecker(object):
    """docstring for DimensionsChecker"""
    def __init__(self, expected, samples, dims_dict, input_idx=0, case_sensitive=True, feedback_messages = {}, show_dims=True):
        self.expected = expected
        self.samples = samples
        self.dims_dict = dims_dict
        self.input_idx = input_idx
        self.case_sensitive = case_sensitive
        self.feedback_messages = DEFAULT_MESSAGES
        self.feedback_messages.update(feedback_messages)
        self.show_dims = show_dims
    def tupleize_answers(self, answer, var_dict_list):
        """
        Takes in an answer and a list of dictionaries mapping variables to values.
        Each dictionary represents a test case for the answer.
        Returns a tuple of formula evaluation results.
        """

        out = []
        for var_dict in var_dict_list:
            out.append(calc.evaluator(
                var_dict,
                dim_funcs,
                answer,
                case_sensitive=self.case_sensitive,
            ))
        return out

    def randomize_variables(self, samples):
            """
            Returns a list of dictionaries mapping variables to random values in range,
            as expected by tupleize_answers.
            
            NOTES:
                - borrowed from https://github.com/edx/edx-platform/blob/master/common/lib/capa/capa/responsetypes.py
                - Modified to add dimensions for each variable.
            """
            variables = samples.split('@')[0].split(',')
            numsamples = int(samples.split('@')[1].split('#')[1])
            sranges = zip(*map(lambda x: map(float, x.split(",")),
                               samples.split('@')[1].split('#')[0].split(':')))
            ranges = dict(zip(variables, sranges))

            out = []
            for BLANK in range(numsamples):
                var_dict = {}
                # ranges give numerical ranges for testing
                for var in ranges:
                    value = random.uniform(*ranges[var])
                    var_dict[str(var)] = value * Quantity(1, self.dims_dict[str(var)])
                out.append(var_dict)
            return out
    def check_dims_same(self, expected, given, samples):
        """
        Given an expected answer string and a given (student) answer string, check that they have the same dimensions.
        """
        var_dict_list = self.randomize_variables(samples)
        student_result = self.tupleize_answers(given, var_dict_list)
        instructor_result = self.tupleize_answers(expected, var_dict_list)

        correct = all( student.dims == instructor.dims
                      for student, instructor in zip(student_result, instructor_result))
        if correct:
            return 'correct'
        else:
            return 'incorrect'
    def get_dimensions_value(self, given, samples):
        """
        Given an answer string, evaluate it and return dimensions. 
        If dimensions can't be determined, raise IndeterminateDimensionError.
        """
        var_dict_list = self.randomize_variables(samples)
        evaluations = self.tupleize_answers(given, var_dict_list)
        def same_dims(q1, q2):
            if q1.dims == q2.dims:
                return q1
            else:
                raise IndeterminateDimensionError
        
        dims = reduce(same_dims, evaluations).dims
        return dims
    def get_hint_msg(self, expected, given, samples):
        msg = ""
        try:
            dims_ok = self.check_dims_same(self.expected, given, self.samples )
            msg = self.feedback_messages[dims_ok]
        except DimensionMismatchError:
            msg = self.feedback_messages['add_error']
        except DimensionArgumentError as e:
            msg = self.feedback_messages['arg_error'].format(func=e[0])
        
        try:
            dims = self.get_dimensions_value(given, self.samples)
        except (IndeterminateDimensionError, DimensionMismatchError, DimensionArgumentError):
            dims = ""
        
        if dims and self.show_dims:
            msg += self.feedback_messages['dims'].format(dims=dims)
        
        return msg

    def raw_hint_fn(self, answer_ids, student_answers, new_cmap, old_cmap):
        input_id = answer_ids[self.input_idx]
        given = str(student_answers[input_id])
        msg = self.get_hint_msg(self.expected, given, self.samples)
        new_cmap.set_property(input_id,"msg",msg)
        return
    def hint_fn(self, answer_ids, student_answers, new_cmap, old_cmap):
        try:
            self.raw_hint_fn(answer_ids, student_answers, new_cmap, old_cmap)
        except Exception:
            pass
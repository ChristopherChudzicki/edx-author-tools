# formularesponse_tools
Contents:

1. `check_dimensions`, a python module that generates a hint function for checking the dimensions of submissions to `formularesponse` problems.

## check_dimensions
This python module inclues a `DimensionsChecker` object that generates hint functions used to check the dimensions of student submissions to formularesponse problems and provide feedback messages based on submission dimensions. See `formularesponse_tools_demo_check_dimensions.xml` for a demonstration.

Basically, this module uses the standard edX `formularesponse` grading function to numerically sample student submissions, except rather than plugging in pure numbers we plug in special python `Quantity` objects that have dimensions as well as values. Then a hint function is generated that provides feedback messages to the student. Feedback messages are specified through a dictionary `feedback_messages` (with defaults) whose keys are:

    1. `correct`: A message to display when the submission has correct dimensions.
    2. `incorrect`: A message to display when the submission has incorrect dimensions.
    3. `add_error`: A message to display when the submission tries to add two quantities with different dimennsions.
    4. `arg_error`: A message to display when the submission contains a functions (e.g., `sin(...)`) whose argument has dimensions but should not.
    5. `dims`: A message to display **in addition to the correct/incorrect message** that shows the student the dimensions of their input.
    6. `indeterminate`: A message to display if the dimensions of the submission cannot be determined. (Indetermine dimensions arise only when quantities are raised to dimensionless but variable powers, e.g., x^(v/v_0).)

Default messages can be customized in `formularesponse_tools/check_dimensions/feedback_messages.py`.

## Future Add-ons
As the name suggests, hint functions can be used to provide feedback messages. But they can also be used to grade student submissions. It might be useful to construct hint function generators for formularesponse problems that:

1. allow multiple different correct answers to a `formularesponse` problem
2. plug in complex numbers (e.g., to enfore `a_conj * a = abs(a^2)` in quantum mechanics courses)
3. check if a student submission has correct limits
4. check if a student submission is off by a scale factor
5. check if a vector expression is valid (e.g., 8.01 uses variables ihat, jhat, khat; students often forgot the ihat, and we could have an automatic message for this.)
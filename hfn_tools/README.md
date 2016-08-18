# hfn_tools
Helper tools to make hint functions for edX problems. Currentely contains only one helper:

1. `pretty`, a decorator that formats hint function messages. 

##The Pretty Decorator

For the most part, `hfn_tools.pretty` works just like `cfn_tools.pretty`. Two notes:

- Hint functions can supply feedback messages through either the `hint` or `msg` property of a `correct_map`. Currently, `hint_fn.pretty` only prettyfies messages supplied through `msg` and **not** `hint`.
- Currently no support for `correct_map`'s `overall_message` property, which I can't get to work.
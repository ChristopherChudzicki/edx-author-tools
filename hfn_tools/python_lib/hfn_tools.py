def pretty(original_function=None,settings={}):
    default_settings = {
        'fontsize':110,
        'correct' : {
            'label': 'Correct',
            'color': "#166e36"
        },
        'partially-correct' : {
            'label': 'Partially Correct',
            'color': "#166e36"
        },
        'incorrect' : {
            'label': 'Incorrect',
            'color': "#b20610"
        }
    }
    for key in settings.keys():
        try:
            default_settings[key].update(settings[key])
        except AttributeError:
            default_settings[key] = settings[key]
    settings = default_settings
    def _decorate(hfn):
        def pretty_hfn(answer_ids, student_answers, new_cmap, old_cmap):
            # First, run the original hint function
            hfn(answer_ids, student_answers, new_cmap, old_cmap)
            # Now make the cmap messages pretty
            for answer_id in answer_ids:
                # Get correctness and unstyled message
                correctness = new_cmap.get_correctness(answer_id)
                unstyled_msg = new_cmap.get_msg(answer_id)
                # If message is empty, don't do anything
                if unstyled_msg == "":
                    continue
                # Get style based on correctness
                style = settings[correctness]
                msg_template = '''
                    <span style='font-size:{fontsize}%;color:{color}'>
                        <span style='font-weight:bold'>{label}:</span>
                        {msg}
                    </span>'''
                msg_template = ' '.join(msg_template.split())
                styled_msg = msg_template.format(msg=unstyled_msg, color=style['color'], label=style['label'], fontsize=settings['fontsize'])
                new_cmap.set_property(answer_id, 'msg', styled_msg)
            return None
    
        return pretty_hfn
   
    if original_function:
        return _decorate(original_function)
    
    return _decorate 
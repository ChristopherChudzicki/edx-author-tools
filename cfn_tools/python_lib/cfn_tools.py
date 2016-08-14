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
    def _decorate(cfn):
        def pretty_dict(gradeDict):
            '''Return a prettyfied gradeDict
        
            Args:
                gradeDict: {'ok':...,'msg':...} may have additional keys such as 'grade_decimal'
            '''
            ok = gradeDict['ok']
            msg = gradeDict['msg']
            #if message is empty, don't do anything:
            if msg == "":
                return gradeDict
            elif 'partial' in str(ok).lower():
                correctness = 'partially-correct'
            elif ok==True:
                correctness = 'correct'
            else:
                correctness = 'incorrect'
            style = settings[correctness]
            gradeDict['msg'] = '''
                <span style='font-size:{fontsize}%;color:{color}'>
                    <span style='font-weight:bold'>{label}:</span>
                    {msg}
                </span>
                '''.format(color=style['color'],label=style['label'],msg=msg,fontsize=settings['fontsize'])
            return gradeDict    
    
        def pretty_multipart_cfn(cfn_val):
            '''Returns a prettyfied multipart checkfunction value
        
            Args:
                cfn_val: {'input_list': [{'ok':...},{'ok':...}...] } may have additional keys such as 'overall_message'
            '''
            old_input_list = cfn_val['input_list']
            new_input_list = []
            for gradeDict in old_input_list:
                try:
                    pretty_dict(gradeDict)
                except:
                    pass
                new_input_list.append( gradeDict )
            cfn_val['input_list'] = new_input_list
            if 'overall_message' in cfn_val.keys():
                if cfn_val['overall_message'] != "":
                    cfn_val['overall_message'] = '''
                        <span style='font-size:{fontsize}%'>
                        <span style='font-weight:bold'>Overall Feedback:</span>
                        {msg}
                        </span>
                        '''.strip().format(fontsize=settings['fontsize'],msg=cfn_val['overall_message'])
        
            return cfn_val
            
        def pretty_cfn(expect,answer):
            cfn_val = cfn(expect,answer)
            #This takes care all cfn (single- or multi-part) that return a dict
            
            #if a multipart cfn, prettify each part
            #Every multipart cfn must have 'input_list' key
            if 'input_list' in cfn_val.keys(): 
                cfn_val = pretty_multipart_cfn(cfn_val)
            #if cfn_val does not have an 'input_list' key, then it is a single-
            else:
                try:
                    cfn_val = pretty_dict(cfn_val)
                except:
                    pass

            return cfn_val
    
        return pretty_cfn
   
    if original_function:
        return _decorate(original_function)
    
    return _decorate 

def debugger(expect,answer):
    '''
    A simple checkfunction for customresponse problems that prints the input to each inputfield.
    '''
    #Multi-input customresponse answer is a list, single-input return unicode
    #Make sure answer is a list
    if not isinstance(answer,list):
        answer = [answer,]
        
    #Now display each part of the list
    part_template = "Python sees: <pre><span style='font-size:16px'>{part}</span></pre> of type <code>{pytype}</code>"
    input_list = [{"ok":True,"msg":part_template.format(part=part, pytype=type(part).__name__)} for part in answer]
    
    return {"overall_message":"Overall Message","input_list":input_list}
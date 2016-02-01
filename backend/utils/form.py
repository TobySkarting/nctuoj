from dateutil import parser
from datetime import datetime
def form_validation(form, schema):
    '''
    schema:
        [{
            ### require
            'name': <str> # +<str> means require, default is optional
            'type': <class>
            ### optional
            'non_empty': <bool> # for str, list
            'except': <list>
            'range': <tuple> # t[0] <= value <= t[1]
            'len_range': <tuple> # t[0] <= len(value) <= t[1]
            'check_dict': <dict> # for dict
            ...
        }]
    int
    str
    list
    set
    dict
    datetime
    '''
    for item in schema:
        require = True if item['name'][0] == '+' else False
        name = item['name'] = item['name'][1:] if require else item['name']

        ### check require
        if require and name not in form:
            return '%s not in form' % name

        if name in form:
            ### check value type
            if 'type' in item:
                if not isinstance(form[name], item['type']):
                    if item['type'] == datetime:
                        try: form[name] = parser.parse(form[name])
                        except Exception as e: return e
                    else:
                        try: form[name] = item['type'](form[name])
                        except Exception as e: return e

            ## check non_empty
            if 'non_empty' in item and item['non_empty']:
                if form[name] == item['type']():
                    return 'value of %s: "%s" should not be empty value' % (name, str(form[name]))

            ### check except
            if 'except' in item:
                if form[name] in item['except']:
                    return 'value of %s: "%s" in except list' % (name, str(form[name]))
            
            ### check range
            if 'range' in item:
                if not (item['range'][0] <= form[name] <= item['range'][1]):
                    return 'value of %s: "%s" not in range %s' % (name, str(form[name]), str(item['range']))

            ### check len_range
            if 'len_range' in item:
                if not (item['len_range'][0] <= len(form[name]) <= item['len_range'][1]):
                    return 'value of %s: "%s" not in len_range %s' % (name, str(form[name]), str(item['len_range']))

            ### chech check_dict
            if 'check_dict' in item:
                err = form_validation(form[name], item['check_dict'])
                if err: return err

    return None

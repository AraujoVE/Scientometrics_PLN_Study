import re
'''
Created to replace the values of a dictionary in a string
'''

def reReplaceDict(dictVal,text):
    formatted_parameters = dict((re.escape(k), v) for k, v in dictVal.items())
    pattern = re.compile("|".join(formatted_parameters.keys()))
    return re.sub(pattern, lambda m: formatted_parameters[re.escape(m.group())], text)
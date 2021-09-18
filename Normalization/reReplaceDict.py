import re

def reReplaceDict(dictVal,text):
    formatted_parameters = dict((re.escape(k), v) for k, v in dictVal.items())
    pattern = re.compile("|".join(formatted_parameters.keys()))
    return re.sub(pattern, lambda m: formatted_parameters[re.escape(m.group())], text)
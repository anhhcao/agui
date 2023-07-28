from re import match

# parses the athinput file and returns a dictionary
def parse(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    data = {}
    info = {}
    prefix = ''
    # looking for name and abstract
    # assuming name and abstract lines have no comments in them
    for line in lines:
        # this regex matches the section line:
        # <[string]>
        m = match('^\s*<(.+)>.*', line)
        if m:
            prefix = m.group(1).strip()
            continue
        # this regex matches strings of the form:
        # [string] = [string with spaces] # comment
        m = match('^([^#]+)\s*=\s*([^#]+).*', line)
        if m:
            # strip the leading and trailing whitespace
            # dictionary entry is a list
            name = m.group(1).strip()
            if prefix == 'comment':
                info[name] = m.group(2).strip()
            else:
                data[f'{prefix}_{name}'] = m.group(2).strip()
    return data, info

# parse but with special formatting
def parse_special(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    data = {}
    info = {}
    prefix = ''
    # looking for name and abstract
    # assuming name and abstract lines have no comments in them
    for line in lines:
        # this regex matches the section line:
        # <[string]>
        m = match('^\s*<(.+)>.*', line)
        if m:
            prefix = m.group(1)
            continue
        # this regex matches strings of the form:
        # [string] = [string with spaces] # comment #> [string] [string]
        m = match('^([^#]+)\s*=\s*([^#]+).*#>\s+([^\s]+)(\s+.+|\s*)$', line)
        if m:
            # strip the leading and trailing whitespace
            # dictionary entry is a list
            data[f'{prefix}_{m.group(1)}'.strip()] = [
                m.group(2).strip(), 
                m.group(3).strip(), 
                m.group(4).strip()
            ]
            continue
        # this regex matches the name / abstract
        m = match('^([^#]+)\s*=\s*([^#]+).*$', line)
        if m:
            info[m.group(1).strip()] = m.group(2).strip()
    return data, info
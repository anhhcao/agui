from re import match

# ^\s*((?:set)\s+)?([^#]+)\s*=([^#]+)(#.*)?#>\s+([^\s]+)(.*=[^\s]*)?(.+)?$
def parse_generic(filename):

    #lines = file.readlines()
    recognized = ['.sh', '.csh', '.py', '.athinput'] # recognized filetypes
    file = open(filename, 'r')
    data = {} # data from the file
    info = {} # info about the file (if athinput, then from the comment block usually)
    type = '' # the type of the file (sh, csh, etc.)
    block = '' # keeps track of the current block (athinput files only)
    
    # check if filename has an extension
    m = match('^(athinput\.)?.+(\..+)$', filename)
    if m:
        ext = m.group(2)
        if m.group(1): # currently athinput.* is the only prefix filetype
            type = 'athinput'
        elif ext in recognized:
            type = ext[1:] # remove the dot
        else:
            print('File type not recognized, trying to determine from file content')

    # file.readlines() is only called once (i think)
    for line in file.readlines():

        # check for block line
        m = match('^\s*<(.+)>.*', line)
        if m:
            block = m.group(1).strip()
            if not type:
                print('File type deduced to be athinput')
                type = 'athinput'
            continue

        # group 1 -> either 'set' or empty; can be used to determine if csh or not
        # group 2 -> variable name
        # group 3 -> variable value
        # group 4 -> either help info or empty
        # group 5 -> GUI type
        # group 6 -> either old csh (repeated) name=value or empty; can be ignored
        # group 7 -> GUI params
        m = match('^\s*(set\s+)?([^#]+)\s*=([^#]+)(#.*)?#>\s+([^\s]+)(.*=[^\s]*)?(.+)?$', line)
        if m:
            
            # attempt to deduce type if not already known
            if not type:
                # if the set keyword is used, then its a csh file
                if m.group(1):
                    print('File type deduced to be csh')
                    type = 'csh'
                else:
                    # beware
                    # no quotes => sh but not the other way around since we can still have quotes in shell scripts
                    value = m.group(3).strip()
                    if value != 'True' and value != 'False' and not value.isdigit() and not match('^\'.*\'|\".*\"$', value):
                        print('File type deduced to be sh')
                        type = 'sh'
                # else still undetermined
                # impossible to deduce python code?
            
            # process data
            name = m.group(2).strip()
            if block == 'comment': # only expect this part to run for athinput files
                info[name] = m.group(2).strip()
            else:
                help = m.group(4)
                data[f'{block}/{name}'] = {
                    'value': m.group(3).strip(),
                    'help': '' if not help else help.strip(),
                    'gtype': m.group(5).strip(),
                    'gparams': m.group(7).strip()
                }
    
    # default to sh if a type was not deduced
    if not type:
        print('Unable to deduce file type from content, defaulting to sh')
        type = 'sh'

    # for athinput files, info should be empty
    return data, info, type

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
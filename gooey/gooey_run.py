from gooey import Gooey, GooeyParser
from sys import argv
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

@Gooey(program_name='AGOOEY')
def main():

    # arity checking, same old
    if len(argv) != 2:
        print('Arity error')
        exit()

    data, info = parse(argv[1])
    name = info['problem']
    reference = info['reference']
    if not reference: # empty strings are falsy
        reference = 'N/A'

    parser = GooeyParser(description=f'Problem: {name}\nReference: {reference}')

    keys = data.keys()
    for k in keys:
        parser.add_argument(
            k, # this is the name to acces the element value after parsing is complete
            metavar=k, # display name for widget
            #help='description' # description for widget
            default=data[k]
        )

    args = parser.parse_args()
    # output
    # using command line args is an issue
    # arity error on start (in gui)
    # use file widget instead?

# need to have a main?
if __name__ == '__main__':
    main()
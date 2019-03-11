import re


regex = r"(\[\w*\]+)(?:\s*)+"

test_str = '"Area   es "[a]"" " + "tostring([area2])"'

matches = re.findall(regex, test_str, re.IGNORECASE)
print(matches)
"""

matchNum =expression 0
for match in matches:
    matchNum = matchNum + 1

    print ("Match {matchNum} was found at : {match}".format(matchNum = matchNum, \
        match = match.group()))

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1

        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

        """
a = ['a']

a.extend(test_str.split(' '))
print(a)
commands = []
with open("Script0.txt",'r') as script:
    commands = script.readlines()

"""
    convert each command to be a list
"""
for i in range(len(commands)) :
    commands[i] = commands[i].split()
    for j in commands[i]:
        if ',' in j :
            temp = j.split(',')
            commands[i].remove(j)
            for k in temp:
                commands[i].append(k)

""" 
    Convert each command to HEX
"""
HEXlist = []
temp = ""
OPcode = {"inc_lcd":"01","dec_lcd":"02","rra_lcd":"03","set_delay":"04","clear_lcd":"05",
          "servo_deg":"06", "servo_scan":"07","sleep":"08"}

for command in commands:
    temp = OPcode[command[0]]
    for param in command[1:] :
        temp = "".join([temp,format(int(param), '02x')])
    HEXlist.append(temp)

print('\n'.join(HEXlist))


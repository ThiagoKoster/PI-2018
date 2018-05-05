
# For Test Purposes
# comment all the lines inside main.py that have debug written and save in a new file named main_debug.py
fileLines = open('main.py', 'r').read().splitlines() # put each line of the file in an list of strings
file = open("main_debug.py", "w")
for i in range( len(fileLines)):
    lineString = fileLines[i]
    if 'DEBUG' in fileLines[i]:
        file.write('#'+lineString+'\n')
    else:
        file.write(lineString+'\n')
file.close()




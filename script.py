import subprocess

execute_java = "python player_white.py"
execute_python = "python player_black.py"

pl = 'BLACK'
ai = 'WHITE'
curr = pl

for i in range(1,240):
    if curr==ai:
        curr = pl
        ex_ = subprocess.call(execute_java, shell=True)
        print(ex_)
        #this expects the input to be modified by the executing program itself.
        #the input is now modified with the move executed by the previous program running
    else:
        curr = ai
        subprocess.call(execute_python, shell=True)
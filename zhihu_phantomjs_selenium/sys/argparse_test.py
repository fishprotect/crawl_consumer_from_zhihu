#
import argparse
import os
par = argparse.ArgumentParser()
par.add_argument('echo')
args = par.parse_args()
s = args.echo
cmd = s.split(',')
script = cmd[0]
url = cmd[1]
try:
    commandline = 'python3 '+script+'.py '+'-url '+url
    os.system(commandline)
except:
    # 开始检查错误
    print(args.echo)
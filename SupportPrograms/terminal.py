# Perform terminal commands via ssh
# Regards, Sam Macharia

import os,sys

#==============================================
try:
    os.system("gnome-terminal -e 'python3 PC6.py' ")
except (Exception, e):
    print("[!] 'PC6' has an error.")
    pass
#==============================================
try:
    os.system("gnome-terminal -e 'python3 PC7.py' ")
except (Exception, e):
    print("[!] 'PC7.py' has an error.")
    pass
#==============================================


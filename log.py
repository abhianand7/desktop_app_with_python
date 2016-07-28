import sys


# this method will be replaced by the logging method of inbuilt python
def logs(errors):                           # under development
    saveout = sys.stdout
    try:
        fsock = open('logs.txt', 'a')
    except IOError:
        fsock = open('logs.txt', 'w')
    sys.stdout = fsock
    print errors
    sys.stdout = saveout
    fsock.close()
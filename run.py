import pexpect


# method for running native linux commands
def run_cmd(cmd):                           # under development
    pexpect.run(cmd)
    child = pexpect.spawn(cmd)
    child.expect('')
    child.sendline('')
    return None
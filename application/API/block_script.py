import pexpect
import sys

id = sys.argv[1]

try:
    evillimiter = pexpect.spawn('sudo evillimiter --flush', echo=False)
    evillimiter.timeout = 3600
    #evillimiter.expect('evillimiter')
    evillimiter.sendline("scan")
    evillimiter.sendline("hosts")
    evillimiter.sendline("block " + str(id))
    evillimiter.expect(pexpect.EOF)

except pexpect.exceptions.TIMEOUT:
    print('timeout')

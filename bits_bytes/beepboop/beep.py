import sys
import termios
import tty
import time

def beepboop():
    fd = sys.stdin.fileno()
    old_attrs = termios.tcgetattr(fd)
    try:
        tty.setraw(fd) # calls termios.tcsetattr
        inp = sys.stdin.read(1)
        while ord(inp) != 3:
            # Loop until CTRL+C detected
            if inp.isdigit():
                for _ in range(int(inp)):
                    print(chr(7)) # ascii bell   
                    # time.sleep(.5)
            inp = sys.stdin.read(1)
    finally:
        # reset attributes
        termios.tcsetattr(fd, termios.TCSADRAIN, old_attrs)

if __name__ == '__main__':
    beepboop()


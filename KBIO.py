from msvcrt import getch, kbhit

numberKeys = [
    b"0", b"1", b"2", b"3", b"4", b"5", b"6", b"7", b"8", b"9"
    ]

def numberInput(mi=0, ma=9, brk=b"\r"):
    while True:
        key = getch()
        
        if key == brk:
            break
        
        try:
            index = numberKeys.index(key)
            if index >= mi and index <= ma:
                return index
            
        except ValueError:
            continue

    return -1

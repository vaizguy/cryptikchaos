'''
Created on Oct 23, 2013

Contains methods that obscure plaintext.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.4

import hashlib

def shuffler(string, key=None, iterations=1):  
    """
    Scramble plaintext readability.
    """  

    if key:
        salt = hashlib.sha512(string + key).hexdigest()
        string = string + salt

    for _ in xrange(1, iterations):
        shuffled_string = []
        even_chars = []
        odd_chars  = []

        for odd_pos in [ x for x in xrange (0, len(string)) if x%2!=0]:
            odd_chars.append(string[odd_pos])
        
        for even_pos in [ x for x in xrange (0, len(string)) if x%2==0]:
            even_chars.insert(0, string[even_pos])

        shuffled_string = odd_chars + even_chars 

        string = "".join(shuffled_string)

    return string

def unshuffler(shuffled_string, key=None, iterations=1):
    """
    Unscramble scrambled string.
    """

    wlen = len(shuffled_string)

    string = [None]*wlen

    for _ in xrange(1, iterations):
        odd_segment = shuffled_string[0:wlen/2]
        even_segment = shuffled_string[wlen/2:wlen]

        odd_pos = 1
        for c in odd_segment:
            string[odd_pos] = c
            odd_pos += 2

        even_pos = 0
        for c in even_segment[::-1]:
            string[even_pos] = c
            even_pos += 2

        shuffled_string = ''.join(string)

    string = shuffled_string

    if key:
        if string[-128:] == hashlib.sha512(string[:-128]+key).hexdigest():
            return string[:-128]
        else:
            return ""
    else:
        return string
    
if __name__ == "__main__":
    import random, string
    
    # Random string of 64 bytes
    string = "".join([random.choice(string.ascii_uppercase + string.digits) for x in range(128)])
    print "Original String: {}".format(string)
    
    # Shuffle string
    shuff = shuffler(string, iterations=1000)
    print "Scrambled : {} length : {}".format(shuff, len(shuff))
    
    # Unshuffle shuffled string
    unshuff = unshuffler(shuff, iterations=1000)
    print "Unscrambled: {} length : {}".format(unshuff, len(unshuff))
    
    # Match unshuffled string with original
    if unshuff == string:
        print "Shuffler test pass!"
    else:
        print "Shuffler test fail!"
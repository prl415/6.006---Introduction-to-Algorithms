#!/usr/bin/env python2.7

import unittest
import sys
from dnaseqlib import *

### Utility classes ###

# Produces hash values for a rolling sequence.
class RollingHash:
    def __init__(self, s):
        self.HASH_BASE = 7
        self.seqlen = len(s)
        n = self.seqlen - 1
        h = 0
        for c in s:
            h += ord(c) * (self.HASH_BASE ** n)
            n -= 1
        self.curhash = h

    # Returns the current hash value.
    def current_hash(self):
        return self.curhash

    # Updates the hash by removing previtm and adding nextitm.  Returns the updated
    # hash value.
    def slide(self, previtm, nextitm):
        self.curhash = (self.curhash * self.HASH_BASE) + ord(nextitm)
        self.curhash -= ord(previtm) * (self.HASH_BASE ** self.seqlen)
        return self.curhash

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.multi_dict = dict()
        
        for pair in pairs:
            self.put(pair[1], pair[2])
            
    def get_table(self):
        return self.multi_dict
            
    # Associates the value v with the key k.
    def put(self, k, v):
        # self.multi_dict.setdefault(k, []).append(v)
        table = self.get_table()
        
        if k not in table:
            table[k] = [v]
        else:
            table[k].append(v)
            
    def is_in(self, k):
        table = self.get_table()
        return k in table
        
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        # return self.multi_dict.get(k, [])
        table = self.get_table()
        
        try:
            return table[k]
        except:
            return []

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    seq_k = kfasta.subsequences(kfasta.FastaSequence(seq), k)
    s = next(seq_k)
    rol_hash = RollingHash(s)
    current_hash_val = rol_hash.current_hash()
    yield (current_hash_val, s, 0)
    prev_item = s[0]
    i = 1
    
    try:
        while True:
            s = next(seq_k)
            next_item = s[-1]
            current_hash_val = rol_hash.slide(prev_item, next_item)
            yield (current_hash_val, s, i)
            prev_item = s[0]
            i += 1
            
    except StopIteration:
        return
    
# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    seq_k = subsequenceHashes(seq, k)
    # hash_table = Multidict()
    # not_found = True
    try:
        while True:
            (hash_val, seq, pos) = next(seq_k)
            
            if pos % m == 0:
                yield(hash_val, seq, pos)
                
            # if not hash_table.is_in(hash_val) and not_found:
            #     hash_table.put(hash_val, (seq, pos))
            #     not_found = False
                
    except:
        return
    
def intervalSubsequenceHashes2(seq, k, m):
    seq_k = kfasta.subsequences(kfasta.FastaSequence(seq), k)
    s = next(seq_k)
    rol_hash = RollingHash(s)
    current_hash_val = rol_hash.current_hash()
    yield (current_hash_val, s, 0)
    i = 1
    
    try:
        while True:
            s = next(seq_k)
            
            if i % m == 0:
                rol_hash = RollingHash(s)
                current_hash_val = rol_hash.current_hash()
                yield (current_hash_val, s, i)
                
            i += 1
            
    except StopIteration:
        return


# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    
    hash_table = Multidict()
    for hash_val, subseq, subseq_pos in intervalSubsequenceHashes2(a, k, m):
        hash_table.put(hash_val, (subseq, subseq_pos))
        
    try:
        for hash_val, subseq, subseq_pos in intervalSubsequenceHashes2(b, k, m):
            for _, index in hash_table.get(hash_val):
                yield(index, subseq_pos)
        
    except StopIteration:
        return
        

if __name__ == '__main__':
    # if len(sys.argv) != 4:
    #     print('Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0]))
    #     sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, 'output3.png', (1500,1500), 'data/fpaternal0.fa', 'data/fpaternal0.fa', 8, 1000)

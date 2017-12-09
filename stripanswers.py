#!/usr/local/bin/python3
import unittest
"""

 Strip "answers" from a .pptx.  Original code is from 
     http://andrewfong.com/blog/2011/10/04/remove-notes-from-powerpoint-pptx, for removing notes.
 It looks like adding "@a" at the end of a line will generate
    <a:p> ... <a:t>@a</a:t> ... <a:p>

Example line:
    A<a:p><a:r><a:rPr lang="en-US" sz="2400" dirty="0" /><a:t>   </a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t>(</a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t>700 </a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t>+/-) </a:t></a:r><a:r><a:rPr lang="en-US" sz="500" baseline="-25000" dirty="0" smtClean="0" /><a:t>@a</a:t></a:r><a:endParaRPr lang="en-US" sz="500" baseline="-25000" dirty="0" /></a:p>B

    https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
    
"""
#
#  Usage: ~/tbin/drop_pptx_here.py haskell.pptx
#   Creates haskell-noans.pptx
#
import zipfile
import os, sys
import re, tempfile

def rm_txt(str):
    return re.sub(r'<p:txBody>.*</p:txBody>', '<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr/></a:p></p:txBody>', str)

def main(fn):
    print("Processing %s -- please wait." % fn)
    if fn[-5:] != '.pptx':
        raise RuntimeError("Files need to be .pptx files.")
    old = zipfile.ZipFile(fn, "r")
    fn2 = fn.replace(".pptx","-noans.pptx")
    new = zipfile.ZipFile(fn2, "w")
    for item in old.infolist():
        data = old.read(item.filename)
        if item.filename.startswith("ppt/slides/slide") \
                and item.filename.endswith(".xml"):
            print(". . .", "cleaning", item.filename)
            #data = strip_answers(data)
        new.writestr(item, data)
    new.close()
    old.close()
    print("Complete. Saved as", fn2)
    
"""
def strip_answers(text):
    return re.sub(b'<a:p>.*?<a:t>@a</a:t>.*?</a:p>', b'', text)
"""

def strip_answers(s):
    marker_pos = s.find("<a:t>@a</a:t>")
    
    if marker_pos == -1:
        return s
        
    start = s.rfind("<a:p>", marker_pos)
    end_str = "</a:p>"
    endpos = s.find(end_str, marker_pos) + len(end_str)
    return s[:start] + strip_answer(s[endpos:])

class Test(unittest.TestCase):
    def testRemove(self):
        self.assertEqual(b"AB", strip_answers(b"A<a:p>The Answer<a:t>@a</a:t></a:r>d</a:p>B"))
        self.assertEqual(b"ABCD", strip_answers(b"A<a:p>The Answer<a:t>@a</a:t></a:r>d</a:p>BC<a:p>The Answer<a:t>@a</a:t></a:r>d</a:p>D"))
        self.assertEqual(b"AB", strip_answers(b'A<a:p><a:r><a:rPr lang="en-US" sz="2400" dirty="0" /><a:t>   </a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t>(</a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t>700 </a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t>+/-) </a:t></a:r><a:r><a:rPr lang="en-US" sz="500" baseline="-25000" dirty="0" smtClean="0" /><a:t>@a</a:t></a:r><a:endParaRPr lang="en-US" sz="500" baseline="-25000" dirty="0" /></a:p>B'))

        #self.assertEqual(b"ABC", strip_answers(b"A<a:p>...</a:p>B<a:p>The Answer<a:t>@a</a:t></a:r>d</a:p>C"))


if __name__ == '__main__':
    unittest.main(); sys.exit(1)
    try:
        if len(sys.argv) > 1:
            #
            # start on adding --end but realized I need to do more than
            # just not include those ... -- whm
            if sys.argv[1] == "--end":
                lastSlide = int(sys.argv[2])
                sys.argv = sys.argv[3:]
                end
            for arg in sys.argv[1:]:
                fn = os.path.abspath(arg)
                main(fn)
                print("---")
        else:
            print("You need to drag your .pptx file(s) onto this one.")
    finally:
        input("Press any key to quit.")


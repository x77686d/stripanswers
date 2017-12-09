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

Haskell slides with answers at present: 9, 18-21, 50, 56

Next:
    Maybe use a 0/0/1 "black" to mark answers, instead of @a
        How could that be found?  VBA macro?    
    
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
    try:
        os.remove(fn2)
    except:
        pass

    new = zipfile.ZipFile(fn2, "w")
    for item in old.infolist():
        data = old.read(item.filename)
        if item.filename.startswith("ppt/slides/slide") \
                and item.filename.endswith(".xml"):
            print(". . .", "cleaning", item.filename)
            data = strip_answers(data.decode()).encode()
        new.writestr(item, data)
    new.close()
    os.chmod(fn2, 0o444)
    old.close()
    print("Complete. Saved as", fn2)
    
"""
def strip_answers(text):
    return re.sub(b'<a:p>.*?<a:t>@a</a:t>.*?</a:p>', b'', text)
"""

def strip_answers(s):
    m = re.search(r"<a:t>\s*@a\s*</a:t>", s)
    if not m:
        return s

    marker_pos = m.span()[0]
        
    start = s.rfind("<a:p>", 0, marker_pos)
    end_str = "</a:p>"
    endpos = s.find(end_str, marker_pos) + len(end_str)
    anspar = s[start:endpos]
    return s[:start] + blank_out_text(anspar) + strip_answers(s[endpos:])

def blank_out_text(s):
    m = re.match(r'(.*?<a:t>)(.*?)(</a:t>)(.*$)', s)
    if not m:
        return s
    g = m.groups()
    #
    # Replace the string with a blank else we lose the vertical space for the line
    return g[0] + " " + g[2] + blank_out_text(g[3])

class Test(unittest.TestCase):
    def testClearAT(self):
        self.assertEqual("<a:t> </a:t>", blank_out_text("<a:t>(700 +/-) </a:t>"))
        self.assertEqual("<a:t> </a:t>", blank_out_text("<a:t>(700 +/-) </a:t>"))
        self.assertEqual("A<a:t> </a:t>B<a:t> </a:t>C", blank_out_text("A<a:t>(700 +/-) </a:t>B<a:t>XXX</a:t>C"))

    def testRemove(self):
        self.assertEqual("AB", strip_answers("AB"))
        self.assertEqual("A<a:p><a:t> </a:t><a:t> </a:t></a:r>d</a:p>B", strip_answers("A<a:p><a:t>The Answer</a:t><a:t>@a</a:t></a:r>d</a:p>B"))
        self.assertEqual("A<a:p><a:t> </a:t><a:t> </a:t></a:r>d</a:p>BC<a:p><a:t> </a:t><a:t> </a:t></a:r>d</a:p>D",
           strip_answers("A<a:p><a:t>The Answer</a:t><a:t>@a</a:t></a:r>d</a:p>BC<a:p><a:t>The Answer</a:t><a:t>@a</a:t></a:r>d</a:p>D"))
        self.assertEqual(
                'A<a:p><a:r><a:rPr lang="en-US" sz="2400" dirty="0" /><a:t> </a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t> </a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t> </a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t> </a:t></a:r><a:r><a:rPr lang="en-US" sz="500" baseline="-25000" dirty="0" smtClean="0" /><a:t> </a:t></a:r><a:endParaRPr lang="en-US" sz="500" baseline="-25000" dirty="0" /></a:p>B',
                strip_answers('A<a:p><a:r><a:rPr lang="en-US" sz="2400" dirty="0" /><a:t>   </a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t>(</a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t>700 </a:t></a:r><a:r><a:rPr lang="en-US" sz="2400" dirty="0" smtClean="0" /><a:t>+/-) </a:t></a:r><a:r><a:rPr lang="en-US" sz="500" baseline="-25000" dirty="0" smtClean="0" /><a:t>@a</a:t></a:r><a:endParaRPr lang="en-US" sz="500" baseline="-25000" dirty="0" /></a:p>B'))


        self.assertEqual("A<a:p>...</a:p>B<a:p><a:t> </a:t><a:t> </a:t></a:r>d</a:p>C", strip_answers("A<a:p>...</a:p>B<a:p><a:t>The Answer</a:t><a:t>@a</a:t></a:r>d</a:p>C"))


if __name__ == '__main__':
    #unittest.main(); sys.exit(1)
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
        #input("Press any key to quit.")
        pass


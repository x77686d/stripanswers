# stripanswers
Strip "answers" from PowerPoint pptx files

When teaching I like to provide my students with printed copies of my slides but that leads to a dilemma:
When I pose questions on the slides, should I include the answers?

This program, `stripanswers.py`, reads a .pptx file and generates a new .pptx file with "answers" removed.  At present,
answers are considered to be any paragraph that contains the text "@a".  My current practice is to put the "@a" at the
end of paragraphs in a tiny font, and perhaps with a background-matching color.

**I wrote this program because I couldn't find anything better but if you know of something better, do let me know!**

# Usage
```
% python3 stripanswers.py example.pptx 
Processing .../example.pptx -- please wait.
. . . cleaning ppt/slides/slide4.xml
. . . cleaning ppt/slides/slide3.xml
. . . cleaning ppt/slides/slide2.xml
. . . cleaning ppt/slides/slide1.xml
Complete. Saved as .../example-noans.pptx
---
```
Here is [example.pptx](http://cs.arizona.edu/~whm/stripanswers/example.pptx) and [example-noans.pptx](http://cs.arizona.edu/~whm/example-noans.pptx)

# What's next?
Having to add on an @a is pretty hacky but it does let me check the resulting .pptx file fairly easily--I search it for @a an and see if any made it through.  I've also contemplated using a near-black color, like #001, to mark answers.  I don't know of any way to search for that but maybe that's not important.  If PowerPoint had any notion of Word-like styles, that'd be perfect but it seems like there's no such thing.  I welcome ideas on this.

# Credit
I have to give [Andrew Fong](https://www.andrewfong.com/blog/) most of the credit for this tool which started life as a copy of his [Remove Notes from Powerpoint (PPTX)](
https://www.andrewfong.com/blog/2011/10/04/remove-notes-from-powerpoint-pptx/)
tool.

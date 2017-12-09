# stripanswers
Strip "answers" from PowerPoint pptx files

When teaching I like to provide my students with printed copies of my slides but that leads to a dilemma:
When I pose questions on the slides, should I include the answers?

This program, `stripanswers.py`, reads a .pptx file and generates a new .pptx file with "answers" removed.  At present,
answers are considered to be any paragraph that contains the text "@a".  My current practice is to put the "@a" at the
end of paragraphs in a tiny font, and perhaps with a background-matching color.

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

# What's next?
I've contemplated

# Credit

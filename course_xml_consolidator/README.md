# course_xml_consolidator.py

Consolidate all course XML in a single file. Once XML is in a single file, it can be searched easily using the [lxml.etree](http://lxml.de/tutorial.html) module. Helpful for performing tasks like:

    1. Find all formularesponse problems use 'e' as a variable.
    2. Find all input fields of a particular type with a particular grading format.

**Note**: I do not use this to *edit* course XML, just to help me *find* interesting features. 
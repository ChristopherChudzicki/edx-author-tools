import course_xml_consolidator

# Set path of course directory
course_path = "content-mit-805x/course.xml"

# consolidate the XML into one file and export to `course_consolidated_path`
course = course_xml_consolidator.Course(course_path)
course.export()

# export an OPML outline of the course. Great for workflowy!
url_front = "https://edge.edx.org/courses/course-v1:RELATE+Dev+Sum2015/"
course.export_OPML(url_front=url_front)

# load course from `course_consolidated_path`
course_consolidated_path = course_path[:-4] + "_consolidated.xml"
course = course_xml_consolidator.import_XML(course_consolidated_path)

# Now do whatever you want. For example, count the number of formularesponse problems in sequentials with grading format 'Homework'
sequentials = course.findall(".//sequential[@format='Homework']")
problems = []
for sequential in sequentials:
    problems +=  sequential.findall(".//formularesponse")

print(len(problems))
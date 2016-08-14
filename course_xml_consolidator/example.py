import course_xml_consolidator

# Set path of course directory
course_path = "content-mit-805x/course.xml"
course_consolidated_path = course_path[:-4] + "_consolidated.xml"

# consolidate the XML into one file and export to `course_consolidated_path`
course = course_xml_consolidator.Course(course_path).export()

# load course from `course_consolidated_path`
course = course_xml_consolidator.import_XML(course_consolidated_path)

# Now do whatever you want. For example, count the number of formularesponse problems in sequentials with grading format 'Homework'
sequentials = course.findall(".//sequential[@format='Homework']")
problems = []
for sequential in sequentials:
    problems +=  sequential.findall(".//formularesponse")

print(len(problems))
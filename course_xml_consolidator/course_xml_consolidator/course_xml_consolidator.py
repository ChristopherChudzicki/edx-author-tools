from lxml import etree
import warnings
import os

def remove_comments(element):
    """(element) --> element
    Remove comments that are direct children of an etree.Element object
    """
    for child in element:
        if isinstance(child,etree._Comment):
            element.remove(child)
    return element

def import_XML(path):
    with open(path,'r') as f:
        parser = etree.XMLParser(remove_blank_text=True)
        element = etree.parse(f,parser).getroot()
        return element

def export_XML(element, path):
    with open(path,'w') as f:
        etree.ElementTree(element).write(f, pretty_print=True)

class ExpansionError(Exception):
    pass

class Course(object):
    """docstring for CourseExpanded"""
    def __init__(self, course_path):
        self.not_leaves = ['course', 'chapter', 'sequential', 'vertical', 'split_test']
        self.not_expandable =  ['discussion']
        self.course_path = course_path
        self.course_dir = os.path.dirname(course_path)
        self.expanded = self._expand_recursively( import_XML(course_path) )
    def _get_path_to_expanded_element(self, element):
        """(element) --> str
        Returns the path where the expanded XML for a particular edX element is located.
    
        Example:
            >>> xml_string = <sequential url_name="some_dir:other_dir:filename">
            >>> xml_element = etree.Element(xml_string)
            >>> _get_path_to_expanded_element(xml_element)
        
            would return:
        
            COURSE_DIR/sequential/some_dir/other_dir/filename.xml
        """
        path = "{directory}/{url_name}.xml".format(directory=element.tag, url_name = element.attrib['url_name'])
        path = path.replace(":","/")
        if self.course_dir != "":
            path = "{course_dir}/{path}".format(course_dir=self.course_dir, path=path)
        return path
    def _expand_once(self, element):
        """(element) --> element
        Tries to replace element by the contents of element['url_name'].
        """
        if element.tag in self.not_expandable:
            return element
        children = list(element)
        # If an element has children, it is already expanded. Return the element.
        if len(children) > 0:
            return element
        # If element does not have attribute url_name, it can't be expanded. Return element.
        if not 'url_name' in element.attrib.keys():
            return element
        else:
            url_name = element.attrib["url_name"]
            path = self._get_path_to_expanded_element(element)
            try:
                with open(path,'r') as f:
                    parser = etree.XMLParser(remove_blank_text=True)
                    element = etree.parse(f,parser).getroot()
                element = remove_comments(element)
                element.attrib['url_name'] = url_name
                return element
            except IOError:
                warning_message = "\nCannot open {path}. Aborting expansion. \nParent URL: {parent_url}\n".format(path=path, parent_url=element.getparent().attrib['url_name'])
                warnings.warn(warning_message)
                return element
    def _is_leaf(self, element):
        return element.tag not in self.not_leaves
    def _expand_recursively(self, element):
        """Expands all element recursively, stopping at direct children of verticals.
        """
        if self._is_leaf(element):
            return self._expand_once(element)
        else:
            element = self._expand_once(element)
            for index, child in enumerate(element):
                expanded_child = self._expand_recursively(child)
                element.remove(child)
                element.insert(index,expanded_child)
            return element
    def export(self):
        export_XML(self.expanded, self.course_path[:-4] + "_consolidated.xml" )
    def export_OPML(self, url_front=""):
        OPML = etree.Element('opml')
        OPML_body = etree.SubElement(OPML,'body')
        
        outline = self._to_outline(self.expanded, OPML_body, url_front=url_front)
        string =  etree.tostring(OPML, pretty_print = True)
        export_XML(OPML, self.course_path[:-4] + "_outline.xml")
    def _to_outline(self, content, outline, url_front="" ):
        for content_child in content:
            outline_child = etree.SubElement(outline,'outline')
            display_name = content_child.get('display_name')
            tag = content_child.tag
            url_name = content_child.get('url_name')
            
            outline_child.attrib['type'] = tag
            outline_child.attrib['url_name'] = url_name
            outline_child.attrib['text'] = "{tag}: {display_name}".format(tag=tag.title(), display_name=display_name)
            
            if tag == 'vertical': # Create a link
                outline_child.attrib['_note'] = "{url_front}/jump_to_id/{url_name}".format(url_front=url_front, url_name=url_name )
            if tag in self.not_leaves:
                self._to_outline(content_child, outline_child, url_front=url_front)
            else:
                continue
            

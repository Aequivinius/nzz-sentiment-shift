filename = "/Users/Simon/UNI VII/bigdata/nzz/NZZ_1910_1920-with-uuid/1910-01/JM20121222000301997.xml"
import xml.etree.ElementTree as ET
tree = ET.parse(filename)
root = tree.getroot()
text = root.find('TX')
for child in text.findall('P'):
    print child.text

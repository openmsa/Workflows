import copy
import json
import re
import os
import subprocess


from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import xml.etree.ElementTree as ET
import numpy as np
#from re import search
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from xml.dom import minidom
#from xml.dom.ext.reader.Sax2 import FromXmlStream

dev_var = Variables()
context = Variables.task_call(dev_var)
xml_output_file = context['xml_output_file']

'''  #To used if you want filter the variable which are in YANG file with ' leaf <variable_name> '
yang_good_fields_hash = {}
yang_good_fields = []
pyang_command = ' grep " leaf " ' + str(context['main_yang_file'])
try:
  output = subprocess.check_output(pyang_command, shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
  ret = MSA_API.process_content(constants.FAILED, 'Error:' + stderr, context, True)
  print(ret) 
yang_lines=[]
for line in output.splitlines( ):
  yang_lines.append(line)
  field = re.search(' leaf (\S+) ', str(line), re.IGNORECASE)
  if field:
    yang_good_fields_hash[field.group(1)] = 1  #used hash array to get only one value per fieldname
yang_good_fields = yang_good_fields_hash.keys()
context['yang_good_fields_hash'] = yang_good_fields_hash
'''

yang_fields_without_child_hash = {}

from lxml import etree, objectify

metadata = xml_output_file
parser = etree.XMLParser(attribute_defaults=True, huge_tree=True, ns_clean=False, remove_blank_text=False)
newtree = etree.parse(metadata, parser)
newroot = newtree.getroot()
#objectify.deannotate(newroot, cleanup_namespaces=True)  # Remove namespace  xmlns=xxxx
if (newroot.tag.find('}config')):
  #remove first parent element 'config'
  newtree = etree.ElementTree(newroot[0])

res = ''
for elem in newroot.getiterator():
    if not hasattr(elem.tag, 'find'): continue  # (1)
    i = elem.tag.find('}')
    if i >= 0:
        elem.tag = elem.tag[i+1:]

i=0
parent_yangfield_nochild = {}  # list of parent field who has some chidren field which are in the yang file and has no child.

for element in newroot.iter():
  children = list(element)
  if (i>0):
    parent = element.getparent()
    if len(children):
      res = res + ";\n tag="+ str(element.tag) + ", len="+str(len(children))+ ", parent=" + str(parent.tag) 
    else:    
      res = res + ";\n tag="+ str(element.tag) + ", NO_child" + ", parent=" + str(parent.tag) 
      #find all parents
      all_parents=[]
      grandparent = element.getparent()
      #grandparent = grandparent.getparent() #  remove first bad parent
      while grandparent is not None:
        all_parents.insert(0,grandparent.tag)  #insert first element
        grandparent = grandparent.getparent()
      all_parents.pop(0)   #remove the fisrt config element
      new_tagname  = '_'.join(all_parents) + '_' + element.tag
      #element.tag  = new_tagname
      element.text = '{$params.' + new_tagname + '}'
      yang_fields_without_child_hash[new_tagname] = 1  #used hash array to get only one value per fieldname

  i = i+1

xml_create_output_file = xml_output_file.replace(context['yangs_extension'],'')+'_created.xml'
context['xml_create_output_file'] = xml_create_output_file

context['yang_fields_without_child_hash'] = yang_fields_without_child_hash

newtree.write(xml_create_output_file, pretty_print=True, xml_declaration=False, encoding='UTF-8')

ret = MSA_API.process_content(constants.ENDED, 'Created Part xml = '+xml_create_output_file  , context, True)
print(ret) 




import time
import os
import datetime
import glob
import re
from xml.etree import ElementTree as et
import collections

def get_namespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''

#  Prompt the end-user that this tool is going to be run:
print '------------------- Welcome to use KML_Filter ---------------------------'
print 'Author:      Oliver Xu'
print 'Version:     1.0'
print 'Last Update: 2016.08.18\n'
print 'Input: *.kml file'
print 'Output: .csv file'
print 'This tool would filter out the Placemark/name like 2WAG-05-02-PCD-057'
print 'Then removes those names with Resource Subtype as null and generate CSV file\n'
closeInput = raw_input("Press ENTER to Start")
print '------------------------ Processing -------------------------------------'
print ''
kml_file_list = glob.glob("./*.kml")
for kml_file in kml_file_list:
    # initialize the list
    null_list = []
    null_list2 = []
    whole_list = []
    whole_list2 = []
    final_list = []
    name_list = []
    raw_NE_list = []
    final_NE_list = []
    my_dict = {}
    my_dict2 = {}

    
    #print kml_file
    # e.g.  ".\03.kml", to remove the leading ".\"
    # so that the file name is changed to "03.kml"
    input_file = kml_file.replace(".\\" , "")
    if input_file.endswith('.kml'):
        input_file = input_file[:-4]
    
    #print input_file
    
    # define the output file
    
    # <![CDATA[<html>     *    2WAG-05-02-PCD-057   * <td>Resource Subtype</td><td><div>null
    # _null.log   - store the list of 2WAG-05-02-PCD-057 which has sub type as NULL
    
    # _whole.log  - the whole list of 2WAG-05-02-PCD-057
    # _final.log  - the final list of 2WAG-05-02-PCD-057 (excluded the null list)
    
    rmv_ns_kml_file = '~' + input_file + '.rmv_ns'
    log_file = "~" + input_file + '.ET.log'
    null_html_log_file = "~" + input_file + '.02null.html'
    null_item_name_log_file = "~" + input_file + '.02null.log'
    whole_item_log_file = "~" + input_file + '.01whole.log'
    final_log_file = "~" + input_file + '._log'
    final_NE_file = "~" + input_file + '._NE'
    csv_file = "~" + input_file + '.csv'

    #print log_file
    #print null_html_log_file
    #print null_item_name_log_file
    #print whole_item_log_file
    #print final_log_file
    print csv_file

    # read file as input and save it to file_string
    file_handle = open(kml_file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # remove the name space URL in kml e.g. <kml xmlns="http://www.opengis.net/kml/2.2">
    # re.sub(pattern, repl, string[, count])
    #file_string2 = re.sub(r'\<kml\sxmlns[=":\/\.\w]+\>', '<kml>', file_string)
    #o_rmv_ns_kml_file = open(rmv_ns_kml_file,"w")
    #o_rmv_ns_kml_file.write(file_string2)
    #o_rmv_ns_kml_file.close()
    

    # parse the new xml file which doesn't have the name space in it
    #tree = et.parse(rmv_ns_kml_file)
    
    # parse the kml file
    tree = et.parse(kml_file)
    
    # using xpath to find all './/Placemark/name'
    # for elem in tree.iterfind('Document/Folder/Placemark/name'):
    #
    # name space = http://www.opengis.net/kml/2.2
    #
    # ns='http://www.test.com'
    # el2 = tree.findall("{%s}DEAL_LEVEL/{%s}PAID_OFF" %(ns,ns))
    
    #ns = 'http://www.opengis.net/kml/2.2'
    
    # namespace = get_namespace(tree.getroot())
    # tree.find('./{0}parent/{0}version'.format(namespace)).text
    
    namespace = get_namespace(tree.getroot())
    #print 'name space: ',
    #print namespace
    
    for elem in tree.findall(".//{0}Placemark/{0}name".format(namespace)):
        #print elem.text
        name_list.append(elem.text)
   
    
    #filter out the name_list with the patten like 2WAG-05-02-PCD-057
    name_list = re.findall(r"\w{4}\-\d{2}\-\d{2,3}\-\D{3}\-\d{3,4}", str(name_list))
    #print name_list

    # sort the name_list
    #name_list.sort()

    # to remove the duplicate value,
    # using set() to remove the duplicate value
    name_list2 = list(set(name_list))

    # list has the function of sort() to do the sort.
    #name_list2.sort()   
    
    print 'Total number of matched items like 2WAG-05-02-PCD-057: ', 
    print len(name_list2) 

    # using re.findall() to get all the matching items like 2WAG-05-02-PCD-057, output is list.
    # <![CDATA[<html>     *    2WAG-05-02-PCD-057   * <td>Resource Subtype</td><td><div>null
    # Resource Subtype\<\/td\>\<td>\<div\>null

    null_raw_list = re.findall(r"(^.*?Resource Subtype\<\/td\>\<td\>\<div\>null.*?$)", file_string, re.MULTILINE)



    # list function of sort()
    #null_raw_list.sort()
    null_raw_string = '\n'.join(null_raw_list)
    
    # null_list - filter out the 'NAME   2WAG-05-02-PCD-057' from the null_raw_string
    #
    # <tr><td>NAME</td><td><div>2BWL-01-01-FNO-002</div></td>
    #
    # this is important, because there are many items similar to 2WAG-05-02-PCD-057 in Mappings for this line
    #
    
    null_list = re.findall(r"NAME<\/td><td><div>\w{4}\-\d{2}\-\d{2,3}\-\D{3}\-\d{3,4}", null_raw_string)
    null_list_string = '\n'.join(null_list)
    
    # filter out '2WAG-05-02-PCD-057' from the null_list_string
    null_list2 = re.findall(r"\w{4}\-\d{2}\-\d{2,3}\-\D{3}\-\d{3,4}", null_list_string)
    
    null_list2 = list(set(null_list2))
    #null_list2.sort()

    print 'Total number of matched items with null Subtype:       ', 
    print len(null_list2)	
	
    # using re.findall() to get all the matching items, output is list.
    #whole_list = re.findall(r"\w{4}\-\d{2}\-\d{2,3}\-\D{3}\-\d{3,4}", file_string)
    #whole_list2 = list(set(whole_list))
    #whole_list2.sort()

    #final_list = list( set(whole_list) - set(null_list) )

    final_list = list( set(name_list2) - set(null_list2) )
    
    #final_list.sort()
    
    print 'Total number of matched items without null Subtype:    ', 
    print len(final_list)
    print ''    
    
    # Following 3 files are only for debugging purpose.
    # for the final version, need to comment them.
    """

    # open file to write
    o_null_html_log_file = open(null_html_log_file,"w")
    o_null_item_name_log_file = open(null_item_name_log_file,"w")
    o_whole_item_log_file = open(whole_item_log_file,"w")

    # write to file with the content
    # the following 3 log files are only for debugging purpose.
    
    o_null_html_log_file.write("\n".join(null_raw_list))
    o_null_html_log_file.close()
    
    o_null_item_name_log_file.write("\n".join(null_list2))
    o_null_item_name_log_file.close()  
    
    o_whole_item_log_file.write("\n".join(whole_list2))
    o_whole_item_log_file.close()
    
    """ 


    # write out the result to final_log
    #o_final_log_file = open(final_log_file, "w")
    #o_final_log_file.write("\n".join(final_list))
    #o_final_log_file.close()
    
    # delete the temp file
    if os.path.exists(rmv_ns_kml_file):
        os.remove(rmv_ns_kml_file)  
    
    # Filter out the NE name from final_list
    # e.g. get PCD out of 2WAG-05-02-PCD-057 
    # 
    final_list_str = str(final_list)
    
    # get -PCD-
    raw_NE_list = re.findall(r"(\-\D{3}\-)", final_list_str)
    raw_NE_list_str = str(raw_NE_list)
    
    # get PCD
    final_NE_list = re.findall(r"(\w{3})", raw_NE_list_str) 

    # write out the result to final_log
    #o_final_NE_list = open(final_NE_file, "w")
    #o_final_NE_list.write("\n".join(final_NE_list))
    #o_final_NE_list.close()
    
    # my_dict
    my_dict = dict(zip(final_list,final_NE_list))
    
    # sort the dict
    my_dict2 = collections.OrderedDict(sorted(my_dict.items()))
    
    # write the CSV file
    with open(csv_file, 'w') as f:
        f.write("Name,Type\n")
        [f.write('{0},{1}\n'.format(key, value)) for key, value in my_dict2.items()]          
    
print ''

print '-------------------------------------------------------------------------'
closeInput = raw_input("Press ENTER to exit")
print "Closing...\n"

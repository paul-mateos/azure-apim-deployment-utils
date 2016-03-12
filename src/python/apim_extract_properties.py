import os
import sys
import azure_apim

def apim_extract_properties(base_dir):
    if not base_dir.endswith(os.sep):
        base_dir = base_dir + os.sep
        
    print "Checking configuration..."

    instances_json = base_dir + 'instances.json'
    if not os.path.isfile(instances_json):
        print "Could not find 'instances.json'"
        return False
    
    instance = "apim"

    apim = azure_apim.create_azure_apim(instances_json)
    properties_file = os.path.join(base_dir, 'properties_extracted.json')
    
    print "Extracting properties to 'properties_extracted.json'"
    if not apim.extract_properties_to_file("apim", properties_file):
        print "Property extraction failed."
        return False
    print "Property extraction succeeded."
    
    return True
    
if len(sys.argv) < 2:
    print "Usage:"
    print "   python apim_extract_properties.py <config dir>"
    sys.exit(1)

if not apim_extract_properties(sys.argv[1]):
    sys.exit(1)
    
sys.exit(0)

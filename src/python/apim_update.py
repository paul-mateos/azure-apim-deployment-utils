import os
import sys
import azure_apim

def apim_update(base_dir):
    if not base_dir.endswith(os.sep):
        base_dir = base_dir + os.sep
    print "Checking configuration..."

    instances_json = os.path.join(base_dir, 'instances.json')
    if not os.path.isfile(instances_json):
        print "Could not find 'instances.json'"
        return False
        
    apim = azure_apim.create_azure_apim(instances_json)
    instance = 'apim'

    # Check for properties
    properties_file = os.path.join(base_dir, 'properties.json')
    if os.path.isfile(properties_file):
        if not apim.upsert_properties_from_file(instance, properties_file):
            print "Upserting properties failed."
            return False
        print "Update of properties succeeded."
    else:
        print "Skipping properties, could not find 'properties.json'."
    
    # Check for certificates
    certificates_file = os.path.join(base_dir, 'certificates.json')
    if os.path.isfile(certificates_file):
        if not apim.upsert_certificates_from_file(instance, certificates_file):
            print "Upserting certificates failed."
            return False
        print "Update of certificates succeeded."
    else:
        print "Skipping certificates, could not find 'certificates.json'."
        
    # Check for Swagger files
    swaggerfiles_file = os.path.join(base_dir, 'swaggerfiles.json')
    if os.path.isfile(swaggerfiles_file):
        if not apim.update_swagger_from_file(instance, swaggerfiles_file):
            print "Updating Swagger API definitions failed."
            return False
        print "Update of APIs via Swagger definitions succeeded."
    else:
        print "Skipping Swagger update, could not find 'swaggerfiles.json'."
    
    # Room for more things (backends?)

    return True

if len(sys.argv) < 2:
    print "Usage:"
    print "   python apim_update.py <config dir>"
    sys.exit(1)

if not apim_update(sys.argv[1]):
    sys.exit(1)
    
sys.exit(0)

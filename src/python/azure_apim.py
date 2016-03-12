import time
import sys
import requests
import json
import hashlib
import random
import token_factory
import os
from utils import byteify, replace_env

def create_azure_apim(instances_file):
    tf = token_factory.create_token_factory_from_file(instances_file)
    return AzureApim(tf)

class AzureApim:
    def __init__(self, token_factory):
        self._token_factory = token_factory
        
    def git_save(self, instance, target_branch):
        return self.exec_async_operation(instance, 'tenant/configuration/save',
                                         {'branch': target_branch, 'force': True})
                                    
    def git_deploy(self, instance, source_branch):
        return self.exec_async_operation(instance, 'tenant/configuration/deploy',
                                         {'branch': source_branch, 'force': True})
    
    def git_validate(self, instance, source_branch):
        return self.exec_async_operation(instance, 'tenant/configuration/validate',
                                         {'branch': source_branch, 'force': True})
                                    
    def get_token_factory(self):
        return self._token_factory

    def exec_async_operation(self, instance, operation, json_payload):
        sas_token = self._token_factory.get_sas_token(instance)
        base_url = self._token_factory.get_base_url(instance)
        api_version = self._token_factory.get_api_version()

        save_req = requests.post(base_url + operation + api_version, 
            headers = {'Authorization': sas_token, 'Content-Type': 'application/json' },
            json = json_payload)

        if (202 != save_req.status_code):
            print "Failed to execute operation."
            print "Return Code: " + str(save_req.status_code)
            print save_req.text
        
            return False

        location = save_req.headers['Location']
        print location

        ready = False

        while not ready:
            time.sleep(5)
            status_req = requests.get(location, headers={'Authorization': sas_token})
        
            if (200 != status_req.status_code):
                print "Fetching the status of the process failed:"
                print status_req.text
                
                return False
        
            status_json = byteify(json.loads(status_req.text))
            statusString = status_json['status']
        
            print "Operation Status: " + statusString
        
            if (statusString == "InProgress"):
                continue
            if (statusString == "Succeeded"):
                ready = True
                break
            print "Unexpected status string: '" + statusString + "'. Exiting."
            return False
        return True

    def upsert_certificates_from_file(self, instance, certificates_file):
        with open(certificates_file, 'r') as json_file:
            json_certificates = replace_env(byteify(json.loads(json_file.read())))
        return self.upsert_certificates(instance, json_certificates['certificates'])
        
        
    def upsert_certificates(self, instance, certificate_infos):
        sas_token = self._token_factory.get_sas_token(instance)
        base_url = self._token_factory.get_base_url(instance)
        api_version = self._token_factory.get_api_version()
        
        md5_bucket = {}
        for certificate_info in certificate_infos:
            hex = self.__hexmd5(certificate_info['fileName'])
            md5_bucket[hex] = certificate_info
        
        certs_res = requests.get(base_url + 'certificates' + api_version, 
                                headers = {'Authorization': sas_token})
        if (200 != certs_res.status_code):
            print certs_res.text
            return False
        
        cid_bucket = {}
        certs_json = byteify(json.loads(certs_res.text))
        for cert in certs_json['value']:
            print "Certificate: " + cert['id'] + ", " + cert[u'subject']
            cid_string = cert['id'] # /certificates/{unique id}
            cid = cid_string[cid_string.index('/', 2) + 1:] # /certificates/{unique id} -- pick unique id
            print "cid: " + cid
            cid_bucket[cid] = True

        print cid_bucket

        for cid in cid_bucket:
            if not cid in md5_bucket:
                print "Will delete cid '" + cid + "'"
                if not self.__delete_certificate(base_url, sas_token, api_version, cid):
                    return False
                print "Deleted cid '" + cid + "'."
        
        for cert in md5_bucket:
            if not cert in cid_bucket:
                print "Will add cert '" + md5_bucket[cert]['fileName'] + "' (MD5 " + cert + ")"
                if not self.__add_certificate(base_url, sas_token, api_version, md5_bucket[cert], cert):
                    return False
                print "Added cert '" + md5_bucket[cert]['fileName'] + "'"
            else:
                print "Found certificate with cid '" + cert + "'."

        return True
                

        cert_del_res = requests.delete(base_url + 'certificates/' + cid + api_version,
                                    headers = {'Authorization': sas_token, 'If-Match': '*'})
        if (204 == cert_del_res.status_code
            or 200 == cert_del_res.status_code):
            return True
            
        print "Deletion of certificate failed!"
        print cert_del_res.text
        return False
        
    def update_swagger_from_file(self, instance, swaggerfiles_file):
        with open(swaggerfiles_file, 'r') as json_file:
            swaggerfiles = replace_env(byteify(json.loads(json_file.read())))
        return self.update_swagger(instance, swaggerfiles)
        
    def update_swagger(self, instance, swaggerfiles):
        sas_token = self._token_factory.get_sas_token(instance)
        base_url = self._token_factory.get_base_url(instance)
        api_version = self._token_factory.get_api_version()
        # First, find the ids of the APIs.
        api_res = requests.get(base_url + 'apis' + api_version,
                               headers = {'Authorization': sas_token})
        if (200 != api_res.status_code):
            print "Could not retrieve API information (/api endpoint)."
            print api_res.text
            return False

        apis_json = byteify(json.loads(api_res.text))

        api_id_bag = {}
        api_bag = {}
        for api_def in apis_json['value']:
            api_url = api_def['serviceUrl']
            api_id_url = api_def['id'] # /apis/3498734a389f7bc83749837493
            api_id = api_id_url[api_id_url.index('/', 2) + 1:]
            api_name = api_def['name']
            print "Found API '" + api_name + "' (id " + api_id + ")."
            api_id_bag[api_url] = api_id
            api_bag[api_url] = api_def

        for swaggerfile in swaggerfiles['swaggerFiles']:
            print "Updating '" + swaggerfile['swagger'] + "'."
            swagger_url = swaggerfile['serviceUrl']
            if swagger_url not in api_id_bag:
                print "Could not find serviceUrl '" + swagger_url + "'. Is it a new API? Import it once first in the Web UI."
                return False
            
            api_id = api_id_bag[swagger_url]
            swagger_json = self.__load_swagger(instance, swaggerfile['swagger'])
            swag_res = requests.put(base_url + 'apis/' + api_id + api_version + '&import=true',
                                    headers={'Authorization': sas_token,
                                             'If-Match': '*',
                                             'Content-Type': 'application/vnd.swagger.doc+json'},
                                    json = swagger_json)
            if (204 != swag_res.status_code):
                print "Updating the API did not succeed."
                print swag_res.status_code
                return False
            # Re-update the API definition because the Swagger import overwrites the serviceUrl
            api_res = requests.patch(base_url + 'apis/' + api_id + api_version,
                                     headers = {'Authorization': sas_token,
                                                'If-Match': '*'},
                                     json = api_bag[swagger_url])
            if (204 != api_res.status_code):
                print "Could not update serviceUrl (next update will break!)."
                print api_res.text
                return False
            print "Update succeeded."

        return True
        
    def __load_swagger(self, instance, swagger_file):
        with open(swagger_file, 'r') as json_file:
            swagger_json = byteify(json.loads(json_file.read()))

        # Mandatory for importing swagger            
        swagger_json['host'] = self._token_factory.get_host(instance)
        if 'basePath' not in swagger_json:
            raise LookupError("Could not find 'basePath' property.")
        if 'schemes' not in swagger_json:
            raise LookupError("Could not find 'schemes' property.")
        return swagger_json
        
    def export_swagger_files(self, instance, target_dir):
        sas_token = self._token_factory.get_sas_token(instance)
        base_url = self._token_factory.get_base_url(instance)
        api_version = self._token_factory.get_api_version()

        apis_res = requests.get(base_url + 'apis' + api_version,
                                headers = {'Authorization': sas_token})
        if (200 != apis_res.status_code):
            print "Could not retrieve APIs."
            print apis_res.text
            return False
        
        apis_json = byteify(json.loads(apis_res.text))
        for api_def in apis_json['value']:
            api_url = api_def['id']
            
            swagger_res = requests.get(base_url + api_url[1:] + api_version + '&export=true', 
                                       headers={'Authorization': sas_token,
                                                'Accept': 'application/vnd.swagger.doc+json'})
            if (200 != swagger_res.status_code):
                print "Could not export Swagger definition."
                print swagger_res.text
                return False
            
            swagger = json.loads(swagger_res.text)
            id_name = swagger['basePath'].replace('/', '_')
            if (id_name.startswith('_')):
                id_name = id_name[1:]
            sep = ''
            if not target_dir.endswith(os.sep):
                sep = os.sep
            with open(target_dir + sep + id_name + ".json", 'w') as outfile:
                json.dump(swagger, outfile, indent=4)
                
        return True
            

    def extract_properties(self, instance):
        sas_token = self._token_factory.get_sas_token(instance)
        base_url = self._token_factory.get_base_url(instance)
        api_version = self._token_factory.get_api_version()
        
        prop_get = requests.get(base_url + 'properties' + api_version,
                                headers = {'Authorization': sas_token})
        if (200 != prop_get.status_code):
            print "Could not get properties from '" + instance + "'."
            print prop_get.text
            return False
        
        props_json = byteify(json.loads(prop_get.text))
        props = {}
        for prop in props_json['value']:
            props[prop['name']] = {
                "value": prop['value'],
                "tags": prop['tags'],
                "secret": prop['secret']
            }
        return props
        
    def extract_properties_to_file(self, instance, file_name):
        props = self.extract_properties(instance)
        
        with open(file_name, 'w') as json_file:
            json.dump(props, json_file, indent = 4)
        return True

    def upsert_properties_from_file(self, instance, properties_file):
        with open(properties_file, 'r') as json_file:
            json_properties = replace_env(byteify(json.loads(json_file.read())))
        return self.upsert_properties(instance, json_properties)

    def upsert_properties(self, instance, properties):
        sas_token = self._token_factory.get_sas_token(instance)
        base_url = self._token_factory.get_base_url(instance)
        api_version = self._token_factory.get_api_version()
        
        prop_get = requests.get(base_url + 'properties' + api_version,
                                headers = {'Authorization': sas_token})
        if (200 != prop_get.status_code):
            print "Could not get properties from '" + instance + "'."
            print prop_get.text
            return False
        
        props_json = byteify(json.loads(prop_get.text))
        
        prop_id_bag = {}
        for prop in props_json['value']:
            prop_id = prop['id']
            prop_id_bag[prop['name']] = prop_id[prop_id.index('/', 2) + 1:]

        for prop_name in properties:
            if prop_name in prop_id_bag:
                print "Updating '" + prop_name + "'"
                if not self.__update_property(base_url, sas_token, api_version, prop_name, prop_id_bag[prop_name], properties[prop_name]):
                    return False
            else:
                print "Inserting '" + prop_name + "'"
                if not self.__insert_property(base_url, sas_token, api_version, prop_name, properties[prop_name]):
                    return False

        for prop in props_json['value']:
            prop_name = prop['name']
            if not prop_name in properties:
                # Property in APIm, not in JSON, delete it
                print "Deleting property '" + prop_name + "'."
                if not self.__delete_property(base_url, sas_token, api_version, prop_name, prop_id_bag[prop_name]):
                    return False

        return True

    def __update_property(self, base_url, sas_token, api_version, prop_name, prop_id, properties):
        prop_res = requests.patch(base_url + 'properties/' + prop_id + api_version,
                                  headers = {'Authorization': sas_token, 'If-Match': '*'},
                                  json = {
                                      'name': prop_name,
                                      'value': properties['value'],
                                      'tags': properties['tags'],
                                      'secret': properties['secret']    
                                  })
        if (200 != prop_res.status_code
            and 204 != prop_res.status_code):
            print "Update of property '" + prop_name + "' failed."
            print prop_res.text
            return False
        print "Successfully updated property '" + prop_name + "' (id " + prop_id + ")."
        return True
        
    def __insert_property(self, base_url, sas_token, api_version, prop_name, properties):
        # We need a random ID to PUT the property to.
        prop_id = '%030x' % random.randrange(16**30)
        prop_res = requests.put(base_url + 'properties/' + prop_id + api_version,
                                headers = {'Authorization': sas_token},
                                json = {
                                    'name': prop_name,
                                    'value': properties['value'],
                                    'tags': properties['tags'],
                                    'secret': properties['secret']    
                                })
        if (200 != prop_res.status_code
            and 201 != prop_res.status_code):
            print "Insert of property '" + prop_name + "' failed."
            print prop_res.text
            return False
        print "Successfully inserted property '" + prop_name + "' (id " + prop_id + ")."
        return True
 
    def __delete_property(self, base_url, sas_token, api_version, prop_name, prop_id):
        prop_res = requests.delete(base_url + 'properties/' + prop_id + api_version,
                                   headers = {'Authorization': sas_token, 'If-Match': '*'})
        if (204 != prop_res.status_code
            and 200 != prop_res.status_code):
            print "Deletion of property '" + prop_name + "' (id " + prop_id + ") failed."
            print prop_res.text
            return False
        print "Successfully deleted property '" + prop_name + "' (id " + prop_id + ")."
        return True

    def __hexmd5(self, fileName):
        hasher = hashlib.md5()
        with open(fileName, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        return hasher.hexdigest()

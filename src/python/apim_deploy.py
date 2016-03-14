import os
import tempfile
import shutil
import zipfile
import azure_apim
import apim_update

def apim_deploy(source_zip):
    config_tmp = tempfile.mkdtemp()
    git_tmp = tempfile.mkdtemp()

    print "Work in progress. Uncomment to test."
    return False

    try:
        # Extract ZIP file
        print "Unzipping configuration file..."
        if not os.path.isfile(source_zip):
            print "Could not read source zip file '" + source_zip + "'."
            return False
        
        zip_file = zipfile.ZipFile(source_zip, 'r')
        try:
            zip_file.extractall(config_tmp)
        finally:
            zip_file.close()

        # Check sanity of config dir
        instances_json = os.path.join(config_tmp, 'instances.json')
        if not os.path.isfile(instances_json):
            print "Could not find 'instances.json'"
            return False
        
        # Do an apim_update on the extracted files
        print "Updating certificates and properties..."
        apim_update.apim_update(config_tmp)
        
        # Save current config to git
        instance = "apim"

        apim = azure_apim.create_azure_apim(instances_json)
        print "Telling APIm to store configuration to git..."
        if not apim.git_save(instance, 'master'):
            print "Failed."
            return False
        
        # Clone to local dir
        scm_user = 'apim'
        scm_password = apim.get_token_factory().get_scm_sas_token(instance)
        scm_host = apim.get_token_factory().get_scm_url(instance)
        
        print "Cloning repository to '" + git_tmp + "'.
        repo = git.Repo.clone_from(
            'https://' + scm_user + ':' + scm_password + '@' + scm_host,
            git_tmp
        )
        print "git clone done."
        
        # Overwrite config with content from ZIP file
        
        # Push the changes to the APIm git repo
    finally:
        shutil.rmtree(config_tmp)
        shutil.rmtree(git_tmp)
    
    return True
    
if len(sys.argv) < 2:
    print "Usage:"
    print "   python apim_deploy.py <config dir> <target file>"
    sys.exit(1)

if not apim_deploy(sys.argv[1], sys.argv[2]):
    sys.exit(1)
    
sys.exit(0)

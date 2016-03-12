import sys
import os
import tempfile
import shutil
import git
import zipfile
import azure_apim

def apim_extract(base_dir, target_zip):
    if not base_dir.endswith(os.sep):
        base_dir = base_dir + os.sep

    if target_zip.endswith('.zip'):
        target_zip = target_zip[:-4] # strip .zip

    print "Checking configuration..."

    instances_json = base_dir + 'instances.json'
    if not os.path.isfile(instances_json):
        print "Could not find 'instances.json'"
        return False

    config_files = [
        'instances.json',
        'properties.json',
        'certificates.json',
        'swaggerfiles.json'
    ]

    instance = "apim"

    apim = azure_apim.create_azure_apim(instances_json)
    print "Telling APIm to store configuration to git..."
    if not apim.git_save(instance, 'master'):
        print "Failed."
        return False

    #repo = git.Repo.clone_from('https://github.com/apisio/apis.io.git', '~/Temp/new_repo', branch='master')
    scm_user = 'apim'
    scm_password = apim.get_token_factory().get_scm_sas_token(instance)
    scm_host = apim.get_token_factory().get_scm_url(instance)

    git_temp = tempfile.mkdtemp()

    try:
        print "Cloning repository to temporary path..."
        print "Temp path: " + git_temp
        apim_path = os.path.join(git_temp, 'azureapim.scm')
        repo = git.Repo.clone_from(
            'https://' + scm_user + ':' + scm_password + '@' + scm_host,
            apim_path
        )
        print "git clone done."
        shutil.rmtree(os.path.join(apim_path, '.git')) # remove git folder

        for config_file in config_files:
            full_path = os.path.join(base_dir, config_file)
            if os.path.isfile(full_path):
                shutil.copyfile(full_path, os.path.join(git_temp, config_file))

        print "Creating archive."
        shutil.make_archive(target_zip, format='zip', root_dir=git_temp)
        
    finally:
        shutil.rmtree(git_temp)

    print "Operation finished successfully."
    return True

if len(sys.argv) < 3:
    print "Usage:"
    print "   python apim_extract.py <config dir> <target file>"
    sys.exit(1)

if not apim_extract(sys.argv[1], sys.argv[2]):
    sys.exit(1)
    
sys.exit(0)

import tempfile
import shutil
import azure_apim
import apim_update

def apim_deploy(source_zip):
    config_tmp = tempfile.mkdtemp()
    git_tmp = tempfile.mkdtemp()

    try:
        # Extract ZIP file
        
        # Do an apim_update on the extracted files
        
        # Save current config to git
        
        # Clone to local dir
        
        # Overwrite config with content from ZIP file
        
        # Push the changes to the APIm git repo
    finally:
        shutil.rmtree(config_tmp)
        shitil.rmtree(git_tmp)
    
    return True
    
if len(sys.argv) < 2:
    print "Usage:"
    print "   python apim_deploy.py <config dir> <target file>"
    sys.exit(1)

if not apim_deploy(sys.argv[1], sys.argv[2]):
    sys.exit(1)
    
sys.exit(0)

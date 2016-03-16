import os
import tempfile
import shutil
import sys

if len(sys.argv) < 2:
    print "Usage:"
    print "  python create_dist.py <version>"
    sys.exit(1)

version = sys.argv[1]

try:
    temp_dir = tempfile.mkdtemp()
    print "Using temporary directory: " + temp_dir
    target_dir = os.path.join(temp_dir, 'azure-apim-deployment-utils')
    #os.makedirs(target_dir)
    
    shutil.copytree(os.path.join('..', 'apim'), target_dir, ignore=shutil.ignore_patterns('*.pyc', 'tmp*', '.DS_*'))
    
    target_dir = os.path.join(os.path.join('..', '..'), 'bin')
    target_file = os.path.join(target_dir, 'azure-apim-deployment-utils-' + version)
    shutil.make_archive(target_file, format='zip', root_dir=temp_dir)
    
finally:
    shutil.rmtree(temp_dir)

sys.exit(0)

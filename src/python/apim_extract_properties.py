import sys
import apim_commands
    
if len(sys.argv) < 2:
    print "Usage:"
    print "   python apim_extract_properties.py <config dir>"
    sys.exit(1)

if not apim_commands.apim_extract_properties(sys.argv[1]):
    sys.exit(1)
    
sys.exit(0)

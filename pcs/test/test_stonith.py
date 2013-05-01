import os,sys
import shutil
import unittest
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
import utils
from pcs_test_functions import pcs

empty_cib = "empty.xml"
temp_cib = "temp.xml"

class StonithTest(unittest.TestCase):
    def setUp(self):
        shutil.copy(empty_cib, temp_cib)

    def testStonithCreation(self):
        output, returnVal = pcs(temp_cib, "stonith create test1 fence_noxist")
        assert returnVal == 1
        assert output == "Error: Unable to create resource 'stonith:fence_noxist', it is not installed on this system (use --force to override)\n"

        output, returnVal = pcs(temp_cib, "stonith create test1 fence_noxist --force")
        assert returnVal == 0
        assert output == ""

        output, returnVal = pcs(temp_cib, "stonith create test2 fence_ilo")
        assert returnVal == 0
        assert output == ""

        output, returnVal = pcs(temp_cib, "stonith create test3 fence_ilo bad_argument=test")
        assert returnVal == 1
        assert output == "Error: resource option(s): 'bad_argument', are not recognized for resource type: 'stonith:fence_ilo' (use --force to override)\n",[output]

        output, returnVal = pcs(temp_cib, "stonith create test3 fence_ilo ipaddr=test")
        assert returnVal == 0
        assert output == "",[output]

# Testing that pcmk_host_check, pcmk_host_list & pcmk_host_map are allowed for
# stonith agents
        output, returnVal = pcs(temp_cib, 'stonith create apc-fencing fence_apc params ipaddr="morph-apc" login="apc" passwd="apc" switch="1" pcmk_host_map="buzz-01:1;buzz-02:2;buzz-03:3;buzz-04:4;buzz-05:5" action="reboot" debug="1" pcmk_host_check="static-list" pcmk_host_list="buzz-01,buzz-02,buzz-03,buzz-04,buzz-05"')
        print output
        assert returnVal == 0
        assert output == "",[output]

        output, returnVal = pcs(temp_cib, 'stonith show apc-fencing')
        assert returnVal == 0
        assert output == ' Resource: apc-fencing (class=stonith type=fence_apc)\n  Attributes: ipaddr="morph-apc" login="apc" passwd="apc" switch="1" pcmk_host_map="buzz-01:1;buzz-02:2;buzz-03:3;buzz-04:4;buzz-05:5" action="reboot" debug="1" pcmk_host_check="static-list" pcmk_host_list="buzz-01,buzz-02,buzz-03,buzz-04,buzz-05" \n',[output]

        output, returnVal = pcs(temp_cib, 'stonith delete apc-fencing')
        assert returnVal == 0
        assert output == 'Deleting Resource - apc-fencing\n',[output]

        output, returnVal = pcs(temp_cib, "stonith update test3 bad_ipaddr=test")
        assert returnVal == 1
        assert output == "Error: resource option(s): 'bad_ipaddr', are not recognized for resource type: 'stonith::fence_ilo' (use --force to override)\n",[output]

        output, returnVal = pcs(temp_cib, "stonith update test3 login=testA")
        assert returnVal == 0
        assert output == "",[output]

        output, returnVal = pcs(temp_cib, "stonith show test2")
        assert returnVal == 0
        assert output == " Resource: test2 (class=stonith type=fence_ilo)\n",[output]

        output, returnVal = pcs(temp_cib, "stonith show --all")
        assert returnVal == 0
        assert output == " Resource: test1 (class=stonith type=fence_noxist)\n Resource: test2 (class=stonith type=fence_ilo)\n Resource: test3 (class=stonith type=fence_ilo)\n  Attributes: ipaddr=test login=testA \n",[output]


    def testStonithFenceConfirm(self):
        output, returnVal = pcs(temp_cib, "stonith fence blah blah")
        assert returnVal == 1
        assert output == "Error: must specify one (and only one) node to fence\n"

        output, returnVal = pcs(temp_cib, "stonith confirm blah blah")
        assert returnVal == 1
        assert output == "Error: must specify one (and only one) node to confirm fenced\n"

if __name__ == "__main__":
    unittest.main()

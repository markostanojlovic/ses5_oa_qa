import unittest
from pool_new import NewPoolTestCase
from pool_edit import EditNewPoolTestCase
from pool_delete import DeleteNewPoolTestCase
from rbd_img_new import NewRBDTestCase

def suite():
    suite = unittest.TestSuite()
    suite.addTest (NewPoolTestCase('test_TC001'))
    suite.addTest (NewPoolTestCase('test_TC002'))
    suite.addTest (EditNewPoolTestCase('test_TC003'))
    suite.addTest (EditNewPoolTestCase('test_TC004'))
    suite.addTest (DeleteNewPoolTestCase('test_TC005'))
    suite.addTest (DeleteNewPoolTestCase('test_TC006'))
    suite.addTest (NewRBDTestCase('test_TC007'))
    suite.addTest (NewRBDTestCase('test_TC008'))
    suite.addTest (iSCSITestCase('test_TC009'))
    suite.addTest (iSCSITestCase('test_TC010'))
    suite.addTest (iSCSITestCase('test_TC011'))
    suite.addTest (iSCSITestCase('test_TC012'))
    suite.addTest (iSCSITestCase('test_TC013'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    runner.run (test_suite)

import unittest
from LoginPageTCs import TestLoginPage
from PoolsPageTCs import TestPoolsPage

def suite():
    suite = unittest.TestSuite()
    suite.addTest (TestLoginPage('test_TC001_default_login'))
    suite.addTest (TestPoolsPage('test_oA001_new_pool_repl_3_pg_16_app_rbd'))
    suite.addTest (TestPoolsPage('test_oA002_new_pool_ec_pg_16_app_rbd_cephfs'))
    suite.addTest (TestPoolsPage('test_oA003_edit_pool_repl_3_pg_16_app_rbd'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    runner.run (test_suite)

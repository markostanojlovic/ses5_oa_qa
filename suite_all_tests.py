import unittest
from test_LoginPageTCs import TestLoginPage
from test_PoolsPageTCs import TestPoolsPage
from test_RBDsPageTCs import TestRBDsPage
from test_BugReproduceTCs import TestBugs

def suite():
    suite = unittest.TestSuite()
    suite.addTest (TestLoginPage('test_TC001_default_login'))
    suite.addTest (TestPoolsPage('test_oA001_new_pool_repl_3_pg_16_app_rbd'))
    suite.addTest (TestPoolsPage('test_oA002_new_pool_ec_pg_16_app_rbd_cephfs'))
    suite.addTest (TestPoolsPage('test_oA003_edit_pool_repl_3_pg_16_app_rbd'))
    suite.addTest (TestPoolsPage('test_oA004_edit_pool_ec_pg_16_app_rgw'))
    suite.addTest (TestPoolsPage('test_oA005_del_pool_repl_pg_64_rgw'))
    suite.addTest (TestPoolsPage('test_oA006_del_pool_ec_pg_32_rgw_rbd'))
    suite.addTest (TestRBDsPage('test_oA007_new_RBD_15G_from_repl_pg_16'))
    suite.addTest (TestBugs('test_bug_1100710'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    runner.run (test_suite)

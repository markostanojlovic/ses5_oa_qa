import pytest
from pprint import pprint
import datetime

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest customization. 
    When there is a failed test, screen is captured. 
    """
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        path = './prtsc_failed'
        today = datetime.date.today().strftime('%Y_%m_%d')
        time = datetime.datetime.now().time().strftime('%H_%M')
        timestamp = today + '_' + time
        test_name = rep.location[2] # better than print(rep.nodeid)
        prtsc_name = '{}/failed_{}_{}.png'.format(path,test_name,timestamp)
        # pprint(vars(rep))
        print('DEBUG INFO: Screen captured and available at: {}'.format(prtsc_name))
        # print(self.driver.current_url)  
        # TODO how to pass self.driver to this method? 
        # print(self.driver.msg)
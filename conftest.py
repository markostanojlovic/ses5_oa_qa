import pytest
from pprint import pprint
import datetime

@pytest.fixture(scope="class")
def driver_get(request):
    """
    For whole test suite, running one Chrome browser seassion. 
    """
    from selenium import webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    web_driver = webdriver.Chrome(options=chrome_options) # TODO paramatrize to use headless etc. 
    # web_driver = webdriver.Chrome() # DEBUG 
    request.cls.driver = web_driver
    yield
    web_driver.close()

# @pytest.fixture(scope="session") # use for all 
# def driver_get(request):
#     """
#     For whole test suite, running one Chrome browser seassion. 
#     """
#     from selenium import webdriver
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('headless')
#     chrome_options.add_argument('window-size=1920x1080')
#     web_driver = webdriver.Chrome(options=chrome_options)
#     session = request.node
#     for item in session.items:
#         cls = item.getparent(pytest.Class)
#         setattr(cls.obj, "driver", web_driver)
#     yield
#     web_driver.close()

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
        path = './prtsc_failed' # TODO create a directory if not existing 
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
import pytest
import datetime
import os

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

@pytest.fixture(scope='class')
def web_driver(request):
    return request.cls.driver

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
        if not os.path.exists(path):
            os.makedirs(path)
        today = datetime.date.today().strftime('%Y_%m_%d')
        time = datetime.datetime.now().time().strftime('%H_%M')
        timestamp = today + '_' + time
        test_name = rep.location[2] # better than print(rep.nodeid)
        prtsc_name = '{}/failed_{}_{}.png'.format(path,test_name,timestamp)
        print('\nDEBUG INFO: Screen captured and available at: {}'.format(prtsc_name))
        if 'web_driver' in item.fixturenames:
            web_driver = item.funcargs['web_driver']
            print('DEBUG INFO:Current URL: {}'.format(web_driver.current_url))
            try:
                web_driver.save_screenshot(prtsc_name)
            except:
                print("ERROR: Screenshot creation failed.")            
        else:
            print('NO WEBDRIVER')
            return
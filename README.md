# Selenium automation of openAttic ses5 qa tests 

Number of defined TCs (Test Cases): 4
Duration of all tests suite: 60.65 s

## Requirements :

- Chrome browser 
- Python 3.6
- Python modules: *list is in python_requirement.txt file*
- Connection to running SES cluster with:
  - IP of a openAttic server is setup in config.yml
  - openAttic installed and configured with all applications and APIs (RGW, iSCSI, NFS, Salt)
  - At least 2 iSCSI cluster nodes deployed 

## How to setup the environment 

### Python

- To setup Python environment run: `./py_setup.sh`

### Selenium Webdriver for Chrome 
 

## How to use the tests 

### Running individual test 

- To run test by unittest: `python LoginPageTCs.py TestLoginPage.test_TC001_default_login`

### Running the suite 

- To run suite by unittest: `python suite_all_tests.py -v`
- To run suite by pytest:   `pytest suite_all_tests.py -v`
- To generate html-report:  `pytest --html=report.html suite_all_tests.py`

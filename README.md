# Selenium automation of openAttic ses5 qa tests 

[**Test Case Definitions**](https://github.com/markostanojlovic/ses5_oa_qa/wiki/Test-Case-Definitions)

## Requirements :

- Chrome browser + webdriver
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
### Selenium Webdriver for Firefox 
 

## How to use the tests 

### Running individual test 

- To run test by unittest (*obsolete*): `python LoginPageTCs.py TestLoginPage.test_TC001_default_login` 

### Running the suite 

- To run all test by pytest:   `pytest -v`

### HTML report 

This takes all defined test in all files with prefix "test_":

`pytest -v --html=pytest_report.html --self-contained-html`

Copy the html report to location of the html server, for example: 

`sudo cp pytest_report.html /usr/share/nginx/html/`

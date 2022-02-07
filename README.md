# Medicine Shop Automation Software by CodeCannibals

## About the software


The Medicine Shop Automation Software’s purpose is to automate Medicine Shop management and ease the shop owner’s workload. It is a convenient and easy-to-use application for the shop owner who has to deal with managing the medicine shop’s inventories and undergo various types of procedures involving transactions with vendors of the medicines and customers who buy the medicines. The system is based on a relational database with its Medicine Inventory and Transaction Records. It can handle efficient storage of data and provides the user with various functionalities. Above all, the software aims to provide a comfortable user experience to the medicine shop owners.


## Pre-requisites


Python must be installed on your computer. Go to [link](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu) to get detailed instructions for installing the latest version of python on the Linux platform.


Django must be installed on your computer. Go to [link](https://www.digitalocean.com/community/tutorials/how-to-install-the-django-web-framework-on-ubuntu-20-04) to get detailed instructions for installing the latest version of Django on the Linux platform.


A [browser](https://www.google.com/aclk?sa=l&ai=DChcSEwj32_KpxOfvAhVR10wCHUl8CPEYABABGgJ0bQ&sig=AOD64_1JzL_elPFDLixEd5Ikf0ZpdVSyQA&q&adurl&ved=2ahUKEwjOouqpxOfvAhWloekKHXtRAjgQ0Qx6BAgDEAE) must be installed in order to run the software.


### For testing : 


In order to test the code, you need to install the [coverage](https://zoomadmin.com/HowToInstall/UbuntuPackage/python3-coverage) package. A simple command as below should work or you may go to the link for further installation instructions.



```bash
pip install coverage
```
## Installation


Download the project's source file from Moodle Website. Then go to the command line and enter into the directory in which you have downloaded the files.

```bash
cd Downloads
```
Then change your directory to the msa folder.

```bash
cd msa
```

Then run the following commands step by step.

```bash
python manage.py runserver
```
This will open the software in your browser. Use the details below in order to log in and use the software, you can change the password later.

#### Username : admin
#### Password : hello


### [Optional] Create new user:
 
```bash
python manage.py createsuperuser
```
You will be asked to enter your username, email, and password. Please do so in order to create a super user successfully. After that run the command below and proceed with the new login details.

```bash
python manage.py runserver
```

## Usage

The software is completely self-explanatory.

## Testing

Go to the directory of the software having the manage.py file.


```bash
cd Downloads/msa
```
In this directory, run the following commands in order to automatedly test the software.

The below command runs all the test cases.

```bash
coverage run manage.py test
```
The below command gives the coverage report.

```bash
coverage report
```
The below command generates an index.html that can be opened in the browser which gives a detailed report of all the tests performed.

The index.html file is provided along with the software. This file is generated on our side.

```bash
coverage html
```

The above command also generates such a file. It is located in 
```bash
msa/htmlcov/index.html
```

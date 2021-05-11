# vaccine_slot_finder
This project can be used to send alert when a vaccine slot is available at your pincode.

**Speciality of this project**:
This project uses private VM(free Amazon ec2 instance) and Amazon SES which is very trustworthy
for real time email alert receiving.

The logic is available in vaccine_slot_finder.py which can be modified as per need. The current
flow is that if any slot is available at a particular pincode for tommorrow's date, you will be
notified on your mail id. Then, you can book the vaccine slot for your loved ones.

**How to run this code:**
1) As this runs on a free EC2 instance, please create and run an instance on AWS where region must
be "ap-south-1", otherwise the requests are being blocked by API and you will receive a 403 Error.
Configure your AWS CLI with the base details like AWS Access Key ID, AWS Access Secret key and more.
Have a look for how to configure AWS CLI:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html
Verify whether python3 is installed or not. 
Use this command in AWS CLI: ```python3 --version```

Create a virtual python environment using command:
```python3 -n venv <Directory_name>```
Activate the virtual environment which is created using previous command:
```source <Directory_name>/bin activate```

2) As we use Amazon SES(free for first 62,000 mails per month), 
Verify the TO and FROM Email addresses which you want to use for sending and receiving email alerts.
Please have a look here for How to verify emails on Amazon SES:
https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html

3) Clone this repo:
```git clone https://github.com/nishummehta/vaccine_slot_finder.git```
or you can use other ways as well.

4) Install the requirements 
```pip install -r requirements.txt```

5) Run the python tool using command:
```nohup python vaccine_slot_finder.py --pincode <your_pincode(127021)> --sender_email 12@abc.com --receiver_emails_comma_seperated 34@abc.com,56@abc.com > vaccine_slot_finder_logs &```
Make sure to add "**&**" at the end of python command to run the tool in background.

Sit back and relax. Wait for your notifier to inform you about the available slot.
Book you vaccine from Arogya Setu app when you are notified. Till that time, be at home and be safe.

**Useful resources:**
**How to send a mail using BOTO3 and AMAZON SES**
https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html

**API Setu page where you can the cowin APIs**
https://apisetu.gov.in/public/api/cowin


Feel free to contact me if you found this code to be non working or you encounter any bug.
Email id: nishummehta1997@gmail.com

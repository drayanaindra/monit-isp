import os
import re
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

# set your directory for log or anything when you wanna say fuck
SET_DIR = os.path.dirname(os.path.abspath(' '))
NAME_FILE = 'log-myisp.txt' # custom your file name
FULL_PATH_DIR = SET_DIR + '/' + NAME_FILE
MIN_DOWN = 256 # in Kbps

# setup smtp mail
# confirm activation application in here https://accounts.google.com/b/0/DisplayUnlockCaptcha
# turn on Less secure apps in here https://www.google.com/settings/security/lesssecureapps
MAIL_ADDRESS = '' # your mail
MAIL_TARGET = '' # your target mail
PASSWORD_EMAIL = '' # your password mail

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
print 'login mail'
server.login(MAIL_ADDRESS, PASSWORD_EMAIL)

# setup email
msg = MIMEMultipart()
msg['From'] = MAIL_ADDRESS
msg['To'] = MAIL_TARGET
msg['Subject'] = "[REPORT] PT. Angsa Maen Kuda"
body = """
      Halo bro,
      Halo this is my auto report when download rate is bitch
      
      Regards,
      Saitama
      """

print 'Do Speedtest'
create_log = os.system('speedtest-cli --share > {isp}'.format(isp=FULL_PATH_DIR))

with open(NAME_FILE, "r") as mylog:
  string_log = mylog.read().replace('\n', '')
  
get_down_bit = re.search('Download: (.+?) Mbit', string_log)
to_int_bit = float(get_down_bit.group(1))
# conver to kbps
convert_to_kbps = to_int_bit * 1024

if convert_to_kbps <= MIN_DOWN:
  print 'send mail'
  attachment = open(FULL_PATH_DIR, "rb")
  msg.attach(MIMEText(body, 'plain'))
  
  part = MIMEBase('application', 'octet-stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  
  part.add_header('Content-Disposition', "attachment; filename= %s" % NAME_FILE)
  msg.attach(part)
  text = msg.as_string()
  
  server.sendmail(MAIL_ADDRESS, MAIL_TARGET, text)
  server.quit()

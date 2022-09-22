import smtplib
import dbconnector
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
load_dotenv()


try:
    standarts = dbconnector.loadStandarts()
    result = dbconnector.GetWrongDefinitions(standarts[0], os.getenv("UYGULAMA_LIKE"))
    result += dbconnector.GetWrongDefinitions(standarts[1], os.getenv("VERITABANI_LIKE"))
    result += dbconnector.GetWrongDefinitions(standarts[2], os.getenv("DREAM_LIKE"))
    result += dbconnector.GetWrongDefinitions(standarts[3], os.getenv("TURIZM_LIKE"))
    result += dbconnector.GetWrongDefinitions(standarts[4], os.getenv("DIJITALCOZUM_LIKE"))
    result += dbconnector.GetWrongDefinitions(standarts[5], os.getenv("MOBILITE_LIKE"))
    result += dbconnector.GetWrongDefinitions(standarts[6], os.getenv("DEPOLAMA_LIKE"))
    result += dbconnector.GetWrongDefinitions(standarts[7],os.getenv("BILGI_LIKE"))



    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Değiştirilmesi Gereken Responsible Listesi"
    msg['From'] = os.getenv("FROM_PART")
    msg['To'] = os.getenv("TO_PART_GIVEN_TEAM")
    msg['Cc'] = os.getenv("CC_PART")

    #Create your SMTP session
    smtp = smtplib.SMTP(os.getenv("IP_SMTP"), os.getenv("PORT_SMTP"))

   #Use TLS to add security
    #smtp.starttls()

    #Defining The Message

    Standart = ""

    for i in len(standarts):
        Standart += "<li> {} </li>".format(standarts[i])

    Content_Title = "Değiştirilmesi gereken kısımlar aşağıda belirtilmiştir, <br> <hr> Standartlar Ekipler için: <br> {} <br> şeklindedir.<br><br>".format(Standart)

    Content_End = "<br><br> Bu mail otomatik olarak <b>{}</b> tarihinde gönderilmiştir. <br><br>".format(datetime.now().date())

    Mail_Content = Content_Title + """<table><tr><th style="border-style: solid; border-color: black;">Server Name</th><th style="border-style: solid; border-color: black;">Responsible</th></tr>{}</table>"""

    tableItem = ""

    for obj in result:
        tableItem += "<tr><td  style='border-style: solid; border-color: gray;'>{}</td><td  style='border-style: solid; border-color: gray;'>{}</td></tr>".format(obj.serverName, obj.responsible)
    
    Mail_Content = Mail_Content.format(tableItem)

    Mail_Content += Content_End

    Mail_Content_Part = MIMEText(Mail_Content, 'html')

    msg.attach(Mail_Content_Part)


    #Sending the Email
    smtp.sendmail(os.getenv("FROM_PART"), [os.getenv("TO_PART")]+[os.getenv("TO_PART_GIVEN_TEAM")]+[os.getenv("CC_PART")],msg.as_string())
    
    #Terminating the session
    smtp.quit()
    print ("Email sent successfully!")
    lines = ["Responsiblity Checker", 'E-Mail: Sent Successfuly to {}:_{}'.format(os.getenv("PLATFORM_EKIP"),datetime.now().date())]
    with open('Responsiblity Sender Info_{}.txt'.format(datetime.now().date()), 'w') as f:
        for line in lines:
            f.write(line)
            f.write('\n')
except Exception as ex:
    errorlines=["Responsiblity Checker", 'E-Mail: Sent Failed to {}:_{}'.format(os.getenv("PLATFORM_EKIP"),datetime.now().date())]
    print("Something went wrong....",ex)
    with open('Responsiblity Sender Info_{}.txt'.format(datetime.now().date()), 'w') as f:
        for line in errorlines:
            f.write(line)
            f.write('\n')

from urllib.request import Request, urlopen
import requests
import re
from xml.dom import minidom
from xml.sax.saxutils import escape
import csv
import os.path

#run anonymous code 
def runApexCode(apexCode, sessionId, instanceURL, orgId):
    endpoint = '{}/services/Soap/s/43.0/{}'.format(instanceURL,orgId)
    xmlData = """ 
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:apex="http://soap.sforce.com/2006/08/apex">
            <soapenv:Header>
            <apex:DebuggingHeader>
                <apex:categories>
                    <apex:category>Apex_code</apex:category>
                    <apex:level>FINE</apex:level>
                </apex:categories>
                <apex:debugLevel>DETAIL</apex:debugLevel>
            </apex:DebuggingHeader>
            <apex:SessionHeader>                   
                <apex:sessionId>{}</apex:sessionId>
            </apex:SessionHeader>
            </soapenv:Header>
            <soapenv:Body>
            <apex:executeAnonymous>
                <apex:String>{}</apex:String>
            </apex:executeAnonymous>
            </soapenv:Body>
        </soapenv:Envelope> 
    """.format(sessionId, escape(apexCode))
    headers  = {'Content-Type':'text/xml','SOAPAction':'""'}
    result = requests.post(endpoint, data=xmlData, headers=headers)   
    responseDOM = minidom.parseString(result.text)
    compiled = responseDOM.getElementsByTagName('compiled')[0].firstChild.data
    if compiled == 'false':
        raise Exception('Compilation Error : '+responseDOM.getElementsByTagName('compileProblem')[0].firstChild.data)
    success = responseDOM.getElementsByTagName('success')[0].firstChild.data
    if success == 'false':
        raise Exception('Runtime Error : ' +responseDOM.getElementsByTagName('exceptionMessage')[0].firstChild.data)
    debugLog = responseDOM.getElementsByTagName('debugLog')
    log = debugLog[0].firstChild.data
    return log
from urllib.request import Request, urlopen
import requests
from xml.sax.saxutils import escape
import os.path

def sayHello():
    print('This is from kmlib.py inside sayHello')

def getAccessTokenByCode(code,testVsLogin,clientId,secreteKey):
    endpoint = 'https://{}.salesforce.com/services/oauth2/token'.format(testVsLogin)
    requestBody =   """client_id={}
                       &redirect_uri=https%3A%2F%2Fsflab-python-api.herokuapp.com%2Foauth%2Fcallback
                       &client_secret={}
                       &grant_type=authorization_code&format=json
                       &code={}""".format(clientId,secreteKey,code)
    headers  = {'Content-Type':'application/x-www-form-urlencoded'}
    print(requestBody)
    result = requests.post(endpoint, data=requestBody,headers=headers)      
    print(result.json()['access_token'])
    return result.json()['access_token']

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


if __name__ == '__main__':
    getAccessTokenByCode('aPrxbOND3gL_2LZoaVgHqSAwlP71Jzl2EjcscB3ouWxkzpBdAN3C_ATbmDxJiTzfTz_y.8bHbw==','login','3MVG9g9rbsTkKnAWoqLITQr6PwYP.OzzCi2qpJ4FvKRHOUeti9_o6zvqUSDS.2LroT52i5nLzdZkxvgu6O0J9','5447957181350656860')
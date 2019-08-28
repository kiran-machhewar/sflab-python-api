from urllib.request import Request, urlopen
from simple_salesforce import Salesforce
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

def getUserInfo(sessionId,testVsLogin):
    headers = {'Accept': 'application/json'}
    response = requests.get('https://'+testVsLogin+'.salesforce.com/services/oauth2/userinfo?access_token='+sessionId,headers=headers)           
    return response.text 

def getSObjectIds(query,sessionId,instanceURL,batchSize):    
    sf = Salesforce(instance_url=instanceURL, session_id=sessionId)
    result = sf.query_all(query)
    sobjectIds = []
    subsetRecordIds = []
    index = 0
    for record in result['records']:
        if index < batchSize:
            subsetRecordIds.append(record['Id'])
            index = index + 1
        if index == batchSize:
            index = 0
            sobjectIds.append(subsetRecordIds)
            subsetRecordIds = []
    sobjectIds.append(subsetRecordIds)
    return sobjectIds

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

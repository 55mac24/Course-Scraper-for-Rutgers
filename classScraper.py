import requests
import json
from lxml import html

courseOfferingsId = []
webReg = open("WebRegCourses.txt","r")
g = ""
flag = False
for line in webReg.readlines(): #Parses txt file with all courses to add to list
    for j in line:
        if(j == ')'):
            courseOfferingsId.append(g)
            g = ""
            flag = False
        elif(flag):
            g = g + j
        elif( j == '('):
            flag = True
webReg.close()

#print ('[%s]' % ', '.join(map(str, courseOfferingsId)))

loginUrl = ""
for course in courseOfferingsId: #Performs login authentication and downloads courses in JSON format

    link = "https://sims.rutgers.edu/csp/sectionsLookup.json?semester=92018&campus=NB&levelOfStudy=U&subject="+course

    courseSession = requests.session()
    paramaters = {'service': link}
    loginUrl = "https://cas.rutgers.edu/login?service=https%3A%2F%2Fsims.rutgers.edu%2Fcsp%2Fj_spring_cas_security_check"
    login = courseSession.get(loginUrl, params=paramaters)
    loginTree = html.fromstring(login.content)
    loginAuth = loginTree.xpath(r'//form//input[@type="hidden"]') #find all hidden authentication attributes to add to the payload
    payload = {x.attrib["name"]: x.attrib["value"] for x in loginAuth}

    #print(payload)

    payload['username'] = "" #your netID goes here
    payload['password'] = "" #your password goes here


    response = courseSession.post(loginUrl,data=payload, params=paramaters) #Payload and parameters needed to complete HTTP request
    grabJSON = courseSession.get(link)
    data = grabJSON.json()

    #print(response.url)
    #print(grabJson.text)

    fileName = course+'.json'
    with open(fileName, 'w') as outfile:
        json.dump(data, outfile,indent=2) #Writes Formatted JSON file




import requests
import json
from time import sleep
from os import system
from sys import platform
#from mytts import audio_read


commands = {'win32':'cls','linux':'clear','linux2':'clear','darwin':'clear'}

# Clear console screen
def clear():
    if platform in commands:
        system(commands[platform])
    else:
        raise OSError("Uncompatible Operating-System.")
    print("...")




link = "https://portail.if-algerie.com/"
login = link + "login"
home = link + "home"
rdv = link + "exams"
getdays = rdv + "/getdays"
reserve = rdv + "/reserve"

keywords = (
    "uid",
    "title",
    "start",
    "duration",
    "minutes",
    "className",
    "level",
    "price",
    "antenna_name",
    "antenna_id",
    "local",
    "status",
    "full"
)

dap = "TCF dans le cadre de la DAP"
so = "TCF SO"
canada = "TCF Canada"


# Fill these cookies according to your IFA account
# You can get them by inspecting element in portail.ifa-algerie.com (when logged in)
# Then Application > Storage > Cookies
cookies_ = {
    #'_ga':'' ,  (Old version)
    #'_fbp' : '',(Old version)
    'cf_clearance': '',
    'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d' : '', # the hash after 'remember_web_' can be different
    'XSRF-TOKEN' : '', 
    'ifa_session' : '',
    '__cf_bm': ''
}


# You can get the X-CSRF-TOKEN from inspecting element
# Then Elements >
# <head>
#   <meta name="csrf-token" content="here is where you find the token">
# copy the 'content' attribute's value and paste it in this dictonary..

x = {'X-CSRF-TOKEN': ' '}

# Fill this tuple with TCF Types that you're Trying to get
# Examples : so, dap, canada
Desired_TCF_Types = (dap, so)

AlgDA = lambda seance: seance['antenna_name']=="IF Alger" and seance['title'] in Desired_TCF_Types

lambdaFree = lambda seance: seance['full']=='0'

def do_getdays(sessionVar, uid):
    return sessionVar.post(getdays, data={"uid":uid, "service_type":"EX"} , headers=x )

endstring_old = "console.log(defaultEvents)"
endstring = "var $this = this;"
class IFA:
    def __init__(self, icode) :
        self.code = icode
        jsData = self.code[self.code.index("var defaultEvents")+21:self.code.index(endstring)-7]
        # JSONifying the JavaScriptArray
        FixedJS = jsData[:-15]+ jsData[-14:]
        for keyword in keywords:
            FixedJS = FixedJS.replace(keyword, '"{}"'.format(keyword))
        # JSON To Python Dictionary
        self.dataList = json.loads(FixedJS)
        del FixedJS
        self.Needed = list(filter(AlgDA, self.dataList))
        self.NeededL = len(self.Needed)
        self.free = list(filter( lambdaFree, self.Needed))
        self.freeL = len(self.free)



def siyi(session_, cookies=dict(), headers=dict()):
    while True:
        try:
            return session_.get(rdv, cookies=cookies, headers=headers).text
        except:
            print('Connection Error.')


def main():
    i = 0
    success = False
    session = requests.session()
    code = siyi(session, cookies=cookies_, headers=x)
    while True:
        i+=1
        if "error-body" in code:
            print("Error. Trying again...")
        elif "<title>Error</" in code:
            print("Too many requests !")
        elif "<h1>500</h1>" in code:
            print("Error 500.")
        elif "Se souvenir de moi<" in code:
            print("Cookies Expired.")
        else:
            instance = IFA(code)
            print( "{}/{} are free.".format(instance.freeL, instance.NeededL) )
            if instance.freeL != 0 :
                print("\nRendez-Vous Disponibles\n"*3)
                for seance in instance.free:
                    answer = do_getdays(session, seance['uid'])
                    try:
                        json_res = answer.json()
                        if json_res['success']==True:
                            print(json_res)
                            print("Azzel " + seance['title'])
                            success = True
                            #audio_read('dual.mp3')
                            break
                        else:
                            print("Places Indisponibles.")
                    except json.decoder.JSONDecodeError :
                        print("No JSON response.")
                if success: break
        print("----------{}----------".format(i))
        sleep(0.1) # Interval between requests
        clear()
        code = siyi(session)
    input("\nOut of while loop.\n")
#
if __name__=='__main__':
    main()

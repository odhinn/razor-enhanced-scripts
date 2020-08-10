##############################################################################################
#                                 Pet Intensity Calculator                                   #
##############################################################################################
# Author    : Odhinn                                                                         #
# Server    : Quingis UO | htttp://www.quingis.com                                           # 
# Info      : This script lets you get intensity value of newly tamed pet. It will save      #
#             log file and also copy planner link into clipboard.                            #
# Usage     : If you do not have IronPython on your system, just download it from            #
#             https://ironpython.net/ and install. And also if you have portable version of  #
#             IronPython, you can set the path manually.                                     #
#             Just run the script and you will get the result.                               #
# Warning   : If you want to use it on your current pets, you have to change their name to   #
#             original. You do not have to put "a" or "an" before the name.                  #
#             You can decide enable/disable logging,clipboard and also notifications inside  #
#             the script under USER SETTINGS comment.                                        #
# Source    : All datas come from www.uo-cah.com                                             #
##############################################################################################

import clr
import string
import System
from System.Threading import Thread, ThreadStart
clr.AddReference("System.Windows.Forms")
from Microsoft.Win32 import Registry,RegistryKey,RegistryHive,RegistryView
import datetime
import sys
localKey = RegistryKey.OpenBaseKey(RegistryHive.LocalMachine, RegistryView.Registry64)
paths = localKey.OpenSubKey("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Installer\\Folders").GetValueNames()   
ironPython=[i for i, s in enumerate(paths) if 'IronPython' in s and 'Lib' in s]
sys.path.append(paths[ironPython[0]])
#Or you can do it manually. 
#for example:
#sys.path.append(r'C:\Program Files\IronPython 2.7\Lib') # Set your default path of IronPython library
import urllib2
import os.path

#USER SETTINGS
cancelORcontinue = True # True: stop after cancelation | False: ask for new target after cancelation 
enableLogging = True
enableClipboard = True 
loggingNotification= True 
clipboardNotification= True 
#END OF USER SETTINGS

pointPerSlotLeft = 1501    
stringIR='Intensity Rating: <strong>'
endIR = '%</strong>'
stringIV= 'Intensity Value: <strong>'
endIV = '</strong></div></td></tr><tr>'
stringIRange = 'Intensity Range: '
endIRange= '</td></tr></tbody></table>'
stringPlanner = '<a href="/pet-planner?'
#"
endPlanner = '"><img style="border-radius:25px;" src="/sites/default/files/creatures/petplanner.png"/>'
#"
petBodies = [246,794,1423,232,233,1510,1511,60,61,1419,1420,277,242,1285,23,12,59,719,11,116,1440,169,190,1424,20,1286,248,791,793,98,201,715,243,714,132,1407,206,1426,1289,177,178,179,1425,832,1417,1418,730,276,244,1416,1291,103,106,1441,733,734,1422,1415,720,250,122,293,180,49,1254,1255,1410]

def getName(tMobile):
     getInfo = (string.capwords(Mobiles.FindBySerial(tMobile).Name)).replace(" ","+")
     if getInfo[0:2]=="A+" or getInfo[0:3]=="An+":
         return getInfo[getInfo.index("+")+1:]
     else:
         return getInfo
         
def writeLog(url,planner,name):
     petLog = Misc.CurrentScriptDirectory() + "\\pet_intensity_calculator_log.txt"
     current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
     logHeader="################# PET INTENSITY CALCULATOR LOG FILE #################\n\n"
     strHeader= "[ "+current_time+" ] - ############### "+name+" ###############"
     strFooter="\n\n"+"#"*len(strHeader)+"\n\n"
     file = open(petLog,"a+")
     if(os.stat(petLog).st_size == 0):
         file.write(logHeader)
     file.write(strHeader)
     file.write("\n\n[ UO-CAH INTENSITY CALCULATOR URL ]\n\n"+url)
     file.write("\n\n[ UO-CAH PET PLANNER URL ]\n\n"+planner)
     file.write(strFooter)
     file.close()
     if loggingNotification:
         Misc.SendMessage("Pet data has been successfully saved into log file.",1196)
     
def getClipboard(url):
    def thread_proc():
        System.Windows.Forms.Clipboard.SetText(url)

    t = Thread(ThreadStart(thread_proc))
    t.ApartmentState = System.Threading.ApartmentState.STA
    t.Start()
    if clipboardNotification:
        Misc.SendMessage("Pet Planner URL has been copied to your clipboard.\nPaste it into the browser's address bar.",1196)    
        
def calculateIt(target):

     Gumps.WaitForGump(0,10000)

     myList = Gumps.LastGumpGetLineList()
     if myList[0] != "Attributes":
       Gumps.SendAction(Gumps.CurrentGump(),0)
       calculateIt(target)

     req = [i for i, s in enumerate(myList) if '<center>' in s]
     del myList[0:req[0]] 

     petType = getName(target)    
 
     if len(Mobiles.FindBySerial(target).Properties) > 1: 
        val_Hits = myList[1][myList[1].find('/') + 1: myList[1].find('</')]
        val_Stamina= myList[2][myList[2].find('/') + 1: myList[2].find('</')]
        val_Mana= myList[3][myList[3].find('/') + 1: myList[3].find('</')]
        val_Strength= myList[4][myList[4].find('>') + 1: myList[4].find('</')]
        val_Dexterity= myList[5][myList[5].find('>') + 1: myList[5].find('</')]
        val_Intelligence= myList[6][myList[6].find('>') + 1: myList[6].find('</')]
        val_Physical= myList[11][myList[11].find('>') + 1: myList[11].find('%</')]
        val_Fire = myList[12][myList[12].find('t>') + 2: myList[12].find('%</')]
        val_Cold = myList[13][myList[13].find('t>') + 2: myList[13].find('%</')]
        val_Poison = myList[14][myList[14].find('t>') + 2: myList[14].find('%</')]
        val_Energy = myList[15][myList[15].find('t>') + 2: myList[15].find('%</')]
        val_Wrestling = '0' if not myList[22][myList[22].find('/') + 1: myList[22].find('</')] else myList[22][myList[22].find('/') + 1: myList[22].find('</')]
        val_Tactics = '0' if not myList[23][myList[23].find('/') + 1: myList[23].find('</')] else myList[23][myList[23].find('/') + 1: myList[23].find('</')]
        val_ResistingSpells = '0' if not myList[24][myList[24].find('/') + 1: myList[24].find('</')] else myList[24][myList[24].find('/') + 1: myList[24].find('</')]
        val_Poisoning = '0' if not myList[27][myList[27].find('/') + 1: myList[27].find('</')] else myList[27][myList[27].find('/') + 1: myList[27].find('</')]
        val_Magery = '0' if not myList[31][myList[31].find('/') + 1: myList[31].find('</')] else myList[31][myList[31].find('/') + 1: myList[31].find('</')]
        val_EvalInt = '0' if not myList[32][myList[32].find('/') + 1: myList[32].find('</')] else myList[32][myList[32].find('/') + 1: myList[32].find('</')]
        val_PetSlots = myList[len(myList)-1][myList[len(myList)-1].find('>')+1:myList[len(myList)-1].find('=>')]
        val_TotalPointLeft = ((5 - int(val_PetSlots)) * pointPerSlotLeft)
        #Make sure, we get proper overcap skills. UO-CAH don not use  ',' as indicator.
        if ',' in val_Wrestling:
             val_Wrestling = val_Wrestling.replace(',','.')
        if ',' in val_Tactics:
             val_Tactics = val_Tactics.replace(',','.')
        if ',' in val_ResistingSpells:
             val_ResistingSpells = val_ResistingSpells.replace(',','.')
        if ',' in val_Poisoning:
             val_Poisoning = val_Poisoning.replace(',','.')
        if ',' in val_Magery:
             val_Magery = val_Magery.replace(',','.')   
        if ',' in val_EvalInt:
             val_EvalInt = val_EvalInt.replace(',','.')          
        Gumps.SendAction(3644314075,0)
        url = 'https://www.uo-cah.com/pet-intensity-calculator?creature='+petType+'&hits='+val_Hits+'&stamina='+val_Stamina+'&mana='+val_Mana+'&str='+val_Strength+'&dex='+val_Dexterity+'&int='+val_Intelligence+'&physical='+val_Physical+'&fire='+val_Fire+'&cold='+val_Cold+'&poison='+val_Poison+'&energy='+val_Energy+'&target_physical=--&target_fire=--&target_cold=--&target_poison=--&target_energy=--&wrestling='+val_Wrestling+'&resistingspells='+val_ResistingSpells+'&evalintel='+val_EvalInt+'&tactics='+val_Tactics+'&magery='+val_Magery+'&poisoning='+val_Poisoning+'&mic=fresh#freshresults'

        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        rawData = response.read()
        

        intensityRating = rawData[rawData.find(stringIR)+len(stringIR) : rawData.find(endIR)]
        intensityValue = rawData[rawData.find(stringIV)+len(stringIV) : rawData.find(endIV)]
        intensityRange = rawData[rawData.find(stringIRange)+len(stringIRange):rawData.find(endIRange)]
        intensityDiff = int(intensityValue) - int(intensityRange[intensityRange.find('-')+1:])
        petPlannerRaw = rawData[rawData.find(stringPlanner)+len(stringPlanner):rawData.find(endPlanner)]
        petPlannerPoint = petPlannerRaw[petPlannerRaw.find("&22="):petPlannerRaw.find("&23=")]
        petPlannerReplaced = petPlannerRaw.replace(petPlannerPoint,"&22="+str(val_TotalPointLeft))
        petPlannerURL = "https://www.uo-cah.com/pet-planner?" + petPlannerReplaced 

        
        Misc.SendMessage("----------RESULT----------",83)
        Misc.SendMessage((petType.replace("+"," ")).upper(),38)
        Misc.SendMessage("----------------------------",83)
        Misc.SendMessage("Intensity Rating : {0}%".format(intensityRating),1196)
        Misc.SendMessage("Intensity Value :   {0}".format(intensityValue),1196)
        Misc.SendMessage("Range :   {0}".format(intensityRange),1196)
        Misc.SendMessage("Cap Diff. :  {1} {0}".format(str(intensityDiff).replace("-","") if intensityDiff < 0 else intensityDiff,"Minus" if intensityDiff < 0 else "Plus"),1196)
        Misc.SendMessage("----------------------------",83)
        if enableLogging:         
            #Logging url and also planner url into file so u can check it later.
            writeLog(url,petPlannerURL,petType.replace("+"," ").upper())
        if enableClipboard:
             getClipboard(petPlannerURL)
     else:
         Gumps.SendAction(3644314075,0)
         Misc.SendMessage("This pet is wild, use on newly tamed pet.",38)
         Misc.Pause(1000)
         Main()    
        
def Main():
    target = Target.PromptTarget("Select your newly tamed pet.")
    if target == -1:
        if cancelORcontinue:
            Misc.SendMessage("Have a nice day!",1196)
        else:
            Misc.Pause(1000)
            Main() 
    else:
        Player.UseSkill("Animal Lore")
        Target.WaitForTarget(5000)
        Target.TargetExecute(target)
        try:
            targetBody = Mobiles.FindBySerial(target).Body
        except:
            Misc.SendMessage("This is not a pet.",38)
 
        if targetBody in petBodies:
             calculateIt(target)
        else:
             Misc.SendMessage("This pet isn't supported by this script or uo-cah doesn't have any information about it.",38)
             if cancelORcontinue:
                 Misc.SendMessage("Have a nice day!",1196)
             else:
                 Misc.Pause(1000)
                 Main()
            

Main()

##############################################################################################
#                     PVP - Chaining Magic Arrow and Fireball with Harm                      #
##############################################################################################
# Authors   : Odhinn, Mourn                                                                  #
# Server    : Quingis | htttp://www.quingis.com                                              # 
# Info      : This script let you chaining Magic Arrow and Fireball and cast Harm spell      #
#             if you close to enemy. There is no rapid repetition of magic arrow so spamming #
#             it useless except initial hit.                                                 #
#             So we are combining it with Fireball, Magic Arrow chain. You can also use this #
#             for fizzle your oppenent while doing some moderate damage.                     #
#                                                                                            #
# Usage     : Assign Hotkey and use it. You can spam while pressing the key.                 #
# Warning   : You have to enable "Wait before interrupt" in Scripting/Script Info            #
# Source    : This script converted from UOSteam to Razor Enhanced                           #
##############################################################################################


SharedDataName = "Magic Arrow"

if not Misc.CheckSharedValue(SharedDataName):
    Misc.SetSharedValue(SharedDataName,"Magic Arrow")

def controlSpell():
    return Misc.ReadSharedValue(SharedDataName)

    
def checkPoint(spell):
    Misc.SetSharedValue(SharedDataName,spell)

enemy = Target.GetLast()

if Player.InRangeMobile(enemy,10):
    if Player.InRangeMobile(enemy,1):
        Spells.CastMagery('Harm',enemy)
    else:
        spellcast = controlSpell()
        
        Spells.CastMagery(spellcast)
        Target.WaitForTarget(5000,True)
        Target.TargetExecute(enemy)

        
        if controlSpell() == "Magic Arrow":
           checkPoint("Fireball")
        else:
           checkPoint("Magic Arrow")
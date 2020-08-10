##############################################################################################
#                           PVP - Warrior Follow the Enemy                                   #
##############################################################################################
# Author    : Odhinn                                                                         #
# Server    : Quingis | https://www.quingis.com                                              # 
# Info      : For catching last targeted enemy. Runing behind the enemy and if it gets enemy #
#             it will use weapon ability.                                                    #
# Usage     : Assign Hotkey. Whenever it gets the enemy you will see use your hotkey message.#
##############################################################################################


target = Target.GetLast()
Player.WeaponPrimarySA()
Player.Attack(target)

while True:
    if Player.InRangeMobile(target,0):
        Misc.SendMessage("Target Caught, reuse your hotkey.",1196)
        break
    else:
        Player.PathFindTo( Mobiles.FindBySerial(target).Position.X,Mobiles.FindBySerial(target).Position.Y,Mobiles.FindBySerial(target).Position.Z)
    Misc.Pause(50)

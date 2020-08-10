##############################################################################################
#                           Clean-Up Ingot and Gem Calculator                                #
##############################################################################################
# Author    : Odhinn | https://www.github.com/odhinn                                         #
# Server    : Quingis UO | http://www.quingis.com                                            # 
# Info      : It will calculate the points when targeted the source or container.            #
# Usage     : Just run the script and select source or container. It can calculate single    #
#             resource or full of container.                                                 #                    
##############################################################################################

ingots = {
  "iron" :{"point":0.10},
  "dull copper":{"point":0.50},
  "shadow iron":{"point":0.75},
  "copper":{"point":1},
  "bronze":{"point":1.50},
  "golden":{"point":2.50},
  "agapite":{"point":5},
  "verite":{"point":8.50},
  "valorite":{"point":10}
}
gems = {
   "0x3192" : {"name":"dark saphhire",
       "point": 25},
   "0x3193" : {"name":"turquoise",
       "point": 25},
   "0x3194" : {"name":"perfect emerald",
       "point": 25},
   "0x3198" : {"name":"blue diamond",
        "point": 25},
   "0x3197" : {"name":"fire ruby",
        "point": 25},
   "0x3195" : {"name":"ecru citrine",
        "point": 25},
   "0xF28" : {"name":"a small piece of blockrock",
        "point": 10}   
}

def getName(item):
    if getID(item) in gems:
        result = str(Items.FindBySerial(item).Properties[0])
        result = result.replace(str(Items.FindBySerial(item).Amount)+' ','')
        return result
    elif getID(item) == "0x1BF2":
      if len(Items.FindBySerial(item).Properties) == 2:
        return "iron"
      else:
        return str(Items.FindBySerial(item).Properties[2])
    else:
        return ""
        
def getItemName(item):
    if len(item.Properties) == 2:
        return "iron"
    else:
        return str(item.Properties[2])
    
def getAmount(item):
    return Items.FindBySerial(item).Amount

def getItem(item):
    return Items.FindBySerial(item)
    
def getID(item):
    return "0x{:02X}".format(getItem(item).ItemID)
    
def getPoint(item):
    if getID(item) in gems:
        return gems.get(getID(item)).get("point")
    elif getID(item) == "0x1BF2":
        return ingots.get(getName(item)).get("point")
    else:
        return 0
    
def pointCalc(item):
    return "{0} amounts of {1} = {2} points".format(getAmount(item),getName(item),int(getAmount(item)*getPoint(item))) 

def pointCalcCont(box):
    points = 0
    for Item in getItem(box).Contains:
        if "0x{:02X}".format(Item.ItemID) == "0x1BF2":
            points += Item.Amount * ingots.get(getItemName(Item)).get("point")
        if "0x{:02X}".format(Item.ItemID) in gems:
            points += Item.Amount * gems.get("0x{:02X}".format(Item.ItemID)).get("point")
    Misc.SendMessage("You have total {0} points worth resources.".format(points), 1196)
        

    
item = Target.PromptTarget("Select ingot, gem or container with those.")

if getItem(item).IsContainer:
    Items.UseItem(item)
    Misc.Pause(1000)
    pointCalcCont(item)
else:
    if getID(item) == "0x1BF2":
        Misc.SendMessage(pointCalc(item),1196)
    elif getID(item) in gems:
        Misc.SendMessage(pointCalc(item),1196)
    else:
        Misc.SendMessage(getID(item))
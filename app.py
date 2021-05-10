import requests
import pandas as pd 

# get item list from here https://github.com/broderickhyman/ao-bin-dumps

class ItemType:
    def __init__(self):
        self.OH = 144
        self.TH = 192
        self.ArmorBags = 96
        self.HelmetBootCapeOffHand = 48
    
    def check(self, itemName):
        itemNameSplit = itemName.split('_')
        if itemNameSplit[1] == 'OFF':
            return itemNameSplit[0], self.HelmetBootCapeOffHand

class Fee:
    def __init__(self):
        self.BuyOrder = 0.015
        self.SellOrder = 0.06
        self.SellOrderPrem = 0.03
        self.Setup = 0.015

class UpgradeParts:
    def __init__(self, level, city='Bridgewatch'):
        upgradeItem_list =[f'{level}_RUNE',f'{level}_SOUL',f'{level}_RELIC']
        query_string = ','.join(upgradeItem_list)
        upgradeParts_list = requests.get(f'https://www.albion-online-data.com/api/v2/stats/Prices/{query_string}.json?locations={city}').json()
        for item in upgradeParts_list:
            if item.get('item_id').split('_')[1] == 'RUNE': self.Rune = item.get('sell_price_min')
            if item.get('item_id').split('_')[1] == 'SOUL': self.Soul = item.get('sell_price_min')
            if item.get('item_id').split('_')[1] == 'RELIC': self.Relic = item.get('sell_price_min')
    def parts(self):
        return self.Rune, self.Soul, self.Relic

    def full_upgrade_cost(self, itemCount):
        return (self.Rune * itemCount) + (self.Soul * itemCount) + (self.Relic * itemCount)
    
    def upgrade_cost(self, itemcount, toLevel, fromLevel):
        return

class AlgoTrade:
    def __init__(self, city='Bridgewatch'):
            self.fee = Fee()
            self.itemType = ItemType()
            self.city = city
    
    def make_base_item_list(self, item_list=[]):
        query_string = ','.join(item_list)        
        base_item_list = requests.get(f'https://www.albion-online-data.com/api/v2/stats/Prices/{query_string}.json?locations={self.city}').json()
        return base_item_list

    
    def make_max_item_dict(self,item_list=[]):
        item_dict = dict()
        max_query_string = '@3,'.join(item_list)
        max_item_list = requests.get(f'https://www.albion-online-data.com/api/v2/stats/Prices/{max_query_string}.json?locations={self.city}').json()
        for item in max_item_list:
            name = item.get('item_id')
            price = item.get('sell_price_max')
            join_name = f"{name.split('@')[0]}_{item.get('quality')}"
            if price > 0:
                item_dict[join_name] = {'price': price}
        return item_dict
#######
#### Build a function to find how fast these things sell so you get that $$ quick son
#######
#######
#### Build a function to flip from one upgrade level to another one
#######
#######
#### Build a function to build furnature with a prime mule for profit
#######
# DOUBLE CHECK THESE SELL PRICE MAX ETC...
# GET THE TIME INTO THE DATAFRAME AND START STORING TRENDS
    def full_upgrade(self, item_list=[]):
        profit_list = []
        base_item_list = self.make_base_item_list(item_list)
        max_item_dict = self.make_max_item_dict(item_list)
        for item in base_item_list:
            profit_dict = dict()
            quality = item.get('quality')
            price = item.get('sell_price_max')
            itemName = item.get('item_id')
            joint_name = f"{itemName}_{quality}"
            if(joint_name not in max_item_dict) or (price == 0):
                continue
            itemLevel, upgradeItemCount = self.itemType.check(itemName)
            upgradeParts = UpgradeParts(itemLevel)
            upgradeitemCost = upgradeParts.full_upgrade_cost(upgradeItemCount)
            total_upgrade_cost = upgradeitemCost + price
            max_price = max_item_dict[joint_name].get('price')
            profit = max_price - total_upgrade_cost
            if profit > 0:
                profit_dict.update({"Item": joint_name, "Base": price, "Upgrade Cost": total_upgrade_cost, "Max Sell": max_price, "Profit": profit})
                profit_list.append(profit_dict)
                print({"Item": joint_name, "Base": price, "Upgrade Cost": total_upgrade_cost, "Max Sell": max_price, "Profit": profit})
        df = pd.DataFrame(profit_list)





if __name__ == '__main__':
    trader = AlgoTrade()
    # make this list just items no T# then check T4-T6 etc... 
    # add capturing time to this

    trader.full_upgrade(item_list=['T4_OFF_BOOK','T4_OFF_DEMONSKULL_HELL','T4_OFF_LAMP_UNDEAD','T4_OFF_JESTERCANE_HELL', 'T4_OFF_HORN_KEEPER', 'T4_OFF_ORB_MORGANA', 'T4_OFF_TORCH', 'T4_OFF_TOTEM_KEEPER'])



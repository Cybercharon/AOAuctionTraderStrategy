import requests
import pandas as pd 

# Global
ENCHANT_LVL = [1,2,3]
# rune_list = requests.get(f'https://www.albion-online-data.com/api/v2/stats/Prices/T4_RUNE,T5_RUNE,T6_RUNE,T7_RUNE,T8_RUNE.json?locations={city}').json()
# req = requests.get(f'https://www.albion-online-data.com/api/v2/stats/History/T4_RUNE,T5_RUNE,T6_RUNE,T7_RUNE,T8_RUNE?locations={city}')
# rune_list = requests.get(f'https://www.albion-online-data.com/api/v2/stats/History/T8_OFF_SHIELD@2.json?locations={city}').json()

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

    def full_kit_upgrade_cost(self, itemCount):
        return (self.Rune * itemCount) + (self.Soul * itemCount) + (self.Relic * itemCount)

class AlgoTrade:
    def __init__(self, city='Bridgewatch'):
            self.fee = Fee()
            self.itemType = ItemType()
            self.city = city
    
    
    # I need to clean up this max item list
    def make_max_item_list(self,item_list=[]):
        item_dict = dict()
        max_query_string = '@3,'.join(item_list)
        max_item_list = requests.get(f'https://www.albion-online-data.com/api/v2/stats/Prices/{max_query_string}.json?locations={self.city}').json()
        for item in max_item_list:
            # if item.get('sell_price_max_date') == '0001-01-01T00:00:00':
            #     continue
            item_dict[item.get('item_id')] = {item.get('quality'): item.get('sell_price_max')}
        return item_dict

    def full_kit_upgrade(self, item_list=[]):
        query_string = ','.join(item_list)        
        base_item_list = requests.get(f'https://www.albion-online-data.com/api/v2/stats/Prices/{query_string}.json?locations={self.city}').json()
        max_item_list = self.make_max_item_list(item_list)
        for item in base_item_list:
            if item.get('buy_price_max_date') == '0001-01-01T00:00:00':
                continue
            quality = item.get('quality')
            price = item.get('sell_price_max')
            itemName = item.get('item_id')
            itemLevel, upgradeItemCount = self.itemType.check(itemName)
            upgradeParts = UpgradeParts(itemLevel)
            upgradeitemCost = upgradeParts.full_kit_upgrade_cost(upgradeItemCount)
            total_upgrade_cost = upgradeitemCost + price            
            import ipdb
            ipdb.set_trace() 





if __name__ == '__main__':
    trader = AlgoTrade()
    trader.full_kit_upgrade(item_list=['T4_OFF_BOOK','T4_OFF_DEMONSKULL_HELL','T4_OFF_LAMP_UNDEAD','T4_OFF_JESTERCANE_HELL'])



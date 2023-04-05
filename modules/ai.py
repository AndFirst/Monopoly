from modules.player import Player
from modules.constants import (BID_DIFFERENCE, DEPOSIT, DISTRICTS_SIZES,
                               MAX_PROPERTY_LEVEL)
from modules.exceptions import (AlreadyMortagedError, PropertyLevelError,
                                UnequalBuildingError)
from modules.fields import Property, BuyableField
from random import choice, randint


class AiPlayer(Player):
    '''
    A class to represent Ai contolled player. Inherits from Player class.
    Ai player is making decisions based on game and self state.

    Methods
    -------
    __init__:
        creator of class
    short_description:
        returns short description of player
    want_to_bid:
        information of player want to make a bid
    bid:
        returns players bid in auction
    pricing:
        returns player's price for his field
    want_to_buy:
        information of player want to buy a field
    earn_from_houses:
        sell houses to make player slovent
    earn_from_fields:
        sell fields to make player solvent
    want_to_stay_in_jail:
        information of player willness to stay in jail
    deposit_decision:
        decision if player want to pay deposit
    use_card_decision:
        decision if player want to use get out of card
    want_to_upgrade:
        information of player willness to build house
    count_owned_districts:
        counts fields owned by player in each district
    almost_full_district:
        returns player's almost full district (without one)
    full_districts:
        returns player's full_districts
    missing_field_id:
        check what field is needed to complet district
    missing_fields_ids:
        find missing field in each almost full district
    reply_for_pricing:
        info of player's willness of buy field from other player
    build_houses_ids:
        returns ids of fields which player want to upgrade
    '''
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)

    def short_description(self) -> str:
        '''
        Short description of Ai player.
        Adds 'AI controlled' to inherited description.
        '''
        text = super().short_description()
        text += 'AI Controlled\n'
        return text

    def want_to_bid(self, current_bid: int, field: BuyableField) -> bool:
        '''
        Decides when Ai player want to make bid in field auction.
        Willnes depends on player's money and current bid.
        Player cannot make bid if after bid he will have less than 300.
        Player do not want to buy field if its price is too high.
        '''
        if self.money() - (current_bid + BID_DIFFERENCE) < 300:
            return False
        elif current_bid + BID_DIFFERENCE > field.price():
            return False
        else:
            draw = randint(1, 10)
            if draw > 9:
                return False
            else:
                return True

    def bid(self, current_bid: int) -> int:
        '''
        Returns bid that player want to make.
        Player's bid is always as small as possible.
        '''

        bid = current_bid + BID_DIFFERENCE
        return bid

    def pricing(self, field: BuyableField) -> int:
        '''
        Returns simple pricing of Ai player field.
        Player always doubles price of buying field from bank.
        '''
        min = field.price()
        max = 2 * field.price()
        return randint(min, max)

    def want_to_buy(self, field: BuyableField) -> bool:
        '''
        Returns True if player want to buy a field.
        '''

        return self.money() - field.price() >= 300

    def earn_from_houses(self, debt: int) -> bool:
        '''
        Try to find houses on player fields and sell it.
        Until all fields are empty or needed money is collected.
        '''
        for i in range(MAX_PROPERTY_LEVEL):
            for field in self.fields().values():
                if isinstance(field, Property):
                    try:
                        field.remove_house()
                    except PropertyLevelError:
                        pass
                    except UnequalBuildingError:
                        pass
                if self.money() >= debt:
                    return True
        return False

    def earn_from_fields(self, debt: int) -> bool:
        '''
        Sell player fields until needed money is collected.
        '''
        fields = [field for field in self.fields().values()]
        for field in fields:
            try:
                self.sell_to_bank(field)
            except AlreadyMortagedError:
                pass
            if self.money() >= debt:
                return

    def want_to_stay_in_jail(self, current_round: int) -> bool:
        '''
        Decision if player want to stay in jail.
        '''
        return current_round <= 5

    def deposit_decision(self) -> bool:
        '''
        Decision of paying the deposit.
        '''
        return self.money() - DEPOSIT >= 300

    def use_card_decision(self) -> bool:
        '''
        Decision of using get out card.
        '''
        return self.get_out_cards_number() > 0

    def want_to_upgrade(self, price) -> bool:
        '''
        Decision if player want to upgrade his properties.
        '''
        return self.money() - price >= 500

    def count_owned_districts(self) -> dict:
        '''
        Counts player properties in each district.
        '''
        counter = {
            'grey': 0,
            'white': 0,
            'magenta': 0,
            'cyan': 0,
            'red': 0,
            'yellow': 0,
            'green': 0,
            'blue': 0
        }
        for field in self.fields().values():
            if isinstance(field, Property):
                counter[field.district()] += 1
        return counter

    def almost_full_districts(self) -> list:
        '''
        Create list of districts in which player has
        one missing field.
        '''
        player_districts = self.count_owned_districts()
        almost_full = []
        for district in player_districts:
            if DISTRICTS_SIZES[district] - player_districts[district] == 1:
                almost_full.append(district)
        return almost_full

    def full_districts(self) -> list:
        '''
        Create a list of player full owned districts.
        '''
        player_districts = self.count_owned_districts()
        full_districts = []
        for district in player_districts:
            if DISTRICTS_SIZES[district] == player_districts[district]:
                full_districts.append(district)
        return full_districts

    def missing_field_id(self, district: str, board: dict) -> int:
        '''
        Returns missing id from player almost owned district.
        '''
        for field in board.values():
            if isinstance(field, Property):
                if field.district() == district and field.owner() != self:
                    return field.id()

    def missing_fields_ids(self, board: dict) -> list:
        '''
        Create list of all missing fields ids.
        '''
        almost_full_districts = self.almost_full_districts()
        missing_ids = []
        for district in almost_full_districts:
            missing_ids.append(self.missing_field_id(district, board))
        return missing_ids

    def reply_for_pricing(self, field: BuyableField, price: int) -> bool:
        '''
        Reply for pricing from other player.
        '''
        pricing = randint(field.price(), 2 * field.price())
        if self.want_to_buy(field) and not price > pricing:
            return True
        else:
            return False

    def build_houses_ids(self) -> list:
        '''
        Ids of fields on which player will try to build house in current turn.
        '''
        fields = self.fields()
        full_districts = self.full_districts()
        ids = []
        if len(full_districts) > 0:
            district_color = choice(full_districts)
            for field in fields.values():
                if isinstance(field, Property):
                    if field.district() == district_color:
                        ids.append(field.id())
        return ids

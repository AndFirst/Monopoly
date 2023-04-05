from modules.constants import (MIN_NUMBER_OF_PLAYERS, MAX_NUMBER_OF_PLAYERS,
                               START_ID, JAIL_ID, PARKING_ID, GO_TO_JAIL_ID,
                               PROPERTY_IDS, TAX_IDS, STATION_IDS, SERVICE_IDS,
                               DRAW_FIELD_IDS, MIN_NUMBER_OF_ROUNDS)
from modules.fields import (Start, Jail, Parking, GoToJail, Property, Tax,
                            Station, Service, DrawField, BuyableField)
from modules.exceptions import (NotAllBancruptError, PlayersNumberError,
                                RepeatedIdError, TooShortGameError)
from random import randint
import json


class Game:
    '''
    Class Game. Backend of Monopoly game.

    Attributes:
    -----------
    _players: dict
        players in game
    _fields: dict
        fields in game
    _number_of_players: int
        number of players in game
    _number_of_rounds: int or None
        number of rounds after which game ends
    _current_player_id: int
        id of player that have turn
    _current_round: int
        number of current round
    _finished: bool
        if game finished

    Methods:
    -------
    players:
        getter
    fields:
        getter
    number_of_players:
        getter
    number_of_rounds:
        getter
    current_player_id:
        getter
    current_round:
        getter
    finished:
        getter
    set_players:
        setter
    set_fields:
        setter
    set_number_of_players:
        setter
    set_number_of_rounds:
        setter

    read_from_json:
        reads fields from json config
    create_fields:
        create fields from config
    roll_dices:
        rolls two dices
    arrest:
        put player to jail
    leave_jail:
        relase player from jail
    next_player:
        find next_player_id
    bidding_players:
        find players who can bid
    fields_for_sell:
        shows fields avaliable to buy
    reached_number_of_rounds:
        check if game finished
    one_remainded:
        check if remainded only one player
    simple_winner:
        return he who remains
    players_fortunes:
        count fortunes of players
    richest_players:
        players who have highest fortune
    debt_to_player:
        take all over from bancrupt to creditor
    remove_houses:
        remove all houses from given fields
    calculate_houses_value:
        calculate value of houses from given fields
    calculate_interests:
        calculate interests from mortged fields
    debt_to_bank;
        take all over from bancrupt to bank
    make_deal:
        buy end sell
    next_bidder_id:
        id of next bidder
    draw_card:
        choice id of chance
    '''
    def __init__(self):
        self._players = {}
        self._fields = {}
        self._number_of_players = len(self._players)
        self._number_of_rounds = None
        self._current_player_id = 0
        self._current_round = 1
        self._finished = False

    # GETTERS GETTERS GETTERS GETTERS
    def players(self) -> dict:
        '''
        Returns game's players.
        '''
        return self._players

    def fields(self) -> dict:
        '''
        Returns game's fields.
        '''
        return self._fields

    def number_of_rounds(self) -> int or None:
        '''
        Returns number of rounds.
        '''
        return self._number_of_rounds

    def number_of_players(self) -> int:
        '''
        Returns number of players.
        '''
        return self._number_of_players

    def current_player_id(self) -> int:
        '''
        Returns id of player who currently have the move.
        '''
        return self._current_player_id

    def current_round(self) -> int:
        '''
        Returns current game round.
        '''
        return self._current_round

    def finished(self) -> bool:
        '''
        Returns True if game is finished.
        '''
        return self._finished

    # SETTERS SETTERS SETTERTS SETTERS
    def set_finished(self):
        self._finished = True

    def set_players(self, players: dict) -> None:
        '''
        Set players to game.
        '''
        ids = [player.id() for player in players.values()]
        if len(set(ids)) != len(ids):
            raise RepeatedIdError()
        self._players = players

    def set_fields(self, fields: dict) -> None:
        '''
        Set fields to game.
        '''
        ids = [field.id() for field in fields.values()]
        if len(set(ids)) != len(ids):
            raise RepeatedIdError()
        self._fields = fields

    def set_number_of_players(self, number: int) -> None:
        '''
        Set number of player so new value.
        '''
        if not (MIN_NUMBER_OF_PLAYERS <= number <= MAX_NUMBER_OF_PLAYERS):
            raise PlayersNumberError
        self._number_of_players = number

    def set_number_of_rounds(self, number_of_rounds: int) -> None:
        '''
        Set number of rounds game will be played.
        '''
        if number_of_rounds is not None:
            if number_of_rounds < MIN_NUMBER_OF_ROUNDS:
                raise TooShortGameError
        self._number_of_rounds = number_of_rounds

    def read_from_json(self, handle):
        '''
        Reads fields from json config.
        '''
        all_data = json.load(handle)
        fields = {}
        for key in all_data:
            id = int(key)
            if id == START_ID:
                fields[id] = Start(all_data[key])
            if id == JAIL_ID:
                fields[id] = Jail(all_data[key])
            if id == PARKING_ID:  # parking id
                fields[id] = Parking(all_data[key])
            if id == GO_TO_JAIL_ID:  # go to jail id
                fields[id] = GoToJail(all_data[key])
            if id in PROPERTY_IDS:
                fields[id] = Property(all_data[key])
            if id in TAX_IDS:
                fields[id] = Tax(all_data[key])
            if id in STATION_IDS:
                fields[id] = Station(all_data[key])
            if id in SERVICE_IDS:
                fields[id] = Service(all_data[key])
            if id in DRAW_FIELD_IDS:
                fields[id] = DrawField(all_data[key])
        fields = dict(sorted(fields.items()))
        self.set_fields(fields)

    def create_fields(self, path):  # WORKS
        '''
        Creates fields from config file.
        '''
        with open(path) as handle:
            self.read_from_json(handle)

    def roll_dices(self):
        '''
        Rolls dices and add double if two dices are equal.
        '''
        player = self.players()[self.current_player_id()]
        result = player.dices()
        if result[0] == result[1]:
            player.add_double()
        else:
            player.reset_doubles()
        return result

    def arrest(self, player):
        '''
        Puts player to jail.
        '''
        player.reset_doubles()
        jail = self.fields()[JAIL_ID]
        jail.add(player)
        player.go_to_jail()

    def leave_jail(self, player):
        '''
        Relase player from jail.
        '''
        jail = self.fields()[JAIL_ID]
        jail.relase(player)
        player.leave_jail()

    def next_player(self):
        '''
        Find next player who is not a bancrupt.
        '''
        found = False
        while not found:
            self._current_player_id += 1
            id = self.current_player_id()

            if id != id % self.number_of_players():
                self._current_round += 1
            self._current_player_id %= self.number_of_players()
            id = self.current_player_id()
            found = not self.players()[id].is_bancrupt()

    def bidding_players(self):
        '''
        Return players who can take part in auction.
        '''
        bidding_players = {}
        for player in self.players().values():
            current_id = self.current_player_id()
            if not (player.id() == current_id or player.is_bancrupt()):
                bidding_players[player.id()] = player
        return bidding_players

    def fields_for_sell(self):
        '''
        Shows fields that can be sold.
        '''
        sellable_fields = {}
        player = self.players()[self.current_player_id()]
        for field in self.fields().values():
            if isinstance(field, BuyableField):
                if field.owner() is not None and field.owner() != player:
                    if not isinstance(field, Property):
                        sellable_fields[field.id()] = field
                    else:
                        build = field.field_in_district_has_buildings()
                        mortaged = field.mortaged()
                        if not mortaged and not build:
                            sellable_fields[field.id()] = field
        return sellable_fields

    def reached_number_of_rounds(self):
        '''
        Check if reached given number of rounds.
        '''
        if self.number_of_rounds() is None:
            return False
        elif self.current_round() <= self.number_of_rounds():
            return False
        else:
            return True

    def one_remainded(self):
        '''
        Checks if only one player is not bancrupt.
        '''
        counter = 0
        for player in self.players().values():
            if not player.is_bancrupt():
                counter += 1
        return counter == 1

    def simple_winner(self):
        '''
        Returns winner when other players are bancrupts.
        '''
        if not self.one_remainded():
            raise NotAllBancruptError
        else:
            for player in self.players().values():
                if not player.is_bancrupt():
                    return player

    def players_fortunes(self):
        '''
        Count active players fortunes.
        '''
        fortunes = {}
        for player in self.players().values():
            if not player.is_bancrupt():
                fortunes[player.id()] = player.fortune()
        return fortunes

    def richest_players(self):
        '''
        Returns players who collected highest fortune.
        '''
        fortunes = self.players_fortunes()
        max_fortune = max(fortunes.values())
        richest_players = {}
        for id in fortunes:
            if fortunes[id] == max_fortune:
                richest_players[id] = self.players()[id]
        return richest_players

    def debt_to_player(self, creditor):
        '''
        Action when player has debt to another player.
        Creditior takes over all player's money, fields and cards.
        All houses must be sold to bank.
        Value of its sell is added to creditor account.
        '''
        player = self.players()[self.current_player_id()]
        money = player.money()

        # calculate things that will be moved to creditor
        value_of_houses = self.calcualte_houses_value(player.fields())
        self.remove_houses(player.fields())
        interests = self.calculate_interests(player.fields())
        number_of_cards = player.get_out_cards_number()

        # hand over all fields to creditor
        fields = [field for field in player.fields().values()]
        for field in fields:
            field.set_owner(creditor)
            player.remove_field(field)
            creditor.add_field(field)

        # add things to creditor object
        creditor.add_money(value_of_houses)
        creditor.add_money(money)
        creditor.add_get_out_cards(number_of_cards)

        # substract interests of mortaged fields
        creditor.substract_money(interests)

        # substract things from player object
        player.substract_money(money)
        player.substract_get_out_cards(number_of_cards)

        # make player bancrupt
        player.set_bancrupt()

    def remove_houses(self, fields):
        '''
        Remove all houses from given collection of fields.
        '''
        for field in fields.values():
            if isinstance(field, Property):
                field.remove_all_houses()

    def calcualte_houses_value(self, fields):
        '''
        Calculate value of selling all house from
        given collection of fields.
        '''
        value_of_houses = 0
        for field in fields.values():
            if isinstance(field, Property):
                level = field.level()
                price = field.house_price()
                value_of_houses += int(0.5 * level * price)
        return value_of_houses

    def calculate_interests(self, fields):
        '''
        Calculate interests from mortaged fields.
        intersest = 10% of mortage value
        '''
        interests = 0
        for field in fields.values():
            if field.mortaged():
                interests += int(0.1 * field.mortage_value())
        return interests

    def debt_to_bank(self):
        '''
        Action when player has debt to bank.
        Creditior takes over all player's money, fields and cards.
        All houses must be sold to bank.
        Value of its sell is added to creditor account.
        '''
        # calculate things that will be moved to bank
        player = self.players()[self.current_player_id()]
        money = player.money()
        number_of_cards = player.get_out_cards_number()

        self.remove_houses(player.fields())

        # move all field to bank
        fields = [field for field in player.fields().values()]
        for field in fields:
            if field.mortaged():
                field.end_mortage()
            player.remove_field(field)
            field.set_owner(None)

        # substract things from player object
        player.substract_get_out_cards(number_of_cards)
        player.substract_money(money)

        # make player bancrupt
        player.set_bancrupt()

    def make_deal(self, buyer, field, price):
        '''
        Make deal between buyer and owner.
        '''
        seller = field.owner()
        if seller is not None:
            seller.add_money(price)
            seller.remove_field(field)
        buyer.substract_money(price)
        buyer.add_field(field)
        field.set_owner(buyer)

    def next_bidder_id(self, id, participants):
        '''
        Find id of next player who can make bid.
        '''
        found = False
        while not found:
            id = (id + 1) % self.number_of_players()
            found = id in participants
        return id

    # CHANCES CHANCES

    def draw_card(self):
        '''
        Choice id of chance card.
        '''
        id = randint(0, 16)
        return id

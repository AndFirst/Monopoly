from modules.constants import (MAX_NUMBER_OF_PLAYERS, JAIL_ID, START_ID,
                               START_MONEY, NUMBER_OF_FIELDS, PAYMENT)
from modules.exceptions import (WrongIdError, NoMoneyError, BuiltUpError,
                                AlreadyMortagedError, AlreadyArrestedError,
                                NotArrestedError, NotOwnedError)
from modules.fields import Property, Station, Service
from random import randint


class Player:
    '''
    A class to represent a player.

    Attributes
    ---------
    _id: int
        identify of player
    _name: str
        name of player (0; max_length]
    _position: int
        id of field on which player stand
    _money: int
        player's account balance
    _fields: list
        fields owned by player
    _stations_owned: int
        number of stations owned by player
    _services_owned: int
        number of services owned by player
    _in_jail_left: int
        number of rounds to come out of jail
    _get_out_cards_number: int
        number of cards relasing from jail
    _is_bancrupt: bool
        is player bancrupt
    _doubles_in_row: int
        number of the same points on dices in row

    Methods
    -------
    id:
        getter
    name:
        getter
    position:
        getter
    money:
        getter
    fields:
        getter
    stations_owned:
        getter
    services_owned:
        getter
    in_jail_left:
        getter
    get_out_cards_number:
        getter
    is_bancrupt:
        getter
    doubles_in_row:
        getter

    move:
        move player a numbe rof fields
    pass_start:
        check_if_player pass start
    get_payment:
        give a payment after passing start
    add_money:
        add money to player account
    substract_money:
        substract_money_from_player_account
    go_to_jail:
        put player to jail
    leave_jail:
        relase player
    add_get_out_cards:
        add number of cards
    substract_get_out_cards:
        substract number of cards
    use_get_out_of_cards:
        substract one card
    dices:
        roll two dices
    add_double:
        add double after lucky roll
    reset_doubles:
        reste plyer's doubles
    buy_from_bank:
        buy field from bank
    sell_to_bank:
        sell field to bank
    pay_rent:
        substract rent from player account
    add_field:
        add field to player fields
    remove_field:
        remove field from player's fields
    fortune:
        calculate player fortune
    can_pay:
        check if player can pay
    set_bancrupt:
        set player bancrupt
    count_houses:
        count all houses on player's properties
    short_description:
        short description to put on list
    jail_info:
        info about player jail status
    description:
        long description of player
    '''

    def __init__(self, id: int, name: str):
        '''
        Creates Player instance.
        '''
        if not 0 <= id < MAX_NUMBER_OF_PLAYERS:
            raise WrongIdError
        self._id = id
        self._name = name
        self._position = START_ID
        self._money = START_MONEY
        self._fields = {}
        self._stations_owned = 0
        self._services_owned = 0
        self._in_jail_round = None
        self._get_out_cards_number = 0
        self._is_bancrupt = False
        self._doubles_in_row = 0

    # GETTERS GETTERS GETTERS

    def id(self):
        '''
        Returns player's id.
        '''
        return self._id

    def name(self):
        '''
        Returns player's name.
        '''
        return self._name

    def position(self):
        '''
        Returns player's current position.
        '''
        return self._position

    def money(self):
        '''
        Returns player's money.
        '''
        return self._money

    def fields(self):
        '''
        Returns player's fields.
        '''
        return self._fields

    def stations_owned(self):
        '''
        Returns player's number of stations.
        '''
        return self._stations_owned

    def services_owned(self):
        '''
        Returns player's number of services.
        '''
        return self._services_owned

    def in_jail_round(self):
        '''
        Return number of rounds player is in jail.
        '''
        return self._in_jail_round

    def get_out_cards_number(self):
        '''
        Returns player's number of get out of jail cards.
        '''
        return self._get_out_cards_number

    def is_bancrupt(self):
        '''
        Returns True if player is bancrupt else False.
        '''
        return self._is_bancrupt

    def doubles_in_row(self):
        '''
        Returns how many doubles in row player currently has.
        '''
        return self._doubles_in_row

    def arrested(self):
        '''
        Return true if player is arrested.
        '''
        return self._in_jail_round is not None

    # METHODS METHODS METHODS

    def move(self, number_of_fields):
        '''
        Moves player a number of fields.
        '''
        if number_of_fields <= 0:
            raise ValueError('Player cannot move back.')
        self._position += number_of_fields

    def pass_start(self):
        '''
        Loops the board. When player passing start,
        his position change to new round around board.
        returns true if pass start
        '''
        if self.position() % NUMBER_OF_FIELDS != self.position():
            self._position %= NUMBER_OF_FIELDS
            return True
        return False

    def get_payment(self):
        '''
        Gives player a payment every time he pass start.
        '''
        self.add_money(PAYMENT)

    def add_money(self, amount):
        '''
        Add amount to player's account balance.
        '''
        if amount < 0:
            raise ValueError
        self._money += amount

    def substract_money(self, amount):
        '''
        Substract amount from player's account balance.
        '''
        if amount < 0:
            raise ValueError
        if self.money() < amount:
            raise NoMoneyError('Player has not got enough money.')
        self._money -= amount

    def go_to_jail(self):
        '''
        Set player jail rounds.
        '''
        if self.arrested():
            raise AlreadyArrestedError
        self._position = JAIL_ID
        self._in_jail_round = 1

    def leave_jail(self):
        '''
        Set player jail rounds to None.
        '''
        if not self.arrested():
            raise NotArrestedError
        self._in_jail_round = None

    def next_jail_round(self):
        '''
        Increment player's jail rounds.
        '''
        if not self.arrested():
            raise NotArrestedError
        self._in_jail_round += 1

    def add_get_out_cards(self, value=1):
        '''
        Add a number of get out of cards.
        '''
        if value < 0:
            raise ValueError
        self._get_out_cards_number += value

    def substract_get_out_cards(self, value=1):
        '''
        Substract a number of get out of cards.
        '''
        if value < 0:
            raise ValueError
        if value > self._get_out_cards_number:
            raise ValueError
        self._get_out_cards_number -= value

    def use_get_out_card(self):
        '''
        Leaves player from jail.
        '''
        if self.get_out_cards_number() == 0:
            raise ValueError
        self._get_out_cards_number -= 1

    def dices(self):
        '''
        Roll two dices and returns result.
        '''
        dice_1 = randint(1, 6)
        dice_2 = randint(1, 6)
        return dice_1, dice_2

    def add_double(self):
        '''
        Increment player's doubles in row.
        '''
        self._doubles_in_row += 1

    def reset_doubles(self):
        '''
        Set player's doubles to zero.
        '''
        self._doubles_in_row = 0

    def buy_from_bank(self, field):
        '''
        Buy field from bank.
        Add field to player's fields.
        Substract player's money.
        '''
        if self.money() < field.price():
            raise NoMoneyError
        else:
            self.substract_money(field.price())
            field.set_owner(self)
            self.add_field(field)

    def sell_to_bank(self, field):
        '''
        Sell field to bank.
        Remove field from player's fields.
        Add money to player account.
        '''
        if not field.owner() is self:
            raise NotOwnedError
        elif isinstance(field, Property) and field.field_in_district_has_buildings():
            raise BuiltUpError
        elif field.mortaged():
            raise AlreadyMortagedError
        else:
            self.add_money(field.mortage_value())
            field.set_owner(None)
            self.remove_field(field)

    def pay_rent(self, rent, owner):
        '''
        Pay rent to owner of field.
        '''
        if self.money() < rent:
            raise NoMoneyError()
        else:
            self.substract_money(rent)
            owner.add_money(rent)

    def add_field(self, field):
        '''
        Add field to player's fields.
        '''
        self._fields[field.id()] = field
        if isinstance(field, Station):
            self._stations_owned += 1
        if isinstance(field, Service):
            self._services_owned += 1
        self._fields = dict(sorted(self._fields.items()))

    def remove_field(self, field):
        '''
        Remove field from player's fields.
        '''
        del self._fields[field.id()]
        if isinstance(field, Station):
            self._stations_owned -= 1
        if isinstance(field, Service):
            self._services_owned -= 1

    def fortune(self):
        '''
        Calculate player fortune
        '''
        fortune = self.money()
        for field in self.fields().values():
            fortune += field.capitalisation()
        return fortune

    def can_pay(self, amount):
        '''
        Check if player can pay of the debt.
        '''
        return self.fortune() >= amount

    def set_bancrupt(self):
        '''
        set player bancrupt
        '''
        self._is_bancrupt = True
        self._position = None

    def count_houses(self):
        '''
        Count all player's houses
        '''
        houses_number = 0
        for field in self.fields().values():
            if isinstance(field, Property):
                houses_number += field.level()
        return houses_number

    # DESCRIPTIONS DESCRIPTIONS DESCRIPTIONS

    def short_description(self):
        '''
        Short description to put on players list.
        '''
        line_1 = '{:<15}{:>25}\n'.format('Id:', self.id())
        line_2 = '{:<15}{:>25}\n'.format('Nazwa:', self.name())
        return line_1 + line_2

    def jail_info(self):
        '''
        Returns info of player's jail status.
        '''
        info = '{:<15}{:>11}{:>15}\n'.format(self.id(), self.name(),
                                             self.in_jail_round())
        return info

    def description(self):
        '''
        Long description of player.
        '''
        dsc = self.short_description()
        if not self.is_bancrupt():
            stations = self.stations_owned()
            jail_round = self.in_jail_round()
            line_3 = '{:<15}{:>25}\n'.format('Pozycja:', self.position())
            line_4 = '{:<15}{:>25}\n'.format('Stan konta:', self.money())
            arrested = 'Tak' if self.in_jail_round() is not None else 'Nie'
            line_5 = '{:<15}{:>25}\n'.format('Aresztowany:', arrested)
            dsc += (line_3 + line_4 + line_5)
            if self.in_jail_round() is not None:
                dsc += '{:<15}{:>24}\n'.format('Rund w areszcie:', jail_round)
            line_6 = '{:<15}{:>25}\n'.format('Ilość dworców:', stations)
            line_7 = '{:<15}{:>25}\n'.format('Ilość usług:', self.services_owned())
            line_8 = '{:<15}{:>25}\n'.format('Liczba pól:', len(self.fields()))
            dsc += (line_6 + line_7 + line_8)
        else:
            line_3 = 'BANKRUT'
            dsc += line_3
        return dsc

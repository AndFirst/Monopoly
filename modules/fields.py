from modules.exceptions import (WrongIdError, BuiltUpError, NotMortagedError,
                                NotOwnedError, PropertyLevelError,
                                NoMoneyError, AlreadyMortagedError,
                                NotOwnedDistrictError, UnequalBuildingError,
                                AlreadyArrestedError, NotArrestedError)
from modules.constants import (DISTRICTS_SIZES, MAX_PROPERTY_LEVEL,
                               NUMBER_OF_STATIONS, NUMBER_OF_SERVICES)
from termcolor import colored


class Field:
    '''
    A basic class to represent field on Monopoly's board.

    Attributes
    ---------
    _id: int
        identify of field [0; number_of_fields)
    _name: str
        name of field

    Methods
    -------
    id:
        getter
    name:
        getter
    short description:
        generates short description (id and name)
    description:
        generates long description
    '''

    def __init__(self, data: dict):
        '''
        Create intance of Field.
        '''
        _id = data['id']
        if _id < 0:
            raise WrongIdError
        else:
            self._id = _id
        self._name = data['name']

    def id(self):
        '''
        Returns field's id.
        '''
        return self._id

    def name(self):
        '''
        Returns field's name
        '''
        return self._name

    def short_description(self):
        '''
        Returns short description about field.
        Using to display field on Monopoly's board.
        '''
        dsc = '{:>2}{:>30}'.format(self.id(), self.name())
        if isinstance(self, Property):
            dsc = colored(dsc, self.district(), attrs=['bold', 'dark'])
        return dsc

    def description(self):
        '''
        Returns detailed description about field.
        '''
        line_1 = '{:<15}{:>25}\n'.format('Nazwa:', self.name())
        line_2 = '{:<15}{:>25}\n'.format('ID:', self.id())
        return line_1 + line_2


class Start(Field):
    '''
    Class Start inherits from Field. Game starts from this field.
    Every time player comes through Start, gets salary.
    '''

    def __init__(self, data: dict):
        '''
        Creates Start instance.
        '''
        super().__init__(data)


class Parking(Field):
    '''
    Class Parking inherits from Field. When player stand on
    this field nothing happens.
    '''

    def __init__(self, data: dict):
        '''
        Creates Parking instance.
        '''
        super().__init__(data)


class Jail(Field):
    '''
    Class Jail inherits from Field. If player is not arrested
    nothing happens on this field. If player is arrested has to
    stay there until he can get out.

    Attributes
    ----------
    _arrested_players: dict
        players in jail

    Methods
    -------

    arrested_players:
        returns list of arrested players
    description:
        generates long description
    add:
        adds player to jail
    relase:
        remove player from jail
    '''

    def __init__(self, data: dict):
        '''
        Creates Jail instance.
        '''
        super().__init__(data)
        self._arrested_players = {}

    def arrested_players(self):
        '''
        Returns arrested players.
        '''
        return self._arrested_players

    def description(self):
        '''
        Returns long description of Jail field.
        '''
        dsc = super().description()
        line_3 = 'Gracze w areszcie:\n'
        line_4 = '{:<15}{:>11}{:>16}\n'.format('ID', 'Nazwa', 'Runda:')
        dsc += (line_3 + line_4)
        for player in self.arrested_players().values():
            dsc += player.jail_info()
        return dsc

    def add(self, player):
        '''
        Add player to jail.
        '''
        if player in self.arrested_players().values():
            raise AlreadyArrestedError
        self._arrested_players[player.id()] = player

    def relase(self, player):
        '''
        Relase player from jail.
        '''
        if player not in self.arrested_players().values():
            raise NotArrestedError
        del self._arrested_players[player.id()]


class GoToJail(Field):
    '''
    Class GoToJail inherits from Field. When player stand on
    this field have to go to jail and stay there for few rounds.
    '''
    def __init__(self, data: dict):
        '''
        Creates GoToJail instance.
        '''
        super().__init__(data)


class Tax(Field):
    '''
    Class Tax inherits from Field. Every time player stand
    on this field have to pay tax to bank.

    Attributes
    ---------
    _value: int
        amount of money player have to pay

    Methods
    -------
    value
        getter
    get_tax
        gets tax from player
    description:
        long description of field
    '''

    def __init__(self, data: dict):
        '''
        Creates Tax instance.
        '''
        super().__init__(data)
        _value = data['value']
        if _value < 0:
            raise ValueError('Tax value cannot be negative number.')
        self._value = _value

    def value(self):
        '''
        Returns Tax value.
        '''
        return self._value

    def get_tax(self, player):
        '''
        Substract tax value from player's account.
        '''
        player.substract_money(self.value())

    def description(self):
        '''
        Description of tax field.
        '''
        base = super().description()
        line_3 = '{:<15} {:>25}\n'.format('Do zapłaty:', self.value())
        return base + line_3


class DrawField(Field):
    '''
    Class DrawField inherits from Field. When player stand on
    this field recives a card with description what player have
    to do.
    '''

    def __init__(self, data: dict):
        '''
        Creates DrawField instance.
        '''
        super().__init__(data)


class BuyableField(Field):
    '''
    Class BuyableField inhertits from Field. Represent field
    that can be bought by player. Base class for Property, Station, Service.

    Attributes:
    ----------
    _price: int
        price of buying empty field
    _mortage_value: int
        money that can be recived for mortage in bank
    _mortaged: bool
        is field mortaged in bank
    _owner: int
        field's owner object

    Methods
    -------
    price:
        getter
    moratge_value:
        getter
    mortaged:
        getter
    owner:
        getter
    description:
        long description of field
    mortage_field:
        mortage field in bank
    start_mortage:
        mortage field in bank
    end_mortage:
        buy back field from mortage
    set_owner:
        set new owner to field
    capitalisation:
        value of selling all field to bank
    '''

    def __init__(self, data: dict):
        '''
        Create BuyableField instance.
        '''
        super().__init__(data)
        _price = data['price']
        if _price <= 0:
            raise ValueError('Price of field cannot be negative or zero')
        self._price = _price
        self._mortage_value = _price // 2
        self._mortaged = False
        self._owner = None

    def price(self):
        '''
        Returns price of field.
        '''
        return self._price

    def mortage_value(self):
        '''
        Returns mortage value of field.
        '''
        return self._mortage_value

    def mortaged(self):
        '''
        Returns True if field is mortaged.
        '''
        return self._mortaged

    def owner(self):
        '''
        Returns field's owner or None if field han no owner.
        '''
        return self._owner

    def start_mortage(self):
        '''
        Mortage field to bank.
        '''
        owner = self.owner()
        if self not in owner.fields().values():
            raise NotOwnedError
        elif self.mortaged():
            raise AlreadyMortagedError
        else:
            owner.add_money(self.mortage_value())
            self._mortaged = True

    def end_mortage(self):
        '''
        Buy field from mortage.
        Player person who buy up the mortage.
        '''
        owner = self.owner()
        if not self.mortaged():
            raise NotMortagedError
        else:
            if owner is not None:
                amount = int(1.1 * self.mortage_value())
                owner.substract_money(amount)
            self._mortaged = False

    def description(self):
        '''
        Generates long description of field.
        '''
        dsc = super().description()
        line_3 = '{:<15}{:>25}\n'.format('Cena:', self.price())
        line_4 = '{:<15}{:>25}\n'.format('Zastaw:', self.mortage_value())
        owner = self.owner().name() if self.owner() is not None else 'bank'
        line_5 = '{:<15}{:>25}\n'.format('Własność:', owner)
        mortaged = 'Tak' if self.mortaged() else 'Nie'
        line_6 = '{:<15}{:>25}\n'.format('Zastawiono:', mortaged)
        dsc += (line_3 + line_4 + line_5 + line_6)
        return dsc

    def set_owner(self, new_owner):
        '''
        Set new owner to field.
        '''
        self._owner = new_owner

    def capitalisation(self):
        '''
        Returns capitalisation of field.
        '''
        if self.mortaged():
            return 0
        else:
            return self.mortage_value()


class Property(BuyableField):
    '''
    Class Property inherits from BuyablePlace. Represents
    property field.

    Attributes
    ---------
    _district: str
        color of property district
    _house_price: int
        cost of building house or hotel
    _rents: dict
        rents on every property level
    _level: int
        number of houses max level is hotel

    Methods
    -------
    district:
        getter
    house_price:
        getter
    rents:
        getter
    level:
        getter
    set_level:
        set level to new value
    build_house
        build house on field
    start_mortage:
        start mortage of property
    field_in_district_has_buildings:
        check if district has any building
    all_district_owned:
        checks if owner has all district
    allow_to_be_upgraded:
        checks if owner can build house
    field_in_district_mortaged:
        check if any field in district is mortaged
    balanced_upgrade:
        checks if upgrade of property is balanced
    allow_to_be_downgraded:
        checks if owner can sell house
    balanced_downgrade:
        checks if downgrade is balanced
    remove_house
        sell house to bank
    remove_all_houses:
        set level to 0
    get_owned_fields_from_district:
        returns other field from field's district
    get_rent:
        get actual rent of field
    description
        long description of field
    capitalisation:
        value of selling field and houses to bank
    '''

    def __init__(self, data: dict):
        '''
        Create Property instance.
        '''
        super().__init__(data)
        self._district = data['district']

        _house_price = data['house_price']
        if _house_price <= 0:
            raise ValueError('House price cannot be negative or zero')
        else:
            self._house_price = _house_price

        _rents = data['rents']
        if len(_rents) != MAX_PROPERTY_LEVEL + 1:
            raise ValueError
        for level in _rents:
            if _rents[level] <= 0:
                raise ValueError('Rent cannot be negative or zero')
        self._rents = _rents
        self._level = 0

    def district(self):
        '''
        Returns property's district.
        '''
        return self._district

    def house_price(self):
        '''
        Returns price of buliding house on property.
        '''
        return self._house_price

    def rents(self):
        '''
        Returns property rents.
        '''
        return self._rents

    def level(self):
        '''
        Returns property level.
        '''
        return self._level

    def set_level(self, value):
        '''
        Set level to new value.
        '''
        if not 0 <= value <= MAX_PROPERTY_LEVEL:
            raise ValueError
        self._level = value

    def build_house(self):
        '''
        Build house on field.
        '''
        owner = self.owner()
        if self.allow_to_be_upgraded():
            owner.substract_money(self.house_price())
            self._level += 1

    def start_mortage(self):
        '''
        Mortage field to bank.
        '''
        owner = self.owner()
        if self not in owner.fields().values():
            raise NotOwnedError
        elif self.mortaged():
            raise AlreadyMortagedError
        elif self.field_in_district_has_buildings():
            raise BuiltUpError
        else:
            owner.add_money(self.mortage_value())
            self._mortaged = True

    def field_in_district_has_buildings(self):
        '''
        Check if any fileld in this district has buildings.
        '''
        owner = self.owner()
        for field in owner.fields().values():
            district = self.district()
            if isinstance(field, Property) and field.district() == district:
                if field.level() > 0:
                    return True
        return False

    def all_district_owned(self):
        '''
        Checks if owner of field has all properties in district.
        '''
        owner = self.owner()
        counter = 0
        district = self.district()
        for field in owner.fields().values():
            if isinstance(field, Property) and field.district() == district:
                counter += 1
        return DISTRICTS_SIZES[self.district()] == counter

    def allow_to_be_upgraded(self):
        '''
        Check if owner can upgrade property.
        '''
        owner = self.owner()
        if self.field_in_district_mortaged():
            raise AlreadyMortagedError
        elif not self.all_district_owned():
            raise NotOwnedDistrictError
        elif self.level() == MAX_PROPERTY_LEVEL:
            raise PropertyLevelError('Property level cannot be higher\
                 than max level')
        elif not self.balanced_upgrade():
            raise UnequalBuildingError
        elif owner.money() < self.house_price():
            raise NoMoneyError
        else:
            return True

    def field_in_district_mortaged(self):
        '''
        Check if any field in district is mortaged.
        '''
        owner = self.owner()
        for field in owner.fields().values():
            district = self.district()
            if isinstance(field, Property) and field.district() == district:
                if field.mortaged():
                    return True
        return False

    def balanced_upgrade(self):
        '''
        Check if upgrade of field is balanced.
        Owner cannot build house on field if its level
        is higher than minimal level in district.
        '''
        fields = self.get_owned_fields_from_district()
        for field in fields.values():
            if self.level() > field.level():
                return False
        return True

    def allow_to_be_downgraded(self):
        '''
        Check if owner can sell house from his field.
        '''
        min_level = 0
        if self.level() == min_level:
            raise PropertyLevelError('Property level cannot be lower\
                 than min level')
        elif not self.balanced_downgrade():
            raise UnequalBuildingError
        else:
            return True

    def balanced_downgrade(self):
        '''
        Checks if selling houses is balanced.
        Owner cannot sell house from field if its level
        is smaller than maximal level in district.
        '''
        fields = self.get_owned_fields_from_district()
        for field in fields.values():
            if self.level() < field.level():
                return False
        return True

    def remove_house(self):
        '''
        Sell house from property to bank.
        '''
        owner = self.owner()
        if self.allow_to_be_downgraded():
            amount = int(self.house_price() / 2)
            owner.add_money(amount)
            self._level -= 1

    def remove_all_houses(self):
        '''
        Removes all houses on field.
        Used only when owner is bancrupt.
        '''
        self._level = 0

    def get_owned_fields_from_district(self):
        '''
        Returns fields that has the same owner like
        this field and belongs to the same district.
        '''
        fields = {}
        owner = self.owner()
        district = self.district()
        for field in owner.fields().values():
            if isinstance(field, Property) and field.district() == district:
                fields[field.id()] = field
        return fields

    def get_rent(self):
        '''
        Returns current field's rent.
        '''
        if self.level() == 0 and self.all_district_owned():
            return self.rents()[str(self.level())] * 2
        else:
            return self.rents()[str(self.level())]

    def description(self):
        '''
        Long description of property to display it for user.
        '''
        dsc = super().description()
        line_7 = '{:<15}{:>25}\n'.format('Kolor:', self.district())
        line_8 = '{:<15}{:>25}\n'.format('Cena budowy:', self.house_price())
        line_9 = '{:<15}{:>25}\n'.format('Poziom:', self.level())
        line_10 = '{:<15}'.format('Opłaty:')
        line_11 = '\n{:<15}{:>25}\n'.format('Poziom', 'Wartość')
        dsc += (line_7 + line_8 + line_9 + line_10 + line_11)
        for level in self.rents():
            line = '{:<15}{:>25}\n'.format(level, self.rents()[level])
            dsc += line
        return dsc

    def capitalisation(self):
        '''
        Return full capitalization of property.
        Using to sum up the game.
        '''
        base = super().capitalisation()
        return base + int(0.5 * (self.level() * self.house_price()))


class Station(BuyableField):
    '''
    Class Station inherits from BuyableField. Represents
    Station field.

    Attributes
    ----------
    _rents: dict
        rents for standing on station

    Methods
    -------
    rents
        getter
    get_rent
        gets rent depending on owner number of stations
    description
        long description of field

    '''

    def __init__(self, data: dict):
        '''
        Creates Station instance.
        '''
        super().__init__(data)
        _rents = data['rents']
        if len(_rents) != NUMBER_OF_STATIONS:
            raise ValueError('Rents number must be equal number of stations')
        for level in _rents:
            if _rents[level] <= 0:
                raise ValueError('Rent cannot be negative or zero')
        self._rents = _rents

    def rents(self):
        '''
        Returns station rents.
        '''
        return self._rents

    def get_rent(self):
        '''
        Returns rent for given number of owned stations
        '''
        stations_owned = self.owner().stations_owned()
        return self._rents[str(stations_owned)]

    def description(self):
        '''
        Long description of the Station.
        '''
        dsc = super().description()
        line_7 = '{:<15}'.format('Opłaty:')
        line_8 = '\n{:<15}{:>25}\n'.format('Ilość', 'Wartość')
        dsc += (line_7 + line_8)
        for level in self.rents():
            line = '{:<15}{:>25}\n'.format(level, self.rents()[level])
            dsc += line
        return dsc


class Service(BuyableField):
    '''
    Class Service inherits from BuyablePlace.
    Represents Service field.

    Attributes
    ----------
    _multipliers: dict
        multipliers of dices when player stand on field

    Methods
    -------
    multipliers:
        getter
    get_rent:
        get rent depending on owner number of services
    description:
        long description of field
    '''

    def __init__(self, data: dict):
        '''
        Creates Service instance.
        '''
        super().__init__(data)
        _multipliers = data['multipliers']
        if len(_multipliers) != NUMBER_OF_SERVICES:
            raise ValueError('Multi number must be equal number of services')
        for level in _multipliers:
            if _multipliers[level] <= 0:
                raise ValueError('Multipliers of dice cannot be negative\
                     or zero')
        self._multipliers = _multipliers

    def multipliers(self):
        '''
        Returns Service's dices multiplier.
        '''
        return self._multipliers

    def get_rent(self, dices):
        '''
        Returns rent for given number of dices.
        '''
        services_owned = self.owner().services_owned()
        return self._multipliers[str(services_owned)] * sum(dices)

    def description(self):
        '''
        Long description of the Service.
        '''
        dsc = super().description()
        line_7 = '{:<15}'.format('Mnożniki:')
        line_8 = '\n{:<15}{:>25}\n'.format('Ilość', 'Mnożnik')
        dsc += (line_7 + line_8)
        for level in self.multipliers():
            line = '{:<15}{:>25}\n'.format(level, self.multipliers()[level])
            dsc += line
        return dsc

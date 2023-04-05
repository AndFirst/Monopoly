from modules.player import Player
from modules.constants import (START_ID, START_MONEY, MAX_NUMBER_OF_PLAYERS,
                               NUMBER_OF_FIELDS, PAYMENT, JAIL_ID)
from modules.exceptions import (WrongIdError, NoMoneyError, NotArrestedError,
                                AlreadyArrestedError, NotOwnedError,
                                BuiltUpError, AlreadyMortagedError)
from modules.fields import Property, Service, Station
import pytest


def test_create_player():
    player = Player(0, 'name')
    assert player.id() == 0
    assert player.name() == 'name'
    assert player.position() == START_ID
    assert player.money() == START_MONEY
    assert player.fields() == {}
    assert player.stations_owned() == 0
    assert player.services_owned() == 0
    assert player.in_jail_round() is None
    assert player.get_out_cards_number() == 0
    assert player.is_bancrupt() is False
    assert player.doubles_in_row() == 0


def test_wrong_id():
    with pytest.raises(WrongIdError):
        _ = Player(-1, 'name')
        _ = Player(MAX_NUMBER_OF_PLAYERS, 'name')


def test_move():
    player = Player(0, 'name')
    assert player.position() == 0
    player.move(1)
    assert player.position() == 1


def test_move_back():
    player = Player(0, 'name')
    assert player.position() == 0
    with pytest.raises(ValueError):
        player.move(0)
    with pytest.raises(ValueError):
        player.move(-1)


def test_no_pass_start():
    player = Player(0, 'name')
    assert player.position() == 0
    player.move(1)
    assert player.pass_start() is False
    assert player.position() == 1


def test_pass_start():
    player = Player(0, 'name')
    player.move(NUMBER_OF_FIELDS - 1)
    assert player.position() == NUMBER_OF_FIELDS - 1
    player.move(1)
    assert player.pass_start() is True
    assert player.position() == 0


def test_get_payment():
    player = Player(0, 'name')
    assert player.money() == START_MONEY
    player.get_payment()
    assert player.money() == START_MONEY + PAYMENT


def test_add_money():
    player = Player(0, 'name')
    assert player.money() == START_MONEY
    player.add_money(10)
    assert player.money() == START_MONEY + 10
    player.add_money(0)
    assert player.money() == START_MONEY + 10


def test_add_negative_value():
    player = Player(0, 'name')
    assert player.money() == START_MONEY
    with pytest.raises(ValueError):
        player.add_money(-1)


def test_substract_money():
    player = Player(0, 'name')
    assert player.money() == START_MONEY
    player.substract_money(10)
    assert player.money() == START_MONEY - 10
    player.substract_money(0)
    assert player.money() == START_MONEY - 10


def test_substract_negative_value():
    player = Player(0, 'name')
    assert player.money() == START_MONEY
    with pytest.raises(ValueError):
        player.substract_money(-1)


def test_substract_too_much_money():
    player = Player(0, 'name')
    assert player.money() == START_MONEY
    with pytest.raises(NoMoneyError):
        player.substract_money(START_MONEY + 1)


def test_go_to_jail():
    player = Player(0, 'name')
    assert player.position() == START_ID
    assert player.in_jail_round() is None
    player.go_to_jail()
    assert player.position() == JAIL_ID
    assert player.in_jail_round() == 1


def test_go_to_jail_already_arrested():
    player = Player(0, 'name')
    player.go_to_jail()
    # player is arrested, test above
    with pytest.raises(AlreadyArrestedError):
        player.go_to_jail()


def test_leave_jail():
    player = Player(0, 'name')
    player.go_to_jail()
    assert player.in_jail_round() == 1
    player.leave_jail()
    assert player.in_jail_round() is None


def test_leave_jail_not_arrested():
    player = Player(0, 'name')
    # player is arrested, test above
    with pytest.raises(NotArrestedError):
        player.leave_jail()


def test_next_jail_round():
    player = Player(0, 'name')
    player.go_to_jail()
    assert player.in_jail_round() == 1
    player.next_jail_round()
    assert player.in_jail_round() == 2


def test_next_jail_round_not_arrested():
    player = Player(0, 'name')
    with pytest.raises(NotArrestedError):
        player.next_jail_round()


def test_add_get_out_cards_default():
    player = Player(0, 'name')
    assert player.get_out_cards_number() == 0
    player.add_get_out_cards()
    assert player.get_out_cards_number() == 1


def test_add_get_out_cards():
    player = Player(0, 'name')
    assert player.get_out_cards_number() == 0
    player.add_get_out_cards(2)
    assert player.get_out_cards_number() == 2


def test_add_get_out_cards_negative_value():
    player = Player(0, 'name')
    with pytest.raises(ValueError):
        player.add_get_out_cards(-2)


def test_substract_get_out_cards_default():
    player = Player(0, 'name')
    player.add_get_out_cards()
    assert player.get_out_cards_number() == 1
    player.substract_get_out_cards()
    assert player.get_out_cards_number() == 0


def test_substract_get_out_cards():
    player = Player(0, 'name')
    player.add_get_out_cards(2)
    assert player.get_out_cards_number() == 2
    player.substract_get_out_cards(2)
    assert player.get_out_cards_number() == 0


def test_substract_get_out_cards_negative_value():
    player = Player(0, 'name')
    player.add_get_out_cards(2)
    assert player.get_out_cards_number() == 2
    with pytest.raises(ValueError):
        player.substract_get_out_cards(-2)


def test_substract_get_out_cards_more_than_player_has():
    player = Player(0, 'name')
    player.add_get_out_cards()
    assert player.get_out_cards_number() == 1
    with pytest.raises(ValueError):
        player.substract_get_out_cards(2)


def test_use_get_out_of_card():
    player = Player(0, 'name')
    player.add_get_out_cards()
    assert player.get_out_cards_number() == 1
    player.use_get_out_card()
    assert player.get_out_cards_number() == 0


def test_use_get_out_of_card_no_cards_owned():
    player = Player(0, 'name')
    with pytest.raises(ValueError):
        player.use_get_out_card()


def test_dices(monkeypatch):
    player = Player(0, 'name')

    def return_one_three(arg):
        return (1, 3)
    monkeypatch.setattr('modules.player.Player.dices', return_one_three)
    result = player.dices()
    assert result[0] == 1
    assert result[1] == 3


def test_add_double():
    player = Player(0, 'name')
    assert player.doubles_in_row() == 0
    player.add_double()
    assert player.doubles_in_row() == 1


def test_reset_doubles():
    player = Player(0, 'name')
    player.add_double()
    player.add_double()
    assert player.doubles_in_row() == 2
    player.reset_doubles()
    assert player.doubles_in_row() == 0


def test_add_property():
    player = Player(0, 'name')
    data = {
        "id": 1,
        "name": "Ulica Konopacka",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 2,
            "1": 10,
            "2": 30,
            "3": 90,
            "4": 160,
            "5": 250
        }
    }
    field = Property(data)
    assert len(player.fields()) == 0
    player.add_field(field)
    assert len(player.fields()) == 1
    assert player.fields()[1].name() == 'Ulica Konopacka'


def test_add_station():
    player = Player(0, 'name')
    data = {
        "id": 5,
        "name": "Dworzec Zachodni",
        "price": 200,
        "rents": {
            "1": 25,
            "2": 50,
            "3": 100,
            "4": 200
        }
    }
    field = Station(data)
    assert len(player.fields()) == 0
    player.add_field(field)
    assert len(player.fields()) == 1
    assert player.stations_owned() == 1
    assert player.fields()[5].name() == 'Dworzec Zachodni'


def test_add_service():
    player = Player(0, 'name')
    data = {
        "id": 12,
        "name": "Elektrownia",
        "price": 150,
        "multipliers": {
            "1": 4,
            "2": 10
        }
    }
    field = Service(data)
    assert len(player.fields()) == 0
    player.add_field(field)
    assert len(player.fields()) == 1
    assert player.services_owned() == 1
    assert player.fields()[12].name() == 'Elektrownia'


def test_remove_property():
    player = Player(0, 'name')
    data = {
        "id": 1,
        "name": "Ulica Konopacka",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 2,
            "1": 10,
            "2": 30,
            "3": 90,
            "4": 160,
            "5": 250
        }
    }
    field = Property(data)
    player.add_field(field)
    assert len(player.fields()) == 1
    player.remove_field(field)
    assert len(player.fields()) == 0


def test_remove_service():
    player = Player(0, 'name')
    data = {
        "id": 12,
        "name": "Elektrownia",
        "price": 150,
        "multipliers": {
            "1": 4,
            "2": 10
        }
    }
    field = Service(data)
    player.add_field(field)
    assert len(player.fields()) == 1
    assert player.services_owned() == 1
    player.remove_field(field)
    assert len(player.fields()) == 0
    assert player.services_owned() == 0


def test_remove_station():
    player = Player(0, 'name')
    data = {
        "id": 5,
        "name": "Dworzec Zachodni",
        "price": 200,
        "rents": {
            "1": 25,
            "2": 50,
            "3": 100,
            "4": 200
        }
    }
    field = Station(data)
    player.add_field(field)
    assert len(player.fields()) == 1
    assert player.stations_owned() == 1
    player.remove_field(field)
    assert len(player.fields()) == 0
    assert player.stations_owned() == 0


def test_buy_property_from_bank():
    player = Player(0, 'name')
    data = {
        "id": 1,
        "name": "Ulica Konopacka",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 2,
            "1": 10,
            "2": 30,
            "3": 90,
            "4": 160,
            "5": 250
        }
    }
    field = Property(data)
    assert player.money() == START_MONEY
    assert field.owner() is None
    assert len(player.fields()) == 0
    player.buy_from_bank(field)
    assert player.money() == START_MONEY - field.price()
    assert field.owner() == player
    assert len(player.fields()) == 1


def test_buy_station_from_bank():
    player = Player(0, 'name')
    data = {
        "id": 5,
        "name": "Dworzec Zachodni",
        "price": 200,
        "rents": {
            "1": 25,
            "2": 50,
            "3": 100,
            "4": 200
        }
    }
    field = Station(data)
    assert player.money() == START_MONEY
    assert field.owner() is None
    assert player.stations_owned() == 0
    player.buy_from_bank(field)
    assert player.money() == START_MONEY - field.price()
    assert field.owner() == player
    assert player.stations_owned() == 1


def test_buy_service_from_bank():
    player = Player(0, 'name')
    data = {
        "id": 12,
        "name": "Elektrownia",
        "price": 150,
        "multipliers": {
            "1": 4,
            "2": 10
        }
    }
    field = Service(data)
    assert player.money() == START_MONEY
    assert field.owner() is None
    assert player.services_owned() == 0
    player.buy_from_bank(field)
    assert player.money() == START_MONEY - field.price()
    assert field.owner() == player
    assert player.services_owned() == 1


def test_buy_from_bank_no_money():
    player = Player(0, 'name')
    data = {
        "id": 12,
        "name": "Elektrownia",
        "price": 150,
        "multipliers": {
            "1": 4,
            "2": 10
        }
    }
    field = Service(data)
    player.substract_money(START_MONEY)
    assert player.money() == 0
    with pytest.raises(NoMoneyError):
        player.buy_from_bank(field)


def test_sell_to_bank():
    player = Player(0, 'name')
    data = {
        "id": 1,
        "name": "Ulica Konopacka",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 2,
            "1": 10,
            "2": 30,
            "3": 90,
            "4": 160,
            "5": 250
        }
    }
    field = Property(data)
    player.buy_from_bank(field)
    money_after_buy = START_MONEY - field.price()
    player.sell_to_bank(field)
    assert player.money() == money_after_buy + field.mortage_value()
    assert field.owner() is None
    assert len(player.fields()) == 0


def test_sell_to_bank_not_owned():
    player = Player(0, 'name')
    player2 = Player(1, 'other_name')
    data = {
        "id": 1,
        "name": "Ulica Konopacka",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 2,
            "1": 10,
            "2": 30,
            "3": 90,
            "4": 160,
            "5": 250
        }
    }
    field = Property(data)
    player.buy_from_bank(field)
    field.set_owner(player2)
    with pytest.raises(NotOwnedError):
        player.sell_to_bank(field)


def test_sell_to_bank_with_houses():
    player = Player(0, 'name')
    data = {
        "id": 1,
        "name": "Ulica Konopacka",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 2,
            "1": 10,
            "2": 30,
            "3": 90,
            "4": 160,
            "5": 250
        }
    }
    field = Property(data)
    player.buy_from_bank(field)
    field.set_level(1)
    with pytest.raises(BuiltUpError):
        player.sell_to_bank(field)


def test_sell_to_bank_mortaged():
    player = Player(0, 'name')
    data = {
        "id": 1,
        "name": "Ulica Konopacka",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 2,
            "1": 10,
            "2": 30,
            "3": 90,
            "4": 160,
            "5": 250
        }
    }
    field = Property(data)
    player.buy_from_bank(field)
    field.start_mortage()
    with pytest.raises(AlreadyMortagedError):
        player.sell_to_bank(field)


def test_pay_rent():
    player = Player(0, 'name')
    owner = Player(1, 'other_name')
    rent = 100
    assert player.money() == START_MONEY == owner.money()
    player.pay_rent(rent, owner)
    assert player.money() == START_MONEY - rent
    assert owner.money() == START_MONEY + rent


def test_pay_rent_no_money():
    player = Player(0, 'name')
    owner = Player(1, 'other_name')
    rent = 100
    player.substract_money(START_MONEY)
    with pytest.raises(NoMoneyError):
        player.pay_rent(rent, owner)


def test_fortune():
    player = Player(0, 'name')
    property_data = {
        "id": 1,
        "name": "Ulica Konopacka",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 2,
            "1": 10,
            "2": 30,
            "3": 90,
            "4": 160,
            "5": 250
        }
    }
    service_data = {
        "id": 12,
        "name": "Elektrownia",
        "price": 150,
        "multipliers": {
            "1": 4,
            "2": 10
        }
    }
    station_data = {
        "id": 5,
        "name": "Dworzec Zachodni",
        "price": 200,
        "rents": {
            "1": 25,
            "2": 50,
            "3": 100,
            "4": 200
        }
    }
    property = Property(property_data)
    property.set_level(2)  # 30 + 2*25 = 80
    print(property.level())
    service = Service(service_data)  # 75
    station = Station(station_data)  # 100
    player.add_field(property)
    player.add_field(station)
    player.add_field(service)
    assert player.fortune() == player.money() + 80 + 75 + 100


def test_can_pay():
    player = Player(0, 'name')
    property_data = {
        "id": 1,
        "name": "Ulica Konopacka",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 2,
            "1": 10,
            "2": 30,
            "3": 90,
            "4": 160,
            "5": 250
        }
    }
    property = Property(property_data)
    player.add_field(property)
    player.substract_money(START_MONEY)
    assert player.money() == 0
    fortune = player.fortune()
    assert player.can_pay(fortune) is True
    assert player.can_pay(fortune + 1) is False


def test_set_bancrupt():
    player = Player(0, 'name')
    assert player.is_bancrupt() is False
    assert player.position() == 0
    player.set_bancrupt()
    assert player.is_bancrupt() is True
    assert player.position() is None


def test_count_houses():
    player = Player(0, 'name')
    property1_data = {
        "id": 1,
        "name": "Ulica Konopacka",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 2,
            "1": 10,
            "2": 30,
            "3": 90,
            "4": 160,
            "5": 250
        }
    }
    property2_data = {
        "id": 13,
        "name": "Ulica Marsa",
        "district": "magenta",
        "price": 140,
        "house_price": 100,
        "rents": {
            "0": 10,
            "1": 50,
            "2": 150,
            "3": 450,
            "4": 625,
            "5": 750
        }
    }
    property_1 = Property(property1_data)
    property_2 = Property(property2_data)
    player.add_field(property_1)
    player.add_field(property_2)
    assert player.count_houses() == 0
    player.fields()[1].set_level(5)
    assert player.count_houses() == 5
    player.fields()[13].set_level(2)
    assert player.count_houses() == 7


def test_short_description():
    player0 = Player(0, 'name')
    player1 = Player(1, 'other_name')
    player0_dsc = player0.short_description()
    player1_dsc = player1.short_description()
    assert player0_dsc == 'Id:                                    0\n'\
                          'Nazwa:                              name\n'
    assert player1_dsc == 'Id:                                    1\n'\
                          'Nazwa:                        other_name\n'


def test_jail_info():
    player = Player(1, 'name')
    player.go_to_jail()
    jail_info = player.jail_info()
    assert jail_info == '1                     name              1\n'

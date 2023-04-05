from modules.fields import (Field, Jail, Tax, BuyableField, Property,
                            Station, Service)
from modules.player import Player
from modules.exceptions import (UnequalBuildingError, AlreadyArrestedError,
                                NoMoneyError, NotArrestedError, NotOwnedError,
                                AlreadyMortagedError, NotOwnedDistrictError,
                                PropertyLevelError, WrongIdError, BuiltUpError,
                                NotMortagedError)
from modules.constants import START_MONEY
import pytest


def test_create_field():
    data = {
        "id": 1,
        "name": "field"
    }
    field = Field(data)
    assert field.id() == 1
    assert field.name() == 'field'


def test_create_field_with_negative_id():
    data = {
        "id": -1,
        "name": "field"
    }
    with pytest.raises(WrongIdError):
        _ = Field(data)


def test_create_jail():
    data = {
        "id": 10,
        "name": "jail"
    }
    jail = Jail(data)
    assert jail.arrested_players() == {}


def test_add_to_jail():
    data = {
        "id": 10,
        "name": "jail"
    }
    jail = Jail(data)
    player = Player(0, 'player')
    assert len(jail.arrested_players()) == 0
    jail.add(player)
    assert len(jail.arrested_players()) == 1


def test_add_to_jail_already_arrested_player():
    data = {
        "id": 10,
        "name": "jail"
    }
    jail = Jail(data)
    player = Player(0, 'player')
    jail.add(player)
    assert len(jail.arrested_players()) == 1
    with pytest.raises(AlreadyArrestedError):
        jail.add(player)


def test_relase_from_jail():
    data = {
        "id": 10,
        "name": "jail"
    }
    jail = Jail(data)
    player = Player(0, 'player')
    jail.add(player)
    assert len(jail.arrested_players()) == 1
    jail.relase(player)
    assert len(jail.arrested_players()) == 0


def test_relase_from_jail_not_arrested_player():
    data = {
        "id": 10,
        "name": "jail"
    }
    jail = Jail(data)
    player = Player(0, 'player')
    with pytest.raises(NotArrestedError):
        jail.relase(player)


def test_create_tax():
    data = {
        "id": 4,
        "name": "tax",
        "value": 200
    }
    field = Tax(data)
    assert field.value() == 200


def test_create_tax_negative_value():
    data = {
        "id": 4,
        "name": "Podatek Dochodowy",
        "value": -200
    }
    with pytest.raises(ValueError):
        _ = Tax(data)


def test_get_tax():
    data = {
        "id": 4,
        "name": "tax",
        "value": 200
    }
    field = Tax(data)
    player = Player(0, 'name')
    assert player.money() == START_MONEY
    field.get_tax(player)
    assert player.money() == START_MONEY - field.value()


def test_create_buyable_field():
    data = {
        "id": 3,
        "name": "buyable_field",
        "price": 60
    }
    field = BuyableField(data)
    assert field.price() == 60
    assert field.mortage_value() == 30
    assert field.mortaged() is False
    assert field.owner() is None


def test_create_buyable_field_negative_price():
    data = {
        "id": 3,
        "name": "buyable_field",
        "price": -60
    }
    with pytest.raises(ValueError):
        _ = BuyableField(data)


def test_start_mortage():
    data = {
        "id": 3,
        "name": "buyable_field",
        "price": 60
    }
    field = BuyableField(data)
    player = Player(1, 'name')
    field.set_owner(player)
    player.add_field(field)
    assert field.mortaged() is False
    assert player.money() == START_MONEY
    field.start_mortage()
    assert field.mortaged() is True
    assert player.money() == START_MONEY + field.mortage_value()


def test_start_mortage_not_owned_field():
    data = {
        "id": 3,
        "name": "buyable_field",
        "price": 60
    }
    field = BuyableField(data)
    player = Player(1, 'name')
    field.set_owner(player)
    with pytest.raises(NotOwnedError):
        field.start_mortage()


def test_start_mortage_mortaged_field():
    data = {
        "id": 3,
        "name": "buyable_field",
        "price": 60
    }
    field = BuyableField(data)
    player = Player(1, 'name')
    field.set_owner(player)
    player.add_field(field)
    field.start_mortage()
    assert field.mortaged() is True
    with pytest.raises(AlreadyMortagedError):
        field.start_mortage()


def test_end_mortage_by_player():
    data = {
        "id": 3,
        "name": "buyable_field",
        "price": 60
    }
    field = BuyableField(data)
    player = Player(1, 'name')
    field.set_owner(player)
    player.add_field(field)
    field.start_mortage()
    assert field.mortaged() is True
    assert player.money() == START_MONEY + field.mortage_value()
    field.end_mortage()
    assert field.mortaged() is False
    assert player.money() == START_MONEY + field.mortage_value() \
           - int(1.1 * field.mortage_value())


def test_end_mortage_bank():
    data = {
        "id": 3,
        "name": "buyable_field",
        "price": 60
    }
    field = BuyableField(data)
    player = Player(1, 'name')
    field.set_owner(player)
    player.add_field(field)
    field.start_mortage()
    player.remove_field(field)
    field.set_owner(None)
    assert field.mortaged() is True
    assert field.owner() is None
    field.end_mortage()
    assert field.mortaged() is False


def test_end_mortage_not_mortaged():
    data = {
        "id": 3,
        "name": "buyable_field",
        "price": 60
    }
    field = BuyableField(data)
    assert field.mortaged() is False
    with pytest.raises(NotMortagedError):
        field.end_mortage()


def test_set_owner():
    data = {
        "id": 3,
        "name": "buyable_field",
        "price": 60
    }
    field = BuyableField(data)
    player1 = Player(1, 'name')
    player2 = Player(2, 'othername')
    assert field.owner() is None
    field.set_owner(player1)
    assert field.owner() == player1
    field.set_owner(player2)
    assert field.owner() == player2


def test_create_property():
    data = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    field = Property(data)
    assert field.district() == 'grey'
    assert field.house_price() == 50
    assert len(field.rents()) == 6
    assert field.rents()['0'] == 4
    assert field.rents()['1'] == 20
    assert field.rents()['2'] == 60
    assert field.rents()['3'] == 180
    assert field.rents()['4'] == 320
    assert field.rents()['5'] == 450


def test_create_property_wrong_house_price():
    data = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 0,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    with pytest.raises(ValueError):
        _ = Property(data)


def test_create_property_wrong_rents_number():
    data = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320
        }
    }
    with pytest.raises(ValueError):
        _ = Property(data)


def test_create_property_wrong_rent():
    data = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": -450
        }
    }
    with pytest.raises(ValueError):
        _ = Property(data)


def test_set_level():
    data = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    field = Property(data)
    assert field.level() == 0
    field.set_level(2)
    assert field.level() == 2


def test_set_level_wrong_value():
    data = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    field = Property(data)
    with pytest.raises(ValueError):
        field.set_level(-1)
    with pytest.raises(ValueError):
        field.set_level(6)


def test_start_mortage_property():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    field_1.set_level(2)
    player = Player(1, 'name')
    field_1.set_owner(player)
    field_2.set_owner(player)
    player.add_field(field_1)
    player.add_field(field_2)
    with pytest.raises(BuiltUpError):
        field_1.start_mortage()
    with pytest.raises(BuiltUpError):
        field_2.start_mortage()


def test_all_district_owned():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player_1 = Player(1, 'name')
    player_2 = Player(2, 'other')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player_1.add_field(field_1)
    field_1.set_owner(player_1)
    assert field_1.all_district_owned() is False
    player_1.add_field(field_2)
    field_2.set_owner(player_1)
    assert field_1.all_district_owned() is True
    assert field_2.all_district_owned() is True
    field_1.set_owner(player_2)
    player_1.remove_field(field_1)
    player_2.add_field(field_1)
    assert field_1.all_district_owned() is False
    assert field_2.all_district_owned() is False


def test_allow_to_be_upgraded():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)

    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)

    assert field_1.allow_to_be_upgraded() is True
    assert field_2.allow_to_be_upgraded() is True


def test_field_in_district_mortaged():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    assert field_1.field_in_district_mortaged() is False
    assert field_2.field_in_district_mortaged() is False
    field_1.start_mortage()
    assert field_1.field_in_district_mortaged() is True
    assert field_2.field_in_district_mortaged() is True
    field_1.end_mortage()
    assert field_1.field_in_district_mortaged() is False
    assert field_2.field_in_district_mortaged() is False


def test_allow_to_be_upgraded_mortaged():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    field_1.start_mortage()
    assert field_1.mortaged() is True
    with pytest.raises(AlreadyMortagedError):
        field_1.allow_to_be_upgraded()
    with pytest.raises(AlreadyMortagedError):
        field_2.allow_to_be_upgraded()


def test_allow_to_be_upgraded_not_all_district_owned():
    data_1 = {
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
    player = Player(1, 'name')
    field_1 = Property(data_1)
    player.add_field(field_1)
    field_1.set_owner(player)
    with pytest.raises(NotOwnedDistrictError):
        field_1.allow_to_be_upgraded()


def test_allow_to_be_upgraded_unequall_building():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    field_1.set_level(1)
    with pytest.raises(UnequalBuildingError):
        field_1.allow_to_be_upgraded()


def test_allow_to_be_upgraded_max_lvl():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    field_1.set_level(5)
    field_2.set_level(5)
    with pytest.raises(PropertyLevelError):
        field_1.allow_to_be_upgraded()
    with pytest.raises(PropertyLevelError):
        field_2.allow_to_be_upgraded()


def test_allow_to_be_upgraded_no_money():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    player.substract_money(START_MONEY)
    assert player.money() == 0
    with pytest.raises(NoMoneyError):
        field_1.allow_to_be_upgraded()
    with pytest.raises(NoMoneyError):
        field_2.allow_to_be_upgraded()


def test_balanced_upgrade():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    assert field_1.balanced_upgrade() is True
    assert field_1.balanced_upgrade() is True
    field_1.set_level(1)
    assert field_1.balanced_upgrade() is False
    assert field_2.balanced_upgrade() is True


def test_build_house():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    assert player.money() == START_MONEY
    assert field_1.level() == 0
    field_1.build_house()
    assert player.money() == START_MONEY - field_1.house_price()
    assert field_1.level() == 1


def test_balanced_downgrade():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    field_1.set_level(5)
    field_2.set_level(5)
    assert field_1.balanced_downgrade() is True
    assert field_2.balanced_downgrade() is True
    field_2.set_level(4)
    assert field_1.balanced_downgrade() is True
    assert field_2.balanced_downgrade() is False


def test_allow_to_be_downgraded():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    field_1.set_level(5)
    field_2.set_level(5)
    assert field_1.allow_to_be_downgraded() is True
    assert field_2.allow_to_be_downgraded() is True


def test_allow_to_be_downgraded_unequal_building():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    field_1.set_level(5)
    field_2.set_level(5)
    assert field_1.allow_to_be_downgraded() is True
    assert field_2.allow_to_be_downgraded() is True
    field_1.set_level(4)
    field_2.allow_to_be_downgraded() is True
    with pytest.raises(UnequalBuildingError):
        field_1.allow_to_be_downgraded()


def test_remove_house():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    field_1.set_level(5)
    field_2.set_level(5)
    assert player.money() == START_MONEY
    assert field_1.level() == 5
    field_1.remove_house()
    assert player.money() == START_MONEY + 25
    assert field_1.level() == 4


def test_remove_all_houses():
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
    field.set_level(5)
    assert field.level() == 5
    field.remove_all_houses()
    assert field.level() == 0


def test_get_owned_fields_from_district():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    data_3 = {
        "id": 6,
        "name": "Ulica Radzymińska",
        "district": "white",
        "price": 100,
        "house_price": 50,
        "rents": {
            "0": 6,
            "1": 30,
            "2": 90,
            "3": 270,
            "4": 400,
            "5": 550
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_3)
    field_3.set_owner(player)
    fields = field_1.get_owned_fields_from_district()
    assert len(fields) == 1
    player.add_field(field_2)
    field_2.set_owner(player)
    fields = field_1.get_owned_fields_from_district()
    assert len(fields) == 2


def test_get_rent():
    data_1 = {
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
    data_2 = {
        "id": 3,
        "name": "Ulica Stalowa",
        "district": "grey",
        "price": 60,
        "house_price": 50,
        "rents": {
            "0": 4,
            "1": 20,
            "2": 60,
            "3": 180,
            "4": 320,
            "5": 450
        }
    }
    player = Player(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    player.add_field(field_1)
    field_1.set_owner(player)
    rent = field_1.get_rent()
    assert rent == 2
    player.add_field(field_2)
    field_2.set_owner(player)
    rent = field_1.get_rent()
    assert rent == 4
    field_1.build_house()
    assert field_1.level() == 1
    assert field_1.get_rent() == 10


def test_capitalisation():
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
    assert field.capitalisation() == 30
    field.set_level(5)
    assert field.capitalisation() == 155


def test_create_station():
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
    assert field.rents()['1'] == 25
    assert field.rents()['2'] == 50
    assert field.rents()['3'] == 100
    assert field.rents()['4'] == 200


def test_create_station_wrong_rents_number():
    data = {
        "id": 5,
        "name": "Dworzec Zachodni",
        "price": 200,
        "rents": {
            "1": 25,
            "2": 50,
            "3": 100,
            "4": 200,
            "5": 1234
        }
    }
    with pytest.raises(ValueError):
        _ = Station(data)


def test_create_station_wrong_rent():
    data = {
        "id": 5,
        "name": "Dworzec Zachodni",
        "price": 200,
        "rents": {
            "1": 25,
            "2": 50,
            "3": 100,
            "4": -200
        }
    }
    with pytest.raises(ValueError):
        _ = Station(data)


def test_get_rent_station():
    data_1 = {
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
    data_2 = {
        "id": 15,
        "name": "Dworzec Wschodni",
        "price": 200,
        "rents": {
            "1": 25,
            "2": 50,
            "3": 100,
            "4": 200
        }
    }
    field_1 = Station(data_1)
    field_2 = Station(data_2)
    player = Player(1, 'player')
    player.add_field(field_1)
    field_1.set_owner(player)
    assert player.stations_owned() == 1
    assert field_1.get_rent() == 25
    player.add_field(field_2)
    field_2.set_owner(player)
    assert player.stations_owned() == 2
    assert field_1.get_rent() == 50
    assert field_2.get_rent() == 50


def test_create_service():
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
    assert field.multipliers()['1'] == 4
    assert field.multipliers()['2'] == 10


def test_create_service_wrong_multipliers_number():
    data = {
        "id": 12,
        "name": "Elektrownia",
        "price": 150,
        "multipliers": {
            "1": 4
        }
    }
    with pytest.raises(ValueError):
        _ = Service(data)


def test_create_service_wrong_multiplier():
    data = {
        "id": 12,
        "name": "Elektrownia",
        "price": 150,
        "multipliers": {
            "1": 0,
            "2": -3
        }
    }
    with pytest.raises(ValueError):
        _ = Service(data)


def test_get_rent_serivce():
    data_1 = {
        "id": 12,
        "name": "Elektrownia",
        "price": 150,
        "multipliers": {
            "1": 4,
            "2": 10
        }
    }
    data_2 = {
        "id": 28,
        "name": "Wodociagi",
        "price": 150,
        "multipliers": {
            "1": 4,
            "2": 10
        }
    }
    field_1 = Service(data_1)
    field_2 = Service(data_2)
    player = Player(1, 'name')
    player.add_field(field_1)
    field_1.set_owner(player)
    assert player.services_owned() == 1
    dices = (1, 1)
    assert field_1.get_rent(dices) == 8
    player.add_field(field_2)
    field_2.set_owner(player)
    assert player.services_owned() == 2
    dices = (4, 6)
    assert field_1.get_rent(dices) == 100
    assert field_2.get_rent(dices) == 100

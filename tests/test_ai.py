from modules.ai import AiPlayer
from modules.fields import Property
from modules.constants import START_MONEY


def test_short_description():
    player = AiPlayer(1, 'name')
    dsc = player.short_description()
    assert dsc == 'Id:                                    1\n'\
                  'Nazwa:                              name\n'\
                  'AI Controlled\n'


def test_want_to_bid_small_price(monkeypatch):
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

    def return_nine(a, b):
        return 9
    monkeypatch.setattr('modules.ai.randint', return_nine)
    field = Property(data)
    player = AiPlayer(1, 'name')
    current_bid = 10
    assert player.money() == START_MONEY
    assert player.want_to_bid(current_bid, field) is True


def test_want_to_bid_not_enough_money():
    data = {
        "id": 1,
        "name": "Ulica Konopacka",
        "district": "grey",
        "price": 1500,
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
    player = AiPlayer(1, 'name')
    current_bid = 1191
    assert player.money() == START_MONEY
    assert player.want_to_bid(current_bid, field) is False


def test_want_to_bid_not_optimal_price():
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
    player = AiPlayer(1, 'name')
    current_bid = 51
    assert player.want_to_bid(current_bid, field) is False


def test_bid():
    player = AiPlayer(1, 'name')
    current_bid = 10
    assert player.bid(current_bid) == 20
    current_bid = 100
    assert player.bid(current_bid) == 110


def test_pricing(monkeypatch):
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

    def return_eighty(arg1, arg2):
        return 80
    monkeypatch.setattr('modules.ai.AiPlayer.pricing', return_eighty)
    field = Property(data)
    player = AiPlayer(1, 'name')
    assert player.pricing(field) == 80


def test_want_to_buy():
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
    player = AiPlayer(1, 'name')
    assert player.want_to_buy(field) is True
    player.substract_money(START_MONEY)
    player.add_money(359)
    assert player.want_to_buy(field) is False


def test_earn_from_houses():
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
    player = AiPlayer(1, 'name')
    player.substract_money(START_MONEY)
    player.add_money(10)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    field_1.set_level(3)
    field_2.set_level(4)
    debt = 100
    assert player.earn_from_houses(debt) is True
    assert field_1.level() == 1
    assert field_2.level() == 2
    assert player.money() == 110

    debt = 200
    assert player.earn_from_houses(debt) is False
    assert field_2.level() == 0
    assert field_2.level() == 0
    assert player.money() == 185


def test_earn_from_fields():
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
    player = AiPlayer(1, 'name')
    player.substract_money(START_MONEY)
    player.add_money(10)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    debt = 50
    assert player.money() == 10
    assert len(player.fields()) == 2
    player.earn_from_fields(debt)
    assert player.money() == 70
    assert len(player.fields()) == 0


def test_want_to_stay_in_jail():
    player = AiPlayer(1, 'name')
    current_round = 5
    assert player.want_to_stay_in_jail(current_round) is True
    current_round = 6
    assert player.want_to_stay_in_jail(current_round) is False


def test_deposit_decision():
    player = AiPlayer(1, 'name')
    assert player.deposit_decision() is True
    player.substract_money(START_MONEY)
    player.add_money(349)
    assert player.deposit_decision() is False


def test_use_card_decision():
    player = AiPlayer(1, 'name')
    assert player.get_out_cards_number() == 0
    assert player.use_card_decision() is False
    player.add_get_out_cards(1)
    assert player.get_out_cards_number() == 1
    assert player.use_card_decision() is True


def test_want_to_upgrade():
    player = AiPlayer(1, 'name')
    house_price = 50
    assert player.money() == START_MONEY
    assert player.want_to_upgrade(house_price) is True
    player.substract_money(START_MONEY)
    player.add_money(549)
    assert player.want_to_upgrade(house_price) is False


def test_count_owned_districts():
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
    player = AiPlayer(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)
    player.add_field(field_1)
    field_1.set_owner(player)
    player.add_field(field_2)
    field_2.set_owner(player)
    player.add_field(field_3)
    field_3.set_owner(player)
    counter = player.count_owned_districts()
    assert counter['grey'] == 2
    assert counter['white'] == 1
    assert counter['magenta'] == 0


def test_almost_full_districts():
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
    data_4 = {
        "id": 8,
        "name": "Ulica Jagiellońska",
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
    player = AiPlayer(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)
    field_4 = Property(data_4)

    player.add_field(field_1)
    field_1.set_owner(player)
    assert player.almost_full_districts() == ['grey']
    player.add_field(field_3)
    field_3.set_owner(player)
    assert player.almost_full_districts() == ['grey']
    player.add_field(field_4)
    field_4.set_owner(player)
    assert player.almost_full_districts() == ['grey', 'white']
    player.add_field(field_2)
    field_2.set_owner(player)
    assert player.almost_full_districts() == ['white']


def test_full_districts():
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

    player = AiPlayer(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)

    player.add_field(field_1)
    field_1.set_owner(player)
    assert player.full_districts() == []

    player.add_field(field_2)
    field_2.set_owner(player)
    assert player.full_districts() == ['grey']

    player.add_field(field_3)
    field_3.set_owner(player)
    assert player.full_districts() == ['grey']


def test_missing_fields_ids():
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
    data_4 = {
        "id": 8,
        "name": "Ulica Jagiellońska",
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
    data_5 = {
        "id": 9,
        "name": "Ulica Targowa",
        "district": "white",
        "price": 120,
        "house_price": 50,
        "rents": {
            "0": 8,
            "1": 40,
            "2": 100,
            "3": 300,
            "4": 450,
            "5": 600
        }
    }
    player = AiPlayer(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)
    field_4 = Property(data_4)
    field_5 = Property(data_5)
    fake_board = {
        1: field_1,
        2: field_2,
        3: field_3,
        4: field_4,
        5: field_5
    }

    player.add_field(field_1)
    field_1.set_owner(player)
    assert player.missing_fields_ids(fake_board) == [3]

    player.add_field(field_3)
    field_3.set_owner(player)
    assert player.missing_fields_ids(fake_board) == [3]

    player.add_field(field_4)
    field_4.set_owner(player)
    assert player.missing_fields_ids(fake_board) == [3, 9]


def test_missing_fields_id():
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
    data_4 = {
        "id": 8,
        "name": "Ulica Jagiellońska",
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
    data_5 = {
        "id": 9,
        "name": "Ulica Targowa",
        "district": "white",
        "price": 120,
        "house_price": 50,
        "rents": {
            "0": 8,
            "1": 40,
            "2": 100,
            "3": 300,
            "4": 450,
            "5": 600
        }
    }
    player = AiPlayer(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)
    field_4 = Property(data_4)
    field_5 = Property(data_5)
    fake_board = {
        1: field_1,
        2: field_2,
        3: field_3,
        4: field_4,
        5: field_5
    }
    player.add_field(field_1)
    field_1.set_owner(player)
    assert player.missing_field_id(field_1.district(), fake_board) == 3


def test_build_houses_ids():
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
    player = AiPlayer(1, 'name')
    field_1 = Property(data_1)
    field_2 = Property(data_2)

    player.add_field(field_1)
    field_1.set_owner(player)
    assert player.build_houses_ids() == []

    player.add_field(field_2)
    field_2.set_owner(player)
    assert player.build_houses_ids() == [1, 3]

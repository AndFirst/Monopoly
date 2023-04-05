from modules.game import Game
from modules.player import Player
from modules.fields import Property, Field, Start, Jail, Service
from modules.ai import AiPlayer
from modules.exceptions import (RepeatedIdError, PlayersNumberError,
                                TooShortGameError, AlreadyArrestedError,
                                NotArrestedError, NotAllBancruptError)
from modules.constants import (MIN_NUMBER_OF_ROUNDS, JAIL_ID, START_ID,
                               START_MONEY)
import pytest


def test_create_game():
    game = Game()
    assert game.players() == {}
    assert game.fields() == {}
    assert game.number_of_players() == 0
    assert game.number_of_rounds() is None
    assert game.current_player_id() == 0
    assert game.current_round() == 1
    assert game.finished() is False


def test_set_finished():
    game = Game()
    assert game.finished() is False
    game.set_finished()
    assert game.finished() is True


def test_set_players():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    players = {
        0: player_0,
        1: player_1
    }
    game = Game()
    assert game.players() == {}
    game.set_players(players)
    assert len(game.players()) == 2
    assert game.players()[0] == player_0
    assert game.players()[1] == player_1


def test_set_players_repeated_id():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(0, 'player_1')
    players = {
        0: player_0,
        1: player_1
    }
    game = Game()
    with pytest.raises(RepeatedIdError):
        game.set_players(players)


def test_set_fields():
    data_0 = {
        "id": 0,
        "name": "Start"
    }
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
    field_0 = Field(data_0)
    field_1 = Property(data_1)
    fields = {
        0: field_0,
        1: field_1
    }
    game = Game()
    assert game.fields() == {}
    game.set_fields(fields)
    assert len(game.fields()) == 2
    assert game.fields()[0] == field_0
    assert game.fields()[1] == field_1


def test_set_fields_repeated_id():
    data_0 = {
        "id": 0,
        "name": "Start"
    }
    data_1 = {
        "id": 0,
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
    field_0 = Field(data_0)
    field_1 = Property(data_1)
    fields = {
        0: field_0,
        1: field_1
    }
    game = Game()
    assert game.fields() == {}
    with pytest.raises(RepeatedIdError):
        game.set_fields(fields)


def test_set_number_of_players():
    game = Game()
    assert game.number_of_players() == 0
    game.set_number_of_players(2)
    assert game.number_of_players() == 2


def test_set_number_of_players_wrong_value():
    game = Game()
    with pytest.raises(PlayersNumberError):
        game.set_number_of_players(1)
    with pytest.raises(PlayersNumberError):
        game.set_number_of_players(7)


def test_set_number_of_rounds():
    game = Game()
    assert game.number_of_rounds() is None
    game.set_number_of_rounds(2)
    assert game.number_of_rounds() == 2


def test_set_number_of_rounds_wrong_value():
    game = Game()
    with pytest.raises(TooShortGameError):
        game.set_number_of_rounds(MIN_NUMBER_OF_ROUNDS - 1)


def test_roll_dices_no_double(monkeypatch):
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    players = {
        0: player_0,
        1: player_1
    }
    game = Game()
    game.set_players(players)

    def return_one_three(arg):
        return (1, 3)
    monkeypatch.setattr('modules.player.Player.dices', return_one_three)
    assert game.roll_dices() == (1, 3)
    assert player_0.doubles_in_row() == 0


def test_roll_dices_double(monkeypatch):
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    players = {
        0: player_0,
        1: player_1
    }
    game = Game()
    game.set_players(players)

    def return_one_three(arg):
        return (1, 3)

    def return_three_three(arg):
        return (3, 3)
    monkeypatch.setattr('modules.player.Player.dices', return_three_three)
    assert game.roll_dices() == (3, 3)
    assert player_0.doubles_in_row() == 1
    assert game.roll_dices() == (3, 3)
    assert player_0.doubles_in_row() == 2
    monkeypatch.setattr('modules.player.Player.dices', return_one_three)
    assert game.roll_dices() == (1, 3)
    assert player_0.doubles_in_row() == 0


def test_arrest():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    players = {
        0: player_0,
        1: player_1
    }
    data_1 = {
        "id": 0,
        "name": "Start"
    }
    data_2 = {
        "id": 10,
        "name": "Więzienie"
    }
    start = Start(data_1)
    jail = Jail(data_2)
    fields = {
        START_ID: start,
        JAIL_ID: jail
    }
    game = Game()
    game.set_players(players)
    game.set_fields(fields)
    assert player_0.position() == START_ID
    assert player_0.arrested() is False
    assert player_0.in_jail_round() is None
    assert jail.arrested_players() == {}
    game.arrest(player_0)
    assert player_0.position() == JAIL_ID
    assert player_0.arrested() is True
    assert player_0.in_jail_round() == 1
    assert jail.arrested_players() == {0: player_0}
    game.arrest(player_1)
    assert player_1.position() == JAIL_ID
    assert player_1.arrested() is True
    assert player_1.in_jail_round() == 1
    assert jail.arrested_players() == {
        0: player_0,
        1: player_1
        }
    with pytest.raises(AlreadyArrestedError):
        game.arrest(player_0)


def test_leave_jail():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    players = {
        0: player_0,
        1: player_1
    }
    data = {
        "id": 10,
        "name": "Więzienie"
    }
    jail = Jail(data)
    fields = {
        JAIL_ID: jail
    }
    game = Game()
    game.set_players(players)
    game.set_fields(fields)
    game.arrest(player_0)
    assert player_0.position() == JAIL_ID
    assert player_0.arrested() is True
    assert player_0.in_jail_round() == 1
    assert jail.arrested_players() == {0: player_0}
    game.leave_jail(player_0)
    assert player_0.position() == JAIL_ID
    assert player_0.arrested() is False
    assert player_0.in_jail_round() is None
    assert jail.arrested_players() == {}

    with pytest.raises(NotArrestedError):
        game.leave_jail(player_1)


def test_next_player():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    player_2 = Player(2, 'player_2')
    players = {
        0: player_0,
        1: player_1,
        2: player_2
    }
    game = Game()

    game.set_number_of_players(3)
    game.set_players(players)
    assert game.current_player_id() == 0
    assert game.current_round() == 1
    game.next_player()
    assert game.current_player_id() == 1
    assert game.current_round() == 1
    game.next_player()
    assert game.current_player_id() == 2
    assert game.current_round() == 1
    game.next_player()
    assert game.current_player_id() == 0
    assert game.current_round() == 2
    player_1.set_bancrupt()
    game.next_player()
    assert game.current_player_id() == 2
    assert game.current_round() == 2
    assert len(game.players()) == 3
    game.next_player()
    assert game.current_player_id() == 0
    assert game.current_round() == 3


def test_bidding_players():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    player_2 = Player(2, 'player_2')
    player_3 = Player(3, 'player_3')
    players = {
        0: player_0,
        1: player_1,
        2: player_2,
        3: player_3
    }
    game = Game()
    game.set_number_of_players(4)
    game.set_players(players)
    assert game.current_player_id() == 0
    assert game.bidding_players() == {
        1: player_1,
        2: player_2,
        3: player_3
    }
    player_3.set_bancrupt()
    assert game.bidding_players() == {
        1: player_1,
        2: player_2,
    }
    game.next_player()
    assert game.bidding_players() == {
        0: player_0,
        2: player_2,
    }


def test_reached_number_of_rounds_given():
    game = Game()
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    players = {
        0: player_0,
        1: player_1
    }
    game.set_number_of_rounds(2)
    game.set_number_of_players(2)
    game.set_players(players)
    assert game.current_round() == 1
    assert game.reached_number_of_rounds() is False
    game.next_player()
    game.next_player()
    assert game.current_round() == 2
    assert game.reached_number_of_rounds() is False
    game.next_player()
    game.next_player()
    assert game.reached_number_of_rounds() is True


def test_reached_number_of_rounds_not_given():
    game = Game()
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    players = {
        0: player_0,
        1: player_1
    }
    game.set_number_of_players(2)
    game.set_players(players)
    for i in range(100):
        assert game.reached_number_of_rounds() is False
        game.next_player()


def test_one_remainded():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    player_2 = Player(2, 'player_2')
    player_3 = Player(3, 'player_3')
    players = {
        0: player_0,
        1: player_1,
        2: player_2,
        3: player_3
    }
    game = Game()
    game.set_number_of_players(4)
    game.set_players(players)
    assert game.one_remainded() is False
    player_0.set_bancrupt()
    assert game.one_remainded() is False
    player_2.set_bancrupt()
    assert game.one_remainded() is False
    player_3.set_bancrupt()
    assert game.one_remainded() is True


def test_simple_winner():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    player_2 = Player(2, 'player_2')
    player_3 = Player(3, 'player_3')
    players = {
        0: player_0,
        1: player_1,
        2: player_2,
        3: player_3
    }
    game = Game()
    game.set_number_of_players(4)
    game.set_players(players)
    assert game.one_remainded() is False
    player_0.set_bancrupt()
    assert game.one_remainded() is False
    player_2.set_bancrupt()
    assert game.one_remainded() is False
    player_3.set_bancrupt()
    assert game.one_remainded() is True
    assert game.simple_winner() == player_1


def test_simple_winner_not_all_bancrupt():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    player_2 = Player(2, 'player_2')
    player_3 = Player(3, 'player_3')
    players = {
        0: player_0,
        1: player_1,
        2: player_2,
        3: player_3
    }
    game = Game()
    game.set_number_of_players(4)
    game.set_players(players)
    assert game.one_remainded() is False
    with pytest.raises(NotAllBancruptError):
        game.simple_winner()


def test_players_fortunes():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    player_2 = Player(2, 'player_2')
    player_3 = Player(3, 'player_3')
    players = {
        0: player_0,
        1: player_1,
        2: player_2,
        3: player_3
    }
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
        "id": 37,
        "name": "Ulica Belwederska",
        "district": "blue",
        "price": 350,
        "house_price": 200,
        "rents": {
            "0": 35,
            "1": 175,
            "2": 500,
            "3": 1100,
            "4": 1300,
            "5": 1500
        }
    }
    data_3 = {
        "id": 39,
        "name": "Aleje Ujazdowskie",
        "district": "blue",
        "price": 400,
        "house_price": 200,
        "rents": {
            "0": 50,
            "1": 200,
            "2": 600,
            "3": 1400,
            "4": 1700,
            "5": 2000
        }
    }
    field_1 = Service(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)
    game = Game()
    game.set_number_of_players(4)
    game.set_players(players)
    fortunes = game.players_fortunes()
    assert fortunes == {
        0: START_MONEY,
        1: START_MONEY,
        2: START_MONEY,
        3: START_MONEY
    }
    player_0.add_money(420)
    player_1.substract_money(23)
    player_2.buy_from_bank(field_1)
    player_3.buy_from_bank(field_2)
    player_3.buy_from_bank(field_3)
    fortunes = game.players_fortunes()
    assert fortunes == {
        0: START_MONEY + 420,
        1: START_MONEY - 23,
        2: START_MONEY - 75,
        3: START_MONEY - 375
    }
    field_2.set_level(5)
    field_3.set_level(4)
    fortunes = game.players_fortunes()
    assert fortunes == {
        0: START_MONEY + 420,
        1: START_MONEY - 23,
        2: START_MONEY - 75,
        3: START_MONEY + 525
    }


def test_richest_players():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    player_2 = Player(2, 'player_2')
    player_3 = Player(3, 'player_3')
    players = {
        0: player_0,
        1: player_1,
        2: player_2,
        3: player_3
    }
    game = Game()
    game.set_number_of_players(4)
    game.set_players(players)
    assert game.richest_players() == {
        0: player_0,
        1: player_1,
        2: player_2,
        3: player_3
    }
    player_0.add_money(123)
    assert game.richest_players() == {
        0: player_0,
    }
    player_2.add_money(300)
    player_3.add_money(300)
    assert game.richest_players() == {
        2: player_2,
        3: player_3
    }


def test_make_deal():
    data = {
        "id": 37,
        "name": "Ulica Belwederska",
        "district": "blue",
        "price": 350,
        "house_price": 200,
        "rents": {
            "0": 35,
            "1": 175,
            "2": 500,
            "3": 1100,
            "4": 1300,
            "5": 1500
        }
    }
    field = Property(data)
    fields = {
        37: field
    }
    player_0 = Player(0, 'name')
    player_1 = Player(1, 'name')
    players = {
        0: player_0,
        1: player_1
    }
    game = Game()
    game.set_players(players)
    game.set_fields(fields)
    assert field.owner() is None
    assert len(player_0.fields()) == 0
    assert player_0.money() == START_MONEY
    game.make_deal(player_0, field, 100)
    assert field.owner() == player_0
    assert len(player_0.fields()) == 1
    assert player_0.money() == START_MONEY - 100
    game.make_deal(player_1, field, 200)
    assert field.owner() == player_1
    assert len(player_0.fields()) == 0
    assert len(player_1.fields()) == 1
    assert player_0.money() == START_MONEY + 100
    assert player_1.money() == START_MONEY - 200


def test_next_bidder_id():
    player_0 = Player(0, 'player_0')
    player_1 = AiPlayer(1, 'player_1')
    player_2 = Player(2, 'player_2')
    player_3 = Player(3, 'player_3')
    players = {
        0: player_0,
        1: player_1,
        2: player_2,
        3: player_3
    }
    game = Game()
    game.set_number_of_players(4)
    game.set_players(players)
    participants = {
        1: player_1,
        2: player_2,
        3: player_3
    }
    id = 1
    id = game.next_bidder_id(id, participants)
    assert id == 2
    id = game.next_bidder_id(id, participants)
    assert id == 3
    id = game.next_bidder_id(id, participants)
    id == 0


def test_draw_card(monkeypatch):
    def return_seven(arg):
        return 7
    monkeypatch.setattr('modules.game.Game.draw_card', return_seven)
    game = Game()
    assert game.draw_card() == 7


def test_remove_houses():
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
        "id": 37,
        "name": "Ulica Belwederska",
        "district": "blue",
        "price": 350,
        "house_price": 200,
        "rents": {
            "0": 35,
            "1": 175,
            "2": 500,
            "3": 1100,
            "4": 1300,
            "5": 1500
        }
    }
    data_3 = {
        "id": 39,
        "name": "Aleje Ujazdowskie",
        "district": "blue",
        "price": 400,
        "house_price": 200,
        "rents": {
            "0": 50,
            "1": 200,
            "2": 600,
            "3": 1400,
            "4": 1700,
            "5": 2000
        }
    }
    field_1 = Service(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)
    fields = {
        12: field_1,
        37: field_2,
        39: field_3
    }
    game = Game()
    field_2.set_level(5)
    field_3.set_level(3)
    assert field_2.level() == 5
    assert field_3.level() == 3
    game.remove_houses(fields)
    assert field_2.level() == 0
    assert field_3.level() == 0


def test_calculate_houses_value():
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
        "id": 37,
        "name": "Ulica Belwederska",
        "district": "blue",
        "price": 350,
        "house_price": 200,
        "rents": {
            "0": 35,
            "1": 175,
            "2": 500,
            "3": 1100,
            "4": 1300,
            "5": 1500
        }
    }
    data_3 = {
        "id": 39,
        "name": "Aleje Ujazdowskie",
        "district": "blue",
        "price": 400,
        "house_price": 200,
        "rents": {
            "0": 50,
            "1": 200,
            "2": 600,
            "3": 1400,
            "4": 1700,
            "5": 2000
        }
    }
    field_1 = Service(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)
    fields = {
        12: field_1,
        37: field_2,
        39: field_3
    }
    game = Game()
    field_2.set_level(5)
    field_3.set_level(3)
    value = game.calcualte_houses_value(fields)
    assert value == 800


def test_caclulate_interests():
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
        "id": 37,
        "name": "Ulica Belwederska",
        "district": "blue",
        "price": 350,
        "house_price": 200,
        "rents": {
            "0": 35,
            "1": 175,
            "2": 500,
            "3": 1100,
            "4": 1300,
            "5": 1500
        }
    }
    data_3 = {
        "id": 39,
        "name": "Aleje Ujazdowskie",
        "district": "blue",
        "price": 400,
        "house_price": 200,
        "rents": {
            "0": 50,
            "1": 200,
            "2": 600,
            "3": 1400,
            "4": 1700,
            "5": 2000
        }
    }
    field_1 = Service(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)
    fields = {
        12: field_1,
        37: field_2,
        39: field_3
    }
    player_1 = Player(0, 'name')
    player_2 = Player(1, 'name')
    players = {
        0: player_1,
        1: player_2
    }
    game = Game()
    game.set_players(players)
    game.set_fields(fields)
    field_1.set_owner(player_1)
    player_1.add_field(field_1)
    field_2.set_owner(player_1)
    player_1.add_field(field_2)
    field_3.set_owner(player_1)
    player_1.add_field(field_3)
    assert game.calculate_interests(fields) == 0
    field_1.start_mortage()
    field_3.start_mortage()
    assert game.calculate_interests(fields) == 7 + 20


def test_debt_to_player():
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
        "id": 37,
        "name": "Ulica Belwederska",
        "district": "blue",
        "price": 350,
        "house_price": 200,
        "rents": {
            "0": 35,
            "1": 175,
            "2": 500,
            "3": 1100,
            "4": 1300,
            "5": 1500
        }
    }
    data_3 = {
        "id": 39,
        "name": "Aleje Ujazdowskie",
        "district": "blue",
        "price": 400,
        "house_price": 200,
        "rents": {
            "0": 50,
            "1": 200,
            "2": 600,
            "3": 1400,
            "4": 1700,
            "5": 2000
        }
    }
    field_1 = Service(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)
    fields = {
        12: field_1,
        37: field_2,
        39: field_3
    }
    player_1 = Player(0, 'name')
    player_2 = Player(1, 'name')
    players = {
        0: player_1,
        1: player_2
    }
    game = Game()
    game.set_players(players)
    game.set_fields(fields)
    field_1.set_owner(player_1)
    player_1.add_field(field_1)
    field_2.set_owner(player_1)
    player_1.add_field(field_2)
    field_3.set_owner(player_1)
    player_1.add_field(field_3)

    player_1.add_get_out_cards(2)
    player_1.substract_money(START_MONEY)
    player_1.add_money(10)
    player_2.substract_money(START_MONEY)

    field_2.set_level(3)
    field_3.set_level(2)

    assert player_1.money() == 10
    assert player_1.get_out_cards_number() == 2
    assert len(player_1.fields()) == 3
    assert player_1.is_bancrupt() is False

    assert player_2.money() == 0
    assert player_2.get_out_cards_number() == 0
    assert len(player_2.fields()) == 0

    game.debt_to_player(player_2)

    assert player_1.money() == 0
    assert player_1.get_out_cards_number() == 0
    assert len(player_1.fields()) == 0
    assert player_1.is_bancrupt() is True

    assert player_2.money() == 510
    assert player_2.get_out_cards_number() == 2
    assert len(player_2.fields()) == 3


def test_debt_to_bank():
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
        "id": 37,
        "name": "Ulica Belwederska",
        "district": "blue",
        "price": 350,
        "house_price": 200,
        "rents": {
            "0": 35,
            "1": 175,
            "2": 500,
            "3": 1100,
            "4": 1300,
            "5": 1500
        }
    }
    data_3 = {
        "id": 39,
        "name": "Aleje Ujazdowskie",
        "district": "blue",
        "price": 400,
        "house_price": 200,
        "rents": {
            "0": 50,
            "1": 200,
            "2": 600,
            "3": 1400,
            "4": 1700,
            "5": 2000
        }
    }
    field_1 = Service(data_1)
    field_2 = Property(data_2)
    field_3 = Property(data_3)
    fields = {
        12: field_1,
        37: field_2,
        39: field_3
    }
    player_1 = Player(0, 'name')
    player_2 = Player(1, 'name')
    players = {
        0: player_1,
        1: player_2
    }
    game = Game()
    game.set_players(players)
    game.set_fields(fields)
    field_1.set_owner(player_1)
    player_1.add_field(field_1)
    field_2.set_owner(player_1)
    player_1.add_field(field_2)
    field_3.set_owner(player_1)
    player_1.add_field(field_3)
    player_1.add_get_out_cards(2)

    assert player_1.money() == 1500
    assert player_1.get_out_cards_number() == 2
    assert len(player_1.fields()) == 3
    assert player_1.is_bancrupt() is False
    assert field_1.owner() == player_1
    assert field_2.owner() == player_1
    assert field_3.owner() == player_1

    game.debt_to_bank()
    assert player_1.money() == 0
    assert player_1.get_out_cards_number() == 0
    assert len(player_1.fields()) == 0
    assert player_1.is_bancrupt() is True
    assert field_1.owner() is None
    assert field_2.owner() is None
    assert field_3.owner() is None

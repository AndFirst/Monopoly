from modules.constants import FIELDS_PATH, DEPOSIT, START_BID
from modules.fields import (Property, BuyableField, GoToJail, DrawField,
                            Station, Service, Tax)
from modules.exceptions import (AlreadyMortagedError, NotOwnedDistrictError,
                                PropertyLevelError, UnequalBuildingError,
                                NotMortagedError, NoMoneyError, BuiltUpError)
from modules.player import Player
from modules.ai import AiPlayer
import sys


class Gameplay:
    '''
    Class Gameplay. Connects interface and game state.
    '''
    def __init__(self, interface, game):
        self._interface = interface
        self._game = game

    # GETTERS

    def interface(self):
        '''
        Call game interface.
        '''
        return self._interface

    def game(self):
        '''
        Call game state.
        '''
        return self._game

    # GAME PREPARATIONS

    def preparations(self):
        '''
        Preparartion and configuration of game.
        Creates fields from config.
        Ask to start the game or quit.
        Creates players from input.
        '''
        self.game().create_fields(FIELDS_PATH)
        self.check_intro_choice()
        self.create_players()
        self.create_rounds()

    def check_intro_choice(self):
        '''
        Intro screen.
        1 - go on
        q - exit
        '''
        choice = self.interface().intro_choice()
        if choice == '1':
            return
        if choice == 'q':
            self.exit()

    def create_players(self):
        '''
        Prints instruction of players number.
        Input number of players from user.
        Set number of players to game.
        Print instruction of players names.
        Add players from user input.
        '''
        self.interface().print_players_number_info()
        input_number = self.interface().input_players_number()
        self.game().set_number_of_players(input_number)
        self.interface().print_player_names_info()
        self.add_players()

    def add_players(self):
        '''
        Input from user players names.
        Ask if player be ai controlled.
        Add correct type of player to dictionary.
        Set players to game.
        '''
        players = {}
        id = 0
        while id < self.game().number_of_players():
            name = self.interface().input_player_name()
            if id == 0:
                new_player = Player(id, name)
            else:
                choice = self.interface().ai_choice(name)
                if choice == '1':
                    new_player = AiPlayer(id, name)
                else:
                    new_player = Player(id, name)
            self.interface().add_successfully(name)
            players[id] = new_player
            id += 1
        self.game().set_players(players)

    def create_rounds(self):
        '''
        Input from user number of rounds.
        If user does not want to set this value,
        set None to number_of_rounds.
        '''
        input_number = self.interface().input_rounds()
        self.game().set_number_of_rounds(input_number)

    # MAIN

    def main(self):
        '''
        Main function of Monopoly game.
        '''
        self.preparations()
        while not self.game().finished():
            self.turn()
            self.game().next_player()
            self.chcek_end()

    def main_menu(self):
        '''
        Main menu for user.
        q - exit
        1 show board
        2 show players
        3 show game info
        4 buy field from another player
        5 end turn
        '''
        while True:
            choice = self.interface().input_main_menu()
            if choice == 'q':
                self.exit()
            elif choice == '1':
                self.board()
            elif choice == '2':
                self.show_players()
            elif choice == '3':
                self.game_info()
            elif choice == '4':
                self.player_buy_from_another_player()
            elif choice == '5':
                return

    # BOARD

    def board(self):
        '''
        Show fields and players pawns.
        '''
        fields = self.game().fields()
        players = self.game().players()
        current_player = players[self.game().current_player_id()]
        while True:
            choice = self.interface().input_board()
            if choice == 'q':
                return
            else:
                card = fields[choice]
                if isinstance(card, BuyableField):
                    owner = card.owner()
                    if owner == current_player:
                        self.card_action(card)
                    else:
                        self.card(card)
                else:
                    self.card(card)

    def card(self, card):
        '''
        Show property belongs to another player.
        '''
        while True:
            choice = self.interface().card(card)
            if choice == 'q':
                return
            else:
                continue

    # PLAYERS

    def show_players(self):
        '''
        Show list of players.
        Allows to open player detailed info.
        '''
        while True:
            players = self.game().players()
            choice = self.interface().input_show_players(players)
            if choice == 'q':
                return
            else:
                self.show_player(choice)

    def show_player(self, id):
        '''
        Shows detailed info of chosen player.
        Allows to show player's fields.
        '''
        while True:
            player = self.game().players()[id]
            choice = self.interface().input_show_player(player)
            if choice == 'q':
                return
            if choice == '1':
                self.show_cards(player)

    def show_cards(self, player):
        '''
        Shows fields belongs to choosen player.
        Allows to show detailed card info.
        '''
        current_player = self.game().players()[self.game().current_player_id()]
        while True:
            cards = player.fields()
            choice = self.interface().input_show_cards(cards)
            if choice == 'q':
                return
            else:
                card = cards[choice]
                if player == current_player:
                    self.card_action(card)
                else:
                    self.card(card)

    # GAME INFO

    def game_info(self):
        '''
        Shows game info screen.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        round = self.game().current_round()
        number_of_rounds = self.game().number_of_rounds()
        while True:
            choice = self.interface().input_game_info(player, round,
                                                      number_of_rounds)
            if choice == 'q':
                return
            else:
                continue

    # CARD ACTIONS

    def card_action(self, field):
        '''
        Shows player's interaction with his fields.
        q - go back
        1 mortage field
        2 end mortage
        3 sell to bank
        4 build house
        5 sell house
        6 put up for auction
        '''
        current_player = self.game().players()[self.game().current_player_id()]
        while True:
            choice = self.interface().card_action(field)
            if choice == 'q':
                return
            if choice == '1':
                # mortage
                self.mortage(field)
            if choice == '2':
                # end mortage
                self.end_mortage(field)
            if choice == '3':
                # sell property to bank
                self.sell_to_bank(field)
            if choice == '4':
                # build house
                self.build_house(field)
            if choice == '5':
                # sell house
                self.sell_house(field)
            if choice == '6':
                # auction
                self.put_for_auction(field)

            if field.owner() != current_player:
                '''
                when field has a new owner we shouldn't
                see a card action menu because we cannot
                do anything with this
                '''
                return

    def mortage(self, field):
        '''
        Mortage screen.
        ask if player want to mortage field.
        1 - confirm
        2 - deny
        '''

        choice = self.interface().ask_mortage(field)
        if choice == '1':
            try:
                field.start_mortage()
                self.interface().mortaged_message(field)
                # go_back = True
            except BuiltUpError:
                self.interface().field_has_buildings_message()
            except AlreadyMortagedError:
                self.interface().already_mortaged_message()
            if choice == '2':
                return

    def end_mortage(self, field):
        '''
        End mortage screen.
        ask if player want to end mortage of field.
        1 - confirm
        2 - deny
        '''
        choice = self.interface().ask_end_mortage(field)
        if choice == '1':
            try:
                field.end_mortage()
                self.interface().end_mortage_message(field)
            except NotMortagedError:
                self.interface().not_mortaged_message(field)
            except NoMoneyError:
                self.interface().no_money_message()
        if choice == '2':
            return

    def sell_to_bank(self, field):
        '''
        Selling to bank screeen.
        ask if player want to sell field.
        1 - confirm
        2 - deny
        '''
        choice = self.interface().ask_sold_to_bank(field)
        if choice == '1':
            try:
                field.owner().sell_to_bank(field)
                self.interface().sold_to_bank_message(field)
            except AlreadyMortagedError:
                self.interface().already_mortaged_message()
            except BuiltUpError:
                self.interface().field_has_buildings_message()
        if choice == '2':
            return

    def build_house(self, field):
        '''
        ask if player want to build house on field.
        1 - confirm
        2 - deny
        '''
        if not isinstance(field, Property):
            self.interface().build_not_on_property_message()
        else:
            choice = self.interface().ask_build_house(field)
            if choice == '1':
                try:
                    field.build_house()
                    self.interface().house_build_message()
                except ValueError:
                    self.interface().build_not_on_property_message()
                except AlreadyMortagedError:
                    self.interface().already_mortaged_message()
                except NotOwnedDistrictError:
                    self.interface().not_owned_district_message()
                except PropertyLevelError:
                    self.interface().max_level_message()
                except UnequalBuildingError:
                    self.interface().unequal_building_message()
                except NoMoneyError:
                    self.interface().no_money_message()
            if choice == '2':
                return

    def sell_house(self, field):
        '''
        ask if player want to sell house from field.
        1 - confirm
        2 - deny
        '''
        if not isinstance(field, Property):
            self.interface().build_not_on_property_message()
        else:
            choice = self.interface().ask_sell_house(field)
            if choice == '1':
                try:
                    field.remove_house()
                    self.interface().house_sold_message()
                except PropertyLevelError:
                    self.interface().min_level_message()
                except UnequalBuildingError:
                    self.interface().unequal_selling_message()
            if choice == '2':
                return

    def put_for_auction(self, field):
        '''
        Action of put field on auction by player.
        '''
        if field.mortaged():
            self.interface().already_mortaged_message()
        elif isinstance(field, Property) and field.field_in_district_has_buildings():
            self.interface().field_has_buildings_message()
        else:
            start_price = self.interface().input_price()
            self.auction(field, start_price)

    # TRADE WITH PLAYERS

    def player_buy_from_another_player(self):
        '''
        Shows list of fields avaliable to buy.
        Allows to choose field that player want to buy.
        '''
        choosen = False
        while not choosen:
            avaliable_fields = self.game().fields_for_sell()
            choice = self.interface().show_fields_for_sell(avaliable_fields)
            if choice == 'q':
                return
            else:
                field = avaliable_fields[choice]
                self.ask_to_buy(field)
                choosen = True

    def ai_buy_from_another_player(self, missing_id):
        '''
        Ai ask to buy players who have fields that Ai want to buy.
        '''
        avaliable_fields = self.game().fields_for_sell()
        for id in avaliable_fields:
            if id == missing_id:
                field = avaliable_fields[id]
                self.ask_to_buy(field)

    def ask_to_buy(self, field):
        '''
        Ask owner of field to buy.
        '''
        owner = field.owner()
        if isinstance(owner, AiPlayer):
            self.ai_owned_trade(field)
        else:
            self.human_owned_trade(field)

    def ai_owned_trade(self, field):
        '''
        Reply from AiPlayer to trade offer.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        owner = field.owner()
        price = owner.pricing(field)
        if isinstance(player, AiPlayer):
            # ai reply to pricing
            self.ai_reply_for_pricing(field, price)
        else:
            self.human_reply_for_price(field, price)

    def ai_reply_for_pricing(self, field, price):
        '''
        Ai reply to field pricing.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        want_to_buy = player.reply_for_pricing(field, price)
        if want_to_buy:
            self.game().make_deal(player, field, price)
            self.interface().bought_message(field)
        else:
            self.interface().not_buy_message(player, field)

    def human_reply_for_price(self, field, price):
        '''
        Human reply for field pricing.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        owner = field.owner()
        reply = self.interface().reply_for_price(price, owner)
        if reply == '1':
            try:
                self.game().make_deal(player, field, price)
                self.interface().bought_message(field)
            except NoMoneyError:
                self.interface().no_money_message()
        if reply == '2':
            self.interface().not_buy_message(player, field)

    def human_owned_trade(self, field):
        '''
        Reply from human player to trade offer.
        1 - input owner's field pricing
        2 - not for trade
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        owner = field.owner()
        choice = self.interface().ask_to_buy(player, field)
        if choice == '1':
            price = self.interface().input_price()
            if isinstance(player, AiPlayer):
                # ai reply to pricing
                self.ai_reply_for_pricing(field, price)
            else:
                self.human_reply_for_price(field, price)
        if choice == '2':
            self.interface().not_for_trade_message(owner)
            return

    # TURN

    def ai_actions(self):
        '''
        Action which Ai can do during its turn.
        Equivalent to main_menu for human player.
        '''
        player = self.game().players()[self.game().current_player_id()]
        fields = player.fields()
        missing_ids = player.missing_fields_ids(self.game().fields())
        for id in missing_ids:
            self.ai_buy_from_another_player(id)
        build_houses_ids = player.build_houses_ids()
        for id in build_houses_ids:
            field = fields[id]
            if player.want_to_upgrade(field.house_price()):
                try:
                    field.build_house()
                except AlreadyMortagedError:
                    pass
                except NotOwnedDistrictError:
                    pass
                except PropertyLevelError:
                    pass
                except UnequalBuildingError:
                    pass

    def turn(self):
        '''
        Current player turn.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        if player.arrested():
            if isinstance(player, AiPlayer):
                self.ai_arrested_turn()
            else:
                self.player_arrested_turn()
        else:
            self.normal_turn()

    def normal_turn(self):
        '''
        Turn of human player if he is not in prison.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        field = self.game().fields()[player.position()]
        while True:
            # rolls two dices and gives message to user
            dices_result = self.game().roll_dices()
            self.interface().dices_message(dices_result)

            # arrest player if he has 3 doubles in row
            if player.doubles_in_row() == 3:
                player.reset_doubles()
                self.game().arrest(player)
                self.interface().arrest_player_message()
                return  # end turn if player go to jail

            # moves player to new field
            self.move_action(dices_result)

            # do an action of field
            self.field_action()

            if player.is_bancrupt():
                return  # end turn if player has bancrupt

            if isinstance(field, GoToJail):
                return  # end turn if player go to jail

            if not isinstance(player, AiPlayer):
                self.main_menu()
            else:
                self.ai_actions()
            # if player roll double has next move
            if player.doubles_in_row() != 0:
                continue
            else:
                return

    def ai_arrested_turn(self):
        '''
        Turn of arrested AI player.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        if player.want_to_stay_in_jail(self.game().current_round()):
            self.try_to_roll()
        else:
            # player want to leave jail
            if player.use_card_decision():
                # use card
                self.try_to_use_card()
            elif player.deposit_decision():
                # pay deposit
                self.try_to_pay_deposit()
            else:
                self.try_to_roll()

    def player_arrested_turn(self):
        '''
        Human player turn if he is in jail.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        self.main_menu()
        end = False
        while not end:
            jail_round = player.in_jail_round()
            choice = self.interface().input_jail_menu(player)
            if choice == '1':
                self.try_to_roll()
            if choice == '2':
                self.try_to_pay_deposit()
            if choice == '3':
                self.try_to_use_card()
            end = jail_round != player.in_jail_round()

    def try_to_roll(self):
        '''
        Action when player try to roll the dice to get out of jail.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        dices_result = player.dices()
        self.interface().dices_message(dices_result)

        if dices_result[0] == dices_result[1]:
            # leave jail
            self.game().leave_jail(player)
            self.interface().leave_jail_message()
            self.move_action(dices_result)
            self.field_action()
            if player.is_bancrupt():
                # end turn if player become bancrupt
                return

            if not isinstance(player, AiPlayer):
                # shows menu only to human player
                self.main_menu()
            else:
                self.ai_actions()

        elif player.in_jail_round() == 3:
            # try to pay deposit
            if not isinstance(player, AiPlayer):
                self.interface().pay_deposit()

            self.force_to_pay(player, DEPOSIT)
            if player.is_bancrupt():
                # end turn if player become bancrupt
                return
            else:
                self.game().leave_jail(player)
                self.interface().leave_jail_message()
                self.move_action(dices_result)
                self.field_action()
                if not isinstance(player, AiPlayer):
                    # shows menu only to human player
                    self.main_menu()
                else:
                    self.ai_actions()
        else:
            # stay in jail
            self.interface().stay_in_jail_message()
            player.next_jail_round()

    def force_to_pay(self, player, value, receiver=None):
        '''
        Force player to pay. If player has not enough money
        calls no_money_action method
        receiver deafults None means bank
        '''
        paid = False
        while not paid:
            try:
                player.substract_money(value)
                if receiver is not None:
                    receiver.add_money(value)
                paid = True
            except NoMoneyError:
                self.no_money_action(value, receiver)
            if player.is_bancrupt():
                return

    def try_to_pay_deposit(self):
        '''
        Player pays a deposit if he have enough money
        else nothing happens.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        try:
            player.substract_money(DEPOSIT)
            self.game().leave_jail(player)
            self.interface().leave_jail_message()
        except NoMoneyError:
            if not isinstance(player, AiPlayer):
                self.interface().no_money_message()

    def try_to_use_card(self):
        '''
        Player tries to use card to get out of jail.
        If he doesn't have nothing happens.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        try:
            player.use_get_out_card()
            self.game().leave_jail(player)
            self.interface().leave_jail_message()
        except ValueError:
            if not isinstance(player, AiPlayer):
                self.interface().no_get_out_of_jail_cards()

    # MOVES

    def move_action(self, dices_result):
        '''
        Action of player moving.
        Moves player to new position.
        Show message on screen
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        player.move(sum(dices_result))
        if player.pass_start():
            # gives payment and print messages of move and payment
            field = self.game().fields()[player.position()]
            player.get_payment()
            self.interface().move_message(dices_result, field)
            self.interface().start_payment_message()
        else:
            # print message of move
            field = self.game().fields()[player.position()]
            self.interface().move_message(dices_result, field)

    def field_action(self):
        '''
        Action after standing on fields.
        DrawField - draw
        GoToJail - put player to jail
        Tax - pay tax
        BuyableField - actions of buyable field
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        field = self.game().fields()[player.position()]

        if isinstance(field, DrawField):
            self.draw()

        elif isinstance(field, GoToJail):
            self.arrest(player)

        elif isinstance(field, Tax):
            # player pay tax
            # print message of tax
            self.pay_tax()

        elif isinstance(field, BuyableField):
            # stand on buyable action
            self.stand_on_buyable()

    def arrest(self, player):
        '''
        Put player to jail and display message.
        '''
        self.game().arrest(player)
        self.interface().arrest_player_message()

    # CHANCES

    def draw(self):
        '''
        Draw chance card,
        display message,
        do card action.
        '''
        card_id = self.game().draw_card()
        self.interface().chance_drawn_message(card_id)
        self.chance(card_id)

    def chance(self, id):
        '''
        Actions launched when player draw a card.
        '''
        player = self.game().players()[self.game().current_player_id()]
        if id == 0:
            # tax refund
            tax = 30
            player.add_money(tax)

        elif id == 1:
            # go to jail
            self.game().arrest(player)

        elif id == 2:
            # tax_refund
            tax = 150
            player.add_money(tax)

        elif id == 3:
            # found a wallet
            in_wallet = 10
            player.add_money(in_wallet)

        elif id == 4:
            # holidays
            pass

        elif id == 5:
            # PIPR condition
            condition = 200
            self.force_to_pay(player, condition)

        elif id == 6:
            # add jail left card
            player.add_get_out_cards()

        elif id == 7:
            # get dividend
            dividend = 50
            player.add_money(dividend)

        elif id == 8:
            # underpayment of tax
            fields_number = len(player.fields())
            tax_per_field = 20
            amount = fields_number * tax_per_field
            self.force_to_pay(player, amount)

        elif id == 9:
            # pay fine
            fine = 15
            self.force_to_pay(player, fine)

        elif id == 10:
            # renovation
            houses = player.count_houses()
            price_per_house = 25
            amount = houses * price_per_house
            self.force_to_pay(player, amount)

        elif id == 11:
            # tax overpayment
            fields_number = len(player.fields())
            tax_per_field = 20
            amount = fields_number * tax_per_field
            player.add_money(amount)

        elif id == 12:
            # inheritance
            inheritance = 100
            player.add_money(inheritance)

        elif id == 13:
            # pay tax
            tax = 100
            self.force_to_pay(player, tax)
        elif id == 14:
            # go to jail
            self.game().arrest(player)

        elif id == 15:
            # find scratch card
            dices = player.dices()
            win = sum(dices)
            if dices[0] == dices[1]:
                win = win * dices[0]
            player.add_money(win)
            self.interface().scratch_card(dices, win)

        elif id == 16:
            # add jail left card
            player.add_get_out_cards()

    # TAX

    def pay_tax(self):
        '''
        Action of standing on Tax field.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        tax = self.game().fields()[player.position()]
        self.force_to_pay(player, tax.value())
        if player.is_bancrupt():
            return
        else:
            self.interface().pay_tax_message(tax.value())

    # BUYABLE FIELDS ACTIONS

    def stand_on_buyable(self):
        '''
        When player stand on buyable field
        if field is mortaged nothing happens,
        if field is owned by this player nothing happens,
        if field is owned by other player there is a rent action
        if field is bank owned there is bank owned action
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        field = self.game().fields()[player.position()]
        if field.mortaged():
            # print message that field is mortaged
            self.interface().mortaged_message(field)
        elif field.owner() is None:
            # print bank owned menu
            self.bank_owned()
        else:
            if field.owner().id() == player.id():
                # print message that field is owned by current player
                self.interface().already_owned_message(field)
            else:
                # pay rent action
                self.rent()

    def bank_owned(self):
        '''
        Check if player is AI.
        If player is ai than calls ai action.
        Else calls player action
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        if isinstance(player, AiPlayer):
            self.bank_owned_ai()
        else:
            self.bank_owned_human()

    def bank_owned_human(self):
        '''
        Player can buy field or pass and put up for auction.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        field = self.game().fields()[player.position()]
        while True:
            choice = self.interface().bank_owned_menu(field)
            if choice == '1':
                # buy
                try:
                    player.buy_from_bank(field)
                    self.interface().bought_message(field)
                    return
                except NoMoneyError:
                    self.interface().no_money_message()
                    continue
            if choice == '2':
                # auction
                self.auction(field)
                return

    def bank_owned_ai(self):
        '''
        Ai choice to buy field or put for auction.
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        field = self.game().fields()[player.position()]
        if player.want_to_buy(field):
            player.buy_from_bank(field)
            self.interface().bought_message(field)
        else:
            self.auction(field)

    def rent(self):
        '''
        Action of rent player has to pay.
        Gets rent from player and gives it to owner.
        if player has no money checks bancruption
        '''
        id = self.game().current_player_id()
        player = self.game().players()[id]
        field = self.game().fields()[player.position()]
        owner = field.owner()
        if isinstance(field, Property):
            rent = field.get_rent()
        elif isinstance(field, Station):
            rent = field.get_rent()
        elif isinstance(field, Service):
            dices = player.dices()
            rent = field.get_rent(dices)
            self.interface().dices_message(dices)

        self.interface().pay_rent_message(rent, owner)

        self.force_to_pay(player, rent, owner)

    # AUCTION

    def auction(self, field, start_bid=START_BID):
        '''
        Auction of field. It takes until only one participant
        left or if nobody make a bid.
        Param start_bid is given when it is auction of player's owned field.
        '''
        id = self.game().current_player_id()
        participants = self.game().bidding_players()
        current_bid = start_bid
        winner_id = None
        made_first_bid = False
        while True:
            id = self.game().next_bidder_id(id, participants)
            bidder = participants[id]
            if isinstance(bidder, AiPlayer):
                # ai auction
                if bidder.want_to_bid(current_bid, field):
                    if not made_first_bid:
                        bid = start_bid
                    else:
                        bid = bidder.bid(current_bid)
                    current_bid = bid
                    winner_id = bidder.id()
                    self.interface().successfully_made_bid(bidder, bid)
                    made_first_bid = True
                else:
                    del participants[id]
                    self.interface().pass_message(bidder)
            else:
                # human auction
                while True:
                    choice = self.interface().player_auction(field, bidder, current_bid)
                    if choice == '1':
                        #
                        if not made_first_bid:
                            input = self.interface().make_first_bid(current_bid, bidder)
                        else:
                            input = self.interface().make_bid(current_bid, bidder)
                        if input == 'q':
                            continue
                        elif bidder.money() < input:
                            self.interface().no_money_message()
                            continue
                        else:
                            # somebody make a bid
                            current_bid = input
                            winner_id = bidder.id()
                            winner = participants[winner_id]
                            self.interface().successfully_made_bid(winner, current_bid)
                            made_first_bid = True
                            break
                    if choice == '2':
                        # player passed
                        del participants[id]
                        self.interface().pass_message(bidder)
                        break

            if len(participants) == 0:
                # all players passed
                self.interface().nobody_make_bid()
                return

            elif len(participants) == 1 and winner_id is not None:
                # there is winner
                winner = participants[winner_id]
                self.game().make_deal(winner, field, current_bid)
                self.interface().winner_of_bid(winner, current_bid)
                return

            else:
                # next turn of auction
                continue

    # BANCRUPTION

    def no_money_action(self, amount, creditor=None):
        '''
        Check if player can pay if he sell his fields.
        If no player is a bancrupt and is out the game.
        If yes calls the make money action.
        '''
        player = self.game().players()[self.game().current_player_id()]
        if player.can_pay(amount):
            # sell sth
            self.make_money(amount)
        else:
            # player bancrupt
            self.interface().bancrupt(player)
            if creditor is None:

                # bank takes over player's fortune
                self.interface().bank_take_over_fortune(player)
                fields = [field for field in player.fields().values()]

                # prepare fields to auction
                self.game().debt_to_bank()

                # puts all fields for auction
                for field in fields:
                    self.auction(field)
            else:
                # creditor takes over player's fortune
                self.interface().creditor_take_over_fortune(creditor, player)
                self.game().debt_to_player(creditor)

    def make_money(self, amount):
        '''
        Player choose what he want to sell to bank.
        Ends when player can pay the debt.
        '''
        player = self.game().players()[self.game().current_player_id()]
        if isinstance(player, AiPlayer):
            self.ai_make_money(amount)
        else:
            self.human_make_money(amount)

    def ai_make_money(self, debt):
        '''
        try to sell houses
        if not earned earn from fields.
        '''
        player = self.game().players()[self.game().current_player_id()]
        if not player.earn_from_houses(debt):
            player.earn_from_fields(debt)

    def human_make_money(self, amount):
        '''
        Player choose what he want to sell to bank.
        Ends when player can pay the debt.
        '''
        player = self.game().players()[self.game().current_player_id()]
        while player.money() < amount:
            choice = self.interface().make_money(player, amount)
            card = player.fields()[choice]
            self.make_money_card(card)
        self.interface().player_can_pay_message()

    def make_money_card(self, card):
        '''
        Player choose what to do with field to earn money to pay debt.
        '''
        choice = self.interface().make_money_card(card)
        if choice == 'q':
            # choose another card
            return
        if choice == '1':
            # mortage
            self.mortage(card)
        if choice == '2':
            # sell to bank
            self.sell_to_bank(card)
        if choice == '3':
            # sell house
            self.sell_house(card)

    # END OF GAME

    def chcek_end(self):
        '''
        Check if game has to finish.
        Firstly if remainded only one player
            game ends and shows end screen
        Secondely if player entered numnber of rounds
            find players who have biggest fortune, end game
        '''
        if self.game().one_remainded():
            # find one who left
            winner = self.game().simple_winner()
            # show end screen
            self.interface().simple_winner(winner)
            # set game finished
            self.game().set_finished()
        elif self.game().reached_number_of_rounds():
            # find richest players
            winners = self.game().richest_players()
            # show end screen
            self.interface().calculated_winners(winners)
            # set game finished
            self.game().set_finished()

    def exit(self):  # WORKS
        '''
        Prints goodbye.
        Turn off game.
        '''
        self.interface().print_exit()
        sys.exit()

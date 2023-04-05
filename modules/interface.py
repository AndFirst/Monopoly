from modules.constants import (MIN_NUMBER_OF_PLAYERS, MAX_NUMBER_OF_PLAYERS,
                               MAX_NAME_LENGTH, MIN_NUMBER_OF_ROUNDS, PAYMENT,
                               NUMBER_OF_FIELDS, DEPOSIT, BID_DIFFERENCE)
from modules.chances import CHANCES


class Interface:
    '''
    Class Interface. Comunicate with user. Frontend of Monopoly game.
    '''
    def __init__(self, game):
        self._game = game

    def game(self):
        return self._game

    def new_line(self):
        '''
        Jump to new line.
        '''
        print('\n')

    def clear(self):
        '''
        Clear terminal.
        '''
        print('\033c')

    def freeze(self):
        '''
        Freeze screen until player input sth.
        '''
        input('Naciśnij, żeby przejść dalej.')

    def head(self):
        '''
        Prints head with informations of current palyer.
        If current player is bancrupt e.g. auction of bancrupt's fields
        head does not appear.
        '''
        player = self.game().players()[self.game().current_player_id()]
        if player.is_bancrupt():
            pass
        else:
            field = self.game().fields()[player.position()]
            text = f'Gracz: {player.name()}\n'\
                f'Stan konta: {player.money()}\n'\
                f'Stoi na polu: {field.id()} {field.name()}\n\n'
            print(text)

    def print_intro(self):
        '''
        Prints intro menu.
        '''
        self.clear()
        text = 'Witaj w Monopoly!\n'\
            '1 Graj.\n'\
            'q Wyjdź.\n'
        print(text)

    def intro_choice(self):
        '''
        Gets intro input from user.
        '''
        while True:
            self.print_intro()
            choice = input('Twój wybór:')
            if choice in ('q', '1'):
                return choice
            else:
                continue

    def print_exit(self):
        '''
        Prints message at the end of game.
        '''
        self.clear()
        print('Dziękuję za grę.')
        self.freeze()

    def print_players_number_info(self):
        '''
        Prints instruction of adding players.
        '''
        min = MIN_NUMBER_OF_PLAYERS
        max = MAX_NUMBER_OF_PLAYERS
        self.clear()
        text = f'Możesz dodać od {min} do {max} graczy.\n'\
            'Pierwszy gracz musi być człowiekiem.\n'\
            'Pozostali mogą być sterowani przez komputer\n'
        print(text)
        self.freeze()

    def print_player_names_info(self):
        '''
        Prints instruction of players names.
        '''
        self.clear()
        text = 'Podaj nazwy graczy.\n'\
            'Nazwa nie może być pusta.\n'\
            f'Maksymalnie {MAX_NAME_LENGTH} znaków.\n'
        print(text)
        self.freeze()

    def input_players_number(self):
        '''
        Gets number of players from user.
        '''
        min = MIN_NUMBER_OF_PLAYERS
        max = MAX_NUMBER_OF_PLAYERS
        while True:
            self.clear()
            number = input('Podaj liczbę graczy:')
            try:
                number = int(number)
            except ValueError:
                continue
            if not min <= number <= max:
                continue
            else:
                return number

    def input_player_name(self):
        '''
        Gets player name from user.
        '''
        while True:
            self.clear()
            name = input('Podaj nazwę:')
            if not 0 < len(name) <= MAX_NAME_LENGTH:
                self.incorrect_name(name)
                continue
            else:
                return name

    def incorrect_name(self, name=''):
        '''
        Message when name is incorrect.
        '''
        self.clear()
        text = f'Nazwa {name} jest niepoprawna.'
        print(text)
        self.freeze()

    def add_successfully(self, name):
        '''
        Message when added player.
        '''
        self.clear()
        text = f'Pomyślnie dodano gracza {name}'
        print(text)
        self.freeze()

    def print_ai_choice(self, name):
        '''
        Prints ai adding menu.
        '''
        self.clear()
        text = f'Czy gracz {name} ma być sterowany przez komputer?\n'\
            '1 Tak\n'\
            '2 Nie\n'
        print(text)

    def ai_choice(self, name):
        '''
        Gets player ai choice from user.
        '''
        while True:
            self.print_ai_choice(name)
            choice = input('Twój wybór:')
            if choice in ('1', '2'):
                return choice
            else:
                continue

    def print_input_rounds(self):
        self.clear()
        text = 'Czy chcesz podać liczbę rund po której gra się zakończy?\n'\
            '1 Tak\n'\
            '2 Nie\n'
        print(text)

    def input_rounds(self):
        '''
        Gets number of rounds from user.
        '''
        while True:
            self.print_input_rounds()
            choice = input('Twój wybór:')
            if choice == '1':
                while True:
                    self.clear()
                    number_of_rounds = input('Podaj liczbę rund:')
                    if not number_of_rounds.isdigit():
                        continue
                    number_of_rounds = int(number_of_rounds)
                    if number_of_rounds < MIN_NUMBER_OF_ROUNDS:
                        continue
                    else:
                        return number_of_rounds
            elif choice == '2':
                return
            else:
                continue

    def print_main_menu(self):
        '''
        Prints main menu.
        '''
        self.clear()
        self.head()
        text = 'q Wyjdź z gry\n'\
               '1 Wyświetl planszę\n'\
               '2 Wyświetl graczy\n'\
               '3 Wyświetl informacje o grze\n'\
               '4 Kup nieruchomość od innego gracza\n'\
               '5 Zakończ swój ruch\n'
        print(text)

    def input_main_menu(self):
        '''
        Gets main menu choice from user.
        '''
        while True:
            self.print_main_menu()
            choice = input('Twój wybór:')
            if choice in ('q', '1', '2', '3', '4', '5'):
                return choice
            else:
                continue

    def print_board(self):
        '''
        Prints board.
        Color property on property district color.
        '''
        fields = self.game().fields()
        players = self.game().players()
        self.clear()
        self.head()
        for field in fields.values():
            line = field.short_description()
            for player in players.values():
                if player.position() == field.id():
                    line += f' |{player.id()} {player.name()}|'
            print(line)
        self.new_line()
        text = 'q Wyjdź do menu głównego.\n'\
            'Aby wyświetlić dane pole podaj jego ID.'
        print(text)

    def input_board(self):
        '''
        Gets id of field which user want to show.
        '''
        while True:
            self.print_board()
            choice = input('Twój wybór:')
            if choice == 'q':
                return choice
            elif not choice.isdigit():
                continue
            choice = int(choice)
            min_id = 0
            max_id = NUMBER_OF_FIELDS - 1
            if min_id <= choice <= max_id:
                return choice
            else:
                continue

    def card(self, card):
        '''
        Prints field description.
        Gets back input from user.
        '''
        while True:
            self.clear()
            self.head()
            print(card.description())
            text = 'q Wróć.\n'
            print(text)
            choice = input('Twój wybór:')
            if choice == 'q':
                return choice
            else:
                continue

    def card_action(self, card):
        '''
        Menu of fields owned by current player.
        '''
        while True:
            self.clear()
            self.head()
            print(card.description())
            self.new_line()
            menu = 'q Wróć.\n'\
                '1 Zastaw nieruchomość.\n'\
                '2 Wykup zastaw.\n'\
                '3 Sprzedaj nieruchomość do banku\n'\
                '4 Zbuduj domek.\n'\
                '5 Sprzedaj domek do banku.\n'\
                '6 Sprzedaj innemu graczowi (aukcja)\n'
            print(menu)
            choice = input('Twój wybór:')
            if choice in ('q', '1', '2', '3', '4', '5', '6'):
                return choice
            else:
                continue

    def print_players(self, players):
        '''
        Prints players list.
        '''
        self.clear()
        self.head()
        for player in players.values():
            print(player.short_description())
        self.new_line()
        text = 'q Wyjdź do menu głównego.\n'\
            'Aby wyświetlić danego gracza podaj jego ID.'
        print(text)

    def input_show_players(self, players):
        '''
        Gets id of player, user want to show.
        '''
        while True:
            self.print_players(players)
            choice = input('Twój wybór:')
            if choice == 'q':
                return choice
            elif not choice.isdigit():
                continue
            choice = int(choice)
            min_id = 0
            max_id = len(players) - 1
            if min_id <= choice <= max_id:
                return choice
            else:
                continue

    def input_show_player(self, player):
        '''
        Prints player detailed description.
        Gives possibility to see player's fields.
        '''
        while True:
            self.clear()
            print(player.description())
            text = 'q Wróć.\n'\
                '1 Wyświetl nieruchomości'
            print(text)
            choice = input('Twój wybór:')
            if choice in ('q', '1'):
                return choice
            else:
                continue

    def print_cards(self, cards):
        '''
        Prints choosen player's cards.
        '''
        for card in cards.values():
            print(card.short_description())
        text = 'q Wróć.\n'\
            'Aby wyświetlić daną kartę podaj jej ID.'
        print(text)

    def input_show_cards(self, cards):
        '''
        Gives possibility to see detailed description
        of choosen card.
        '''
        while True:
            self.clear()
            self.head()
            self.print_cards(cards)
            choice = input('Twój wybór:')
            if choice == 'q':
                return choice
            elif not choice.isdigit():
                continue
            choice = int(choice)
            if choice in cards:
                return choice
            else:
                continue

    def input_game_info(self, player, round, rounds):
        '''
        Shows informations about game state:
            type of game ending
            given number of rounds
            current round
        '''
        while True:
            self.clear()
            self.head()
            if rounds is None:
                print('Gra będzie trwała, aż zostanie tylko jeden gracz.')
            else:
                print(f'Gra zostanie rozstrzygnięta po {rounds} rundach')
            text = f'Obecna runda: {round}\n'\
                f'Kolejka gracza: {player.name()}\n'\
                'q Wyjdź\n'
            print(text)
            choice = input('Twój wybór:')
            if choice == 'q':
                return choice
            else:
                continue

    def show_fields_for_sell(self, fields):
        while True:
            self.clear()
            self.head()
            for field in fields.values():
                print(field.short_description())
            text = 'q wyjdź\n'\
                'Aby wybrać pole, które chcesz kupić podaj jego ID.\n'
            print(text)
            choice = input('Twój wybór:')
            if choice == 'q':
                return choice
            elif not choice.isdigit():
                continue
            choice = int(choice)
            if choice in fields or choice == 'q':
                return choice

    def dices_message(self, result):
        '''
        Prints message about result of dices roll.
        '''
        self.clear()
        self.head()
        text = f'Gracz wyrzucił {result[0]}, {result[1]} oczek.'
        print(text)
        self.freeze()

    def move_message(self, result, field):
        '''
        Prints message about player's move.
        '''
        self.clear()
        self.head()
        text = f'Gracz przesuwa się o {sum(result)} pól.\n'\
            f'Gracz staje na polu {field.id()} {field.name()}.'
        print(text)
        self.freeze()

    def start_payment_message(self):
        '''
        Prints message when player pass Start and gets payment.
        Waits for click.
        '''
        self.clear()
        self.head()
        text = f'Gracz przekracza Start i otrzymuje wypłatę {PAYMENT}'
        print(text)
        self.freeze()

    def arrest_player_message(self):
        '''
        Prints message when player goes to jail.
        '''
        self.clear()
        self.head()
        text = 'Gracz trafia to więzienia.\n'
        print(text)
        self.freeze()

    def pay_tax_message(self, value):
        '''
        Print pessage when player have to pay tax.
        '''
        self.clear()
        self.head()
        text = f'Gracz musi zapłacić {value} podatku.\n'
        print(text)
        self.freeze()

    def already_owned_message(self, field):
        '''
        Print message when player stand on buyable field
        that belongs to this player.
        '''
        self.clear()
        self.head()
        text = f'Pole {field.name()} należy już do tego gracza.\n'
        print(text)
        self.freeze()

    def bank_owned_menu(self, field):
        '''
        Print message when player stand on buyable field
        that belongs to bank.
        '''
        while True:
            self.clear()
            self.head()
            text = f'Nieruchomość {field.name()} należy do banku.\n'\
                f'Cena: {field.price()}\n'\
                '1 Kup nieruchomość.\n'\
                '2 Nie kupuj (odbędzie się licytacja)\n'
            print(text)
            choice = input('Twój wybór:')
            if choice in ('1', '2'):
                return choice
            else:
                continue

    def pay_rent_message(self, rent, owner):
        '''
        Print message when player stand on buyable field
        that belongs to another player.
        '''
        self.clear()
        self.head()
        text = f'Gracz stanął na polu należącym do gracza {owner.name()}.\n'\
            f'Musi zapłacić mu czynsz w wysokości {rent}.\n'
        print(text)
        self.freeze()

    def bought_message(self, field):
        '''
        Print message when player buy field.
        '''
        self.clear()
        self.head()
        text = f'Gracz zakupił nieruchomość {field.name()}\n'
        print(text)
        self.freeze()

    def no_money_message(self):
        '''
        Print message when player has not enough money.
        '''
        self.clear()
        self.head()
        text = 'Gracz nie posiada wystarczająco pieniędzy.\n'
        print(text)
        self.freeze()

    def no_get_out_of_jail_cards(self):
        '''
        Print message when player has no get out of jail cards.
        '''
        self.clear()
        self.head()
        print('Gracz nie posiada kart wyjścia z aresztu.\n')
        self.freeze()

    def input_jail_menu(self, player):
        '''
        Prints jail menu with options:
            1 try to roll double
            2 pay deposit
            3 use get out card
        '''
        while True:
            self.clear()
            self.head()
            in_jail_round = player.in_jail_round()
            text = f'Przebywasz w areszcie {in_jail_round} rundę.\n'\
                'Aby wyjść:\n'\
                '1 Spróbuj wyrzucić dublet.\n'\
                f'2 Zapłać kaucję w wysokości {DEPOSIT}\n'\
                '3 Użyj karty wyjścia z aresztu\n'
            print(text)
            choice = input('Twój wybór:')
            if choice in ('1', '2', '3'):
                return choice
            else:
                continue

    def pay_deposit(self):
        '''
        Message when player has to pay deposit.
        '''
        self.clear()
        self.head()
        text = f'Zapłać kaucję w wysokości {DEPOSIT} i wyjdź z aresztu\n'
        print(text)
        self.freeze()

    def leave_jail_message(self):
        '''
        Message when player leave jail.
        '''
        self.clear()
        self.head()
        text = 'Gracz wychodzi z aresztu.\n'
        print(text)
        self.freeze()

    def stay_in_jail_message(self):
        '''
        Message when player stays in jail.
        '''
        self.clear()
        self.head()
        text = 'Gracz zostaje w areszcie.'
        print(text)
        self.freeze()

    def player_auction(self, field, bidder, current_bid):
        '''
        Prints menu of auction with options:
            1 make bid
            2 pass
        '''
        while True:
            self.clear()
            text = f'Gracz {bidder.name()}\n'\
                f'Stan konta: {bidder.money()}\n\n'\
                f'Trwa licytacja pola {field.name()}.\n'\
                f'Obecna cena: {current_bid}\n'\
                '1 Licytuj.\n'\
                '2 Spasuj.\n'
            print(text)
            choice = input('Twój wybór:')
            if choice in ('1', '2'):
                return choice
            else:
                continue

    def pass_message(self, player):
        '''
        Message when player passed in auction.
        '''
        self.clear()
        text = f'Gracz {player.name()} spasował.\n'
        print(text)
        self.freeze()

    def invalid_bid_message(self):
        '''
        Message when player input wrong bid.
        '''
        self.clear()
        self.head()
        text = 'Oferta jest niepoprawna.\n'
        print(text)
        self.freeze()

    def make_bid(self, current_bid, player):
        '''
        Prints info about current bid.
        Allows to input bid or exit.
        Bid must be higher than current bid
        '''
        while True:
            self.clear()
            text = f'Gracz {player.name()}\n'\
                f'Stan konta: {player.money()}\n\n'\
                f'Obecna oferta: {current_bid}\n'\
                f'Oferta musi być większa o co najmniej {BID_DIFFERENCE}\n'\
                'q Zrezygnuj.\n'
            print(text)
            bid = input('Podaj swoją ofertę:')
            if bid == 'q':
                return bid
            elif not bid.isdigit():
                continue
            bid = int(bid)
            if bid < current_bid + BID_DIFFERENCE:
                self.invalid_bid_message()
                continue
            else:
                return bid

    def make_first_bid(self, current_bid, player):
        '''
        Prints info about first menu.
        Allows to input bid or exit.
        First bid have to be higher or equall to current bid
        '''
        while True:
            self.clear()
            text = f'Gracz {player.name()}\n'\
                f'Stan konta: {player.money()}\n\n'\
                f'Cena wywoławcza: {current_bid}\n'\
                'Twoja oferta nie może być niższa niż cena wywoławcza.\n'\
                'q Zrezygnuj.\n'
            print(text)
            bid = input('Podaj swoją ofertę:')
            if bid == 'q':
                return bid
            elif not bid.isdigit():
                continue
            bid = int(bid)
            if bid < current_bid:
                self.invalid_bid_message()
                continue
            else:
                return bid

    def successfully_made_bid(self, bidder, bid):
        '''
        Message when player made a bid.
        '''
        self.clear()
        self.head()
        text = f'Gracz {bidder.name()} złożył ofertę {bid}'
        print(text)
        self.freeze()

    def nobody_make_bid(self):
        '''
        Message when bid has no winner.
        '''
        self.clear()
        self.head()
        text = 'Aukcja zakończona.\n'\
            'Nikt nie złożył oferty za pole.\n'
        print(text)
        self.freeze()

    def winner_of_bid(self, winner, bid):
        '''
        Message with information about winner of bid.
        '''
        self.clear()
        self.head()
        text = f'Gracz {winner.name()} wygrał licytację.\n'\
            f'Ostateczna oferta: {bid}\n'
        print(text)
        self.freeze()

    def print_ask_to_buy(self, player, field):
        '''
        Message when another player want to buy field.
        Player have to give response:
            1 input price
            2 not for trade
        '''
        self.clear()
        self.head()
        name = field.name()
        owner = field.owner().name()
        text = f'Gracz {player.name()} chce kupić nieruchomość {name}\n'\
            f'Należy ona do gracza {owner}\n'\
            '1 Podaj cenę za jaką chcesz sprzedać.\n'\
            '2 Nie sprzedawaj za żadną cenę.\n'
        print(text)

    def ask_to_buy(self, player, field):
        '''
        User response to trade offer.
            1 input price
            2 not for trade
        '''
        while True:
            self.print_ask_to_buy(player, field)
            choice = input('Twój wybór:')
            if choice in ('1', '2'):
                return choice
            else:
                continue

    def input_price(self):
        '''
        Input pricing of field.
        '''
        while True:
            self.clear()
            self.head()
            price = input('Podaj cenę nieruchomości:')
            if not price.isdigit():
                continue
            price = int(price)
            if price < 0:
                continue
            else:
                return price

    def print_reply_for_price(self, price, owner):
        '''
        Prints asking for player's response to trade offer.
        '''
        self.clear()
        self.head()
        text = f'Gracz {owner.name()} wycenił nieruchomość na {price}.\n'\
            '1 Zgoda, kup nieruchomość.\n'\
            '2 Nie kupuj.\n'
        print(text)

    def reply_for_price(self, price, owner):
        '''
        Input reply for pricing.
        '''
        while True:
            self.print_reply_for_price(price, owner)
            choice = input('Twój wybór:')
            if choice in ('1', '2'):
                return choice
            else:
                continue

    def not_buy_message(self, player, field):
        '''
        Message when player not bought a field.
        '''
        self.clear()
        self.head()
        text = f'Gracz {player.name()} nie kupił pola {field.name()}.\n'
        print(text)
        self.freeze()

    def not_for_trade_message(self, owner):
        '''
        Message when player does not want to sell field.
        '''
        self.clear()
        self.head()
        text = f'Gracz {owner.name()} nie chce sprzedać nieruchomości.\n'
        print(text)
        self.freeze()

    def ask_sold_to_bank(self, field):
        '''
        Choice of selling field to bank.
            1 agree
            2 deny
        '''
        while True:
            self.clear()
            self.head()
            text = f'Nieruchomość {field.name()}.\n'\
                f'Sprzedaj za {field.mortage_value()}.\n'\
                '1 Tak\n'\
                '2 Nie\n'
            print(text)
            choice = input('Twój wybór:')
            if choice in ('1', '2'):
                return choice
            else:
                continue

    def field_has_buildings_message(self):
        '''
        Message when player cannot sell property because there are
        houses on field.
        '''
        self.clear()
        self.head()
        text = 'Działka w tej dzielnicy jest posiada budynki..\n'\
            'Sprzedaj je, aby sprzedać lub zastawić działkę.\n'
        print(text)
        self.freeze()

    def sold_to_bank_message(self, field):
        '''
        Message when player sell field to bank.
        '''
        self.clear()
        self.head()
        text = f'Sprzedano nieruchomość {field.name()} bankowi.\n'
        print(text)
        self.freeze()

    def ask_mortage(self, field):
        '''
        Choice of mortage field in bank.
            1 agree
            2 deny
        '''
        while True:
            self.clear()
            self.head()
            text = f'Nieruchomość {field.name()}.\n'\
                f'Zastaw za {field.mortage_value()}.\n'\
                '1 Tak\n'\
                '2 Nie\n'
            print(text)
            choice = input('Twój wybór:')
            if choice in ('1', '2'):
                return choice
            else:
                continue

    def mortaged_message(self, field):
        '''
        Message when field was mortaged.
        '''
        self.clear()
        self.head()
        text = f'Zastawiono nieruchomość {field.name()}\n'
        print(text)
        self.freeze()

    def already_mortaged_message(self):
        '''
        Message when field is already mortaged in bank.
        '''
        self.clear()
        self.head()
        text = 'Nieruchomość jest zastawiona w banku.\n'
        print(text)
        self.freeze()

    def not_mortaged_message(self, field):
        '''
        Message when player try to end mortage of not mortaged field.
        '''
        self.clear()
        self.head()
        text = f'Nieruchomość {field.name()} nie jest zastawiona.\n'
        print(text)
        self.freeze()

    def ask_end_mortage(self, field):
        '''
        Choice of ending mortage
            1 agree
            2 deny
        '''
        while True:
            self.clear()
            self.head()
            amount = int(1.1 * field.mortage_value())
            text = f'Czy chcesz wykupić zastaw {field.name()} za {amount}?\n'\
                '1 Tak\n'\
                '2 Nie\n'
            print(text)
            choice = input('Twój wybór:')
            if choice in ('1', '2'):
                return choice
            else:
                continue

    def end_mortage_message(self, field):
        '''
        Message when player end mortage of field.
        '''
        self.clear()
        self.head()
        text = f'Wykupiono zastaw nieruchomości {field.name()}\n'
        print(text)
        self.freeze()

    def ask_build_house(self, field):
        '''
        Choice of building house on property.
            1 agree
            2 deny
        '''
        while True:
            self.clear()
            self.head()
            text = f'Działka {field.name()}\n'\
                f'Zbuduj domek za {field.house_price()}.\n'\
                '1 Tak\n'\
                '2 Nie\n'
            print(text)
            choice = input('Twój wybór:')
            if choice in ('1', '2'):
                return choice
            else:
                continue

    def build_not_on_property_message(self):
        '''
        Message when player try to build house not on property.
        '''
        self.clear()
        self.head()
        text = 'Domki można budować tylko na działkach.\n'
        print(text)
        self.freeze()

    def house_build_message(self):
        '''
        Message when player built house.
        '''
        self.clear()
        self.head()
        text = 'Wybudowano domek.\n'
        print(text)
        self.freeze()

    def max_level_message(self):
        '''
        Message when player try to build house on property
        when it reached max level.
        '''
        self.clear()
        self.head()
        text = 'Nieruchomość osiągnęła już najwyższy poziom.\n'\
            'Nie można postawić na niej więcej domków.\n'
        print(text)
        self.freeze()

    def unequal_building_message(self):
        '''
        Message when player try to build house unequally.
        '''
        self.clear()
        self.head()
        text = 'Nie można zbudować domku na tej działce.\n'\
            'Ulepsz inne działki z tej dzielnicy!\n'
        print(text)
        self.freeze()

    def not_owned_district_message(self):
        '''
        Message when player want to build house when
        not all district is owned.
        '''
        self.clear()
        self.head()
        text = 'Nie można zbudować domku na tej działce.\n'\
            'Kup inne działki z tej dzielnicy!\n'
        print(text)
        self.freeze()

    def ask_sell_house(self, field):
        '''
        Choice of selling house to bank
            1 agree
            2 deny
        '''
        amount = int(field.house_price() / 2)
        while True:
            self.clear()
            self.head()
            text = f'Działka {field.name()}\n'\
                f'Sprzedaj domek za {amount}?\n'\
                '1 Tak\n'\
                '2 Nie\n'
            print(text)
            choice = input('Twój wybór:')
            if choice in ('1', '2'):
                return choice
            else:
                continue

    def house_sold_message(self):
        '''
        Print message when player sold house.
        '''
        self.clear()
        self.head()
        text = 'Sprzedano domek.\n'
        print(text)
        self.freeze()

    def min_level_message(self):
        '''
        Prints message when property has min level.
        '''
        self.clear()
        self.head()
        text = 'Nieruchomość nie posiada domków.\n'
        print(text)
        self.freeze()

    def unequal_selling_message(self):
        '''
        Print message when field downgrade is not equally.
        '''
        self.clear()
        self.head()
        text = 'Nie można sprzedać domku z tej działki.\n'\
            'Sprzedaj inne domki z tej dzielnicy!\n'
        print(text)
        self.freeze()

    def simple_winner(self, winner):
        '''
        Prints summary of game when all players bancrupt.
        '''
        self.clear()
        text = 'Gra zakończona.\n'\
            'Wszyscy zbankrutowali.\n'\
            f'Wygrał gracz {winner.name()}.\n'\
            'Gratualcje!\n'
        print(text)
        self.freeze()

    def calculated_winners(self, winners):
        '''
        Print summary of game when was given number of round.
        Prints winner or winners
        '''
        self.clear()
        if len(winners) == 1:
            winner = list(winners.values())[0]
            text = 'Osiągnięto podaną liczbę rund.\n'\
                'Zwycięża gracz, który uzbierał największy majątek.\n'\
                f'Wygrał gracz {winner.name()}\n'\
                'Gratulacje!\n'
        else:
            text = 'Osiągnięto podaną liczbę rund.\n'\
                f'{len(winners)} graczy uzbierało taki sam majątek:\n'
            for winner in winners.values():
                text += f'{winner.name()}\n'
            text += 'Gratulacje!\n'
        print(text)
        self.freeze()

    def bancrupt(self, player):
        '''
        Message when player becomes a bancrupt.
        '''
        self.clear()
        text = f'Gracz {player.name()} zbankrutował.\n'
        print(text)
        self.freeze()

    def make_money(self, player, amount):
        '''
        Prints a message about player's debt.
        Prints a list of fields that player can sell or mortage.
        '''
        while True:
            self.clear()
            self.head()
            fields = player.fields()
            text = f'Twoje zobowiązanie wynosi {amount}.\n'\
                'Sprzedaj coś, aby spłacić długi\n'\
                'Twoje nieruchomości:\n'
            print(text)
            self.print_cards(fields)
            choice = input('Twój wybór:')
            if not choice.isdigit():
                continue
            choice = int(choice)
            if choice in fields:
                return choice
            else:
                continue

    def make_money_card(self, card):
        '''
        Options of making money from choosen card.
        q back and choose another field
        1 mortage field
        2 sell field to bank
        3 sell house
        '''
        while True:
            self.clear()
            print(card.description())
            self.head()
            menu = 'q Wróć\n'\
                '1 Zastaw nieruchomość.\n'\
                '2 Sprzedaj nieruchomość do banku.\n'\
                '3 Sprzedaj domek do banku.\n'
            print(menu)
            choice = input('Twój wybór:')
            if choice in ('1', '2', '3', 'q'):
                return choice
            else:
                continue

    def player_can_pay_message(self):
        '''
        Message when player collest enough money to pay debt.
        '''
        self.clear()
        self.head()
        text = 'Możesz już zapłacić.\n'
        print(text)
        self.freeze()

    def creditor_take_over_fortune(self, creditor, bancrupt):
        '''
        Message when other player takes over fortune of bankrupt.
        '''
        self.clear()
        text = f'{creditor.name()} przejmuje majątek gracza {bancrupt.name()}.'
        print(text)
        self.new_line()
        self.freeze()

    def bank_take_over_fortune(self, bancrupt):
        '''
        Message when bank takes over fortune of bankrupt.
        Informs about auction of fields.
        '''
        self.clear()
        text = f'Bank przejmuje majątek gracza {bancrupt.name()}.\n'\
            'Odbędzie się licytacja jego majątku.\n '
        print(text)
        self.freeze()

    def chance_drawn_message(self, id):
        '''
        Prints description of chance card for a given id.
        '''
        self.clear()
        self.head()
        text = CHANCES[id]
        print(text)
        self.freeze()

    def scratch_card(self, dices, amount):
        '''
        Message when player darws 'Scratch card'
        Shows dices result and win amount
        '''
        self.clear()
        self.head()
        text = f'Wyrzuciłeś {dices[0]}, {dices[1]} i wygrywasz {amount}!\n'
        print(text)
        self.freeze()

class WrongIdError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__('IDs must be between min and max ID')


class NotOwnedError(Exception):
    def __init__(self, *args: object) -> None:
        message = 'Cannot sell or mortage field that not belongs to him'
        super().__init__(message)


class AlreadyMortagedError(Exception):
    def __init__(self, *args: object) -> None:
        message = 'Cannot mortage or sell field that is already mortaged.'
        super().__init__(message)


class NotMortagedError(Exception):
    def __init__(self, *args: object) -> None:
        message = 'Player cannot end mortage of field that is not mortaged'
        super().__init__(message)


class NotEnoughMoneyError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Player han not enough money.')


class PropertyLevelError(Exception):
    pass


class NoMoneyError(Exception):
    pass


class JailRoundsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Value cannot be negative or higher than max.')


class TooShortGameError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Number of rounds cannot be smaller than min number')


class PlayersNumberError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Players number must be in range <min, max>')


class AlreadyOwnedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Field is already owned by player')


class BuiltUpError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Field is built up.')


class NotOwnedDistrictError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Player is not full district owner.')


class UnequalBuildingError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Properties have to be upgraded equally.')


class NotAllBancruptError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Properties have to be upgraded equally.')


class AlreadyArrestedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Cannot arrest player who is already arrested.')


class NotArrestedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Cannot relase player who is not arrested.')


class RepeatedIdError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Id is repated.')

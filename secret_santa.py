from __future__ import annotations
from typing import Optional
import random


class SecretSanta:
    """A secret santa exchange.

    === Attributes ===
    name: The name of this exchange
    budget: The budget for the secret santa exchange.
    _people: The people involved in the exchange, the key represents the
        person's unique ID, the value represents their name.
    _wishlist: The wishlist of the secret santa, each key represents the
        people involved, and the value is a list of the wished items.
    _pointer: The pointer points to whom each person involved must get a gift
        for. The key represents the person who must get the gift, the value
        represents the person to get the gift to.
    """
    name: str
    budget: float
    _people: dict[int, str]
    _wishlist: dict[int, list[str]]
    _pointer: dict[int, Optional[int]]

    def __init__(self, name: str, budget: float) -> None:
        """Initialize a secret santa object.

        >>> secret_santa = SecretSanta('Christmas 2023', 20.0)
        >>> secret_santa.budget
        20.0
        >>> secret_santa._wishlist
        {}
        >>> secret_santa._pointer
        {}
        """
        self.name = name
        self.budget = float(budget)
        self._people = {}
        self._wishlist = {}
        self._pointer = {}

    def add_user(self, user: str, user_id: int) -> bool:
        """Return whether a <user> has been added to the exchange. If the user
        is already in the exchange, return false.

        >>> secret_santa = SecretSanta('Christmas 2023', 20.0)
        >>> secret_santa.add_user('JP', 1)
        True
        """
        if user not in self._wishlist:
            self._people[user_id] = user
            self._wishlist[user_id] = []
            self._pointer[user_id] = None
            return True
        return False

    def add_wish(self, user_id: int, wish: str) -> None:
        """Add a <wish> this a person with <user_id>.

        >>> secret_santa = SecretSanta('Christmas 2023', 20.0)
        >>> secret_santa.add_user('JP', 20)
        True
        >>> secret_santa.add_wish(20, 'Iphone 11 blue case')
        """
        if user_id in self._people:
            self._wishlist[user_id].append(wish)

    def remove_user(self, user_id: int) -> bool:
        """Remove a user within the exchange. Once the user is removed,
        randomize the pointer if it has already been initialized.

        >>> secret_santa = SecretSanta('Christmas 2023', 20.0)
        >>> secret_santa.add_user('JP', 20)
        True
        >>> secret_santa.add_user('Nick', 24)
        True
        >>> secret_santa.remove_user(24)
        True
        >>> 24 in secret_santa._people
        False
        """
        if user_id in self._people:
            self._people.pop(user_id)
            if self._pointer != {}:
                self.randomize_pointer()
            return True
        return False

    def randomize_pointer(self) -> bool:
        """Return if the pointer has been succesfully randomized. Each key will
        point to another key instead of None.

        >>> secret_santa = SecretSanta('Christmas 2023', 20.0)
        >>> secret_santa.add_user('JP', 20)
        True
        >>> secret_santa.add_user('Nick', 24)
        True
        >>> secret_santa.add_user('Tara', 3)
        True
        >>> secret_santa._pointer == {
        ... 20: None, 24: None, 3: None
        ... }
        True
        >>> secret_santa.randomize_pointer()
        True
        >>> secret_santa._pointer[20] is not None
        True
        """
        people_ids = list(self._people.keys())

        for person in self._pointer:
            rand = random.choice(people_ids)

            while rand == person:
                rand = random.choice(people_ids)

            people_ids.remove(rand)
            self._pointer[person] = rand
        return True

    def set_pointer(self, pointer: dict) -> bool:
        """Return if the current pointer was succesfully set to a new value.
        It is succesfully set if pointer is a valid pointer.

        If the pointer is already another dictionary, overwrite it with the
        new pointer.

        >>> secret_santa = SecretSanta('2023 Christmas Exchange', 20.0)
        >>> secret_santa.add_user('JP', 20)
        True
        >>> secret_santa.add_user('Nick', 24)
        True
        >>> secret_santa._pointer == {20: None, 24: None}
        True
        >>> new_pointer = {20: 24, 24: 20}
        >>> secret_santa.set_pointer(new_pointer)
        True
        >>> secret_santa._pointer == {20: 24, 24: 20}
        True
        """
        if self._is_valid_pointer(pointer):
            self._pointer = pointer
            return True
        return False

    def _is_valid_pointer(self, new_pointer: dict) -> bool:
        """Return if <new_pointer> is a valid pointer.

        A pointer is valid if every key has a value corresponding to another
        key in the dictionary. Every value must be a key. If every value is
        None that is valid, if only some are None, that is invalid.
        """
        keys = set(new_pointer.keys())
        values = set(new_pointer.values())

        if keys != values or keys != set(self._pointer.keys()):
            return False

        for key, value in new_pointer.items():
            if key == value or (value not in keys and value is not None):
                return False
        return True

    def to_dict(self) -> dict:
        """Return the representation of the secret_santa object as a dictionary.

        >>> secret_santa = SecretSanta('2023 Christmas Exchange', 20.0)
        >>> secret_santa.add_user('JP', 20)
        True
        >>> secret_santa.add_user('Nick', 24)
        True
        >>> secret_santa.add_user('Tara', 3)
        True
        >>> secret_santa.add_wish(20, 'Iphone 11 blue case')
        >>> secret_santa.add_wish(20, 'Plato: Symposium')
        >>> secret_santa.to_dict() == {
        ... "name": "2023 Christmas Exchange",
        ... "budget": 20.0,
        ... "people": {"20": "JP", "24": "Nick", "3": "Tara"},
        ... "wishlist": {
        ... "20": ["Iphone 11 blue case", "Plato: Symposium"],
        ... "24": [],
        ... "3": []},
        ... "pointer": {"20": None, "24": None, "3": None}
        ... }
        True
        """
        dictionary = dict()

        dictionary["name"] = self.name
        dictionary["budget"] = self.budget

        people_dictionary = {}
        wishlist_dictionary = {}
        pointer_dictionary = {}

        for person in self._people:
            people_dictionary[str(person)] = self._people[person]
            wishlist_dictionary[str(person)] = self._wishlist[person]
            pointer_dictionary[str(person)] = self._pointer[person]

        dictionary["people"] = people_dictionary
        dictionary["wishlist"] = wishlist_dictionary
        dictionary["pointer"] = pointer_dictionary

        return dictionary

    def from_dict(self, secret_santa: dict) -> SecretSanta:
        pass

    def __str__(self) -> str:
        """Returns a string representation of the secret santa object.

        >>> secret_santa = SecretSanta('2023 Christmas Exchange', 20.0)
        >>> secret_santa.add_user('JP', 20)
        True
        >>> secret_santa.add_user('Nick', 24)
        True
        >>> secret_santa.add_user('Tara', 3)
        True
        >>> secret_santa.add_wish(20, 'Iphone 11 blue case')
        >>> secret_santa.add_wish(20, 'Plato: Symposium')
        >>> print(secret_santa)
        2023 Christmas Exchange:
        - JP: ['Iphone 11 blue case', 'Plato: Symposium']
        - Nick: []
        - Tara: []
        """
        total = self.name + ':\n'

        for person in self._people:
            total += '- ' + self._people[person] + ': '

            total += str(self._wishlist[person])

            total += '\n'

        return total[:-1]


if __name__ == '__main__':
    secret_2023 = SecretSanta('2023 Christmas Exchange', 20.0)

    secret_2023.add_user('JP', 20)
    secret_2023.add_user('Nick', 24)
    secret_2023.add_user('Tara', 19)
    secret_2023.add_user('Ana', 23)
    secret_2023.add_user('Isi', 22)
    secret_2023.add_user('Tanisha', 4)

    secret_2023.add_wish(20, 'Iphone 11 blue case')
    secret_2023.add_wish(24, 'Gold earrings')
    secret_2023.add_wish(19, 'Love book')

    secret_2023.randomize_pointer()

    print(secret_2023)

    print(secret_2023._pointer)

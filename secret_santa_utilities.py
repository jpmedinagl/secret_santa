from secret_santa import SecretSanta
import json


def create_exchange(name: str, budget: float) -> SecretSanta:
    """Create a Secret Santa exchange with <name> and <budget>.

    >>> secret_2023 = create_exchange('Christmas 2023', 20.0)
    >>> isinstance(secret_2023, SecretSanta)
    True
    """
    filename = 'exchange_' + name.replace(" ", "_") + '.json'
    secret_santa = SecretSanta(name, budget)
    ss_dict = secret_santa.to_dict()
    with open(filename, 'w') as file:
        json.dump(ss_dict, file, indent=4)
    return secret_santa


def load_exchange(name: str) -> SecretSanta:
    """Load a Secret Santa exchange with <name>.

    >>> secret_2023 = load_exchange('Christmas 2023')
    >>> isinstance(secret_2023, SecretSanta)
    True
    """
    filename = 'exchange_' + name.replace(" ", "_") + '.json'
    with open(filename, 'r') as file:
        secret_santa_dict = json.load(file)

    exchange_name = secret_santa_dict["name"]
    exchange_budget = secret_santa_dict["budget"]
    secret_santa = SecretSanta(exchange_name, exchange_budget)
    new_pointer = {}

    for person in secret_santa_dict["people"]:
        name = secret_santa_dict["people"][person]
        secret_santa.add_user(name, int(person))
        new_pointer[int(person)] = secret_santa_dict["pointer"][person]

        for wish in secret_santa_dict["wishlist"][person]:
            secret_santa.add_wish(int(person), wish)

    secret_santa.set_pointer(new_pointer)

    return secret_santa


def save_exchange(secret_santa: SecretSanta) -> None:
    """Save the secret_santa exchange into a json file.
    """
    name = secret_santa.name
    filename = 'exchange_' + name.replace(" ", "_") + '.json'
    ss_dict = secret_santa.to_dict()
    with open(filename, 'w') as file:
        json.dump(ss_dict, file, indent=4)


if __name__ == '__main__':
    secret_santa_2023 = create_exchange('Christmas 2023', 50.0)

    secret_santa_2023.add_user('JP', 20)
    secret_santa_2023.add_user('Nick', 24)
    secret_santa_2023.add_wish(20, 'Plato: Symposium')
    secret_santa_2023.add_wish(24, 'Star Wars Lego Set')
    secret_santa_2023.randomize_pointer()

    save_exchange(secret_santa_2023)

    secret_santa_2023 = load_exchange('Christmas 2023')
    print(secret_santa_2023)

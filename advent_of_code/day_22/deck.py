"""deck shuffle logic"""
from typing import TextIO, List


def get_instructions(file_input: TextIO) -> List[str]:
    """get list of instructions

    Arguments:
        file_input {TextIO} -- text stream

    Returns:
        List[str] -- list of instructions
    """
    instructions = []
    for instruction in file_input:
        instruction = instruction.strip()
        instructions.append(instruction)

    return instructions


def shuffle(instructions: List[str], deck: List[int]) -> List[int]:
    """shuffles and returns new deck

    Arguments:
        instructions {List[str]} -- shuffling instructions
        deck {List[int]} -- original deck

    Raises:
        ValueError: unknown instruction given

    Returns:
        List[int] -- shuffled deck
    """
    deck_length = len(deck)

    for instruction in instructions:
        if instruction == "deal into new stack":
            deck = deck[::-1]
        elif instruction.startswith("cut "):
            _, cut_value = instruction.split(" ")
            cut_value = int(cut_value)

            deck = deck[cut_value:] + deck[:cut_value]
        elif instruction.startswith("deal with increment "):
            increment = instruction.split(" ")[-1]
            increment = int(increment)

            new_deck = [None] * len(deck)
            count = 0
            for card in deck:
                new_deck[count % deck_length] = card
                count += increment

            deck = new_deck
        else:
            raise ValueError("Unknown instruction!")

    return deck


def find_iter(instructions: List[str], deck_size: int, shuffle_count: int, index: int) -> int:
    """find what card is at a given index, given large deck size and shuffle counts this needs to be
    computed

    Arguments:
        instructions {List[str]} -- shuffle instructions
        deck_size {int} -- deck size
        shuffle_count {int} -- how many times the deck will be shuffled
        index {int} -- index of the card we want to find

    Returns:
        int -- value of card at given index
    """
    offset = 0
    total_increment = 1

    for instruction in instructions:
        if instruction == "deal into new stack":
            total_increment *= -1
            offset += total_increment
        elif instruction.startswith("cut "):
            _, cut_value = instruction.split(" ")
            cut_value = int(cut_value)

            offset += total_increment * cut_value
        elif instruction.startswith("deal with increment "):
            increment = instruction.split(" ")[-1]
            increment = int(increment)

            total_increment *= pow(increment, deck_size-2, deck_size)
            total_increment %= deck_size

    # apply shuffles
    shuffle_increment = pow(total_increment, shuffle_count, deck_size)
    inverse = pow((1 - total_increment) % deck_size, deck_size-2, deck_size)
    shuffle_offset = offset * (1 - shuffle_increment) * inverse
    shuffle_offset %= deck_size

    return (shuffle_offset + index * shuffle_increment) % deck_size

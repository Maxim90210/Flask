from concurrent.futures import ProcessPoolExecutor
import itertools


def is_happy_ticket(ticket):
    str_ticket = str(ticket).zfill(ticket_length)
    half_length = ticket_length // 2
    first_half = str_ticket[:half_length]
    second_half = str_ticket[half_length:]

    sum_first_half = sum(int(digit) for digit in first_half)
    sum_second_half = sum(int(digit) for digit in second_half)

    return sum_first_half == sum_second_half


def count_happy_tickets(start, end):
    count = 0
    for ticket in range(start, end):
        if is_happy_ticket(ticket):
            count += 1
    return count


def split_ranges(total_tickets, num_parts):
    chunk_size = total_tickets // num_parts
    ranges = []
    for i in range(num_parts):
        start = i * chunk_size
        if i == num_parts - 1:
            end = total_tickets
        else:
            end = (i + 1) * chunk_size
        ranges.append((start, end))
    return ranges


def main(ticket_length, num_processes=4):
    total_tickets = 10 ** ticket_length
    ranges = split_ranges(total_tickets, num_processes)

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(count_happy_tickets, start, end) for start, end in ranges]
        results = [future.result() for future in futures]

    total_happy_tickets = sum(results)
    return total_happy_tickets


if __name__ == "__main__":
    ticket_length = 10
    num_happy_tickets = main(ticket_length)
    print(f"Кількість щасливих білетів з {ticket_length} цифрами: {num_happy_tickets}")

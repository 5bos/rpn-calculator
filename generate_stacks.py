import random
from sqlmodel import Session
from db.stack import Stack
from main import engine


def generate_random_lists():
    """Generates a random number of lists that contain randmo number of random items"""
    num_lists = random.randint(5, 10)

    for _ in range(num_lists):
        num_elements = random.randint(3, 10)
        rand_list = [random.randint(-99, 99) for _ in range(num_elements)]
        print(f"Generating stack with items {rand_list}")
        yield rand_list


# Example usage
if __name__ == "__main__":
    with Session(engine) as session:
        for random_list in generate_random_lists():
            stack = Stack(items=random_list)
            session.add(stack)
        session.commit()

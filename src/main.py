import repository
from dtclasses import Purchase, Income
from datetime import datetime


def main():
    global repo
    repo = repository.Repository("test")
    test_purchase()


def test_purchase():
    purchase = Purchase(name="meow", cost=10, date=datetime.now())
    print(purchase)
    repo.add_purchase(purchase)
    repo.delete_purchase(purchase)


if __name__ == "__main__":
    main()

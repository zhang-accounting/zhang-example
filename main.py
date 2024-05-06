import os
import fire
import arrow
import random
import calendar
from random import randint
from pprint import pprint
import uuid
import shutil

COMMODITIES = ["CNY", "USD"]
COMMODITIES_SYMBOL = ["¥", "$"]

COMPANY = 'GrandLordCompany'

INCOMES = [f"{COMPANY}:Salary", "Remuneration", "CitiBank:Interest", "Publisher:DogeRandomHouse",
           "Publisher:TheZhangBookGroup", "Publisher:Scgolastic"]
ASSETS = ["Paypal", "WeChat", "CitiBank:9999"]
LIABILITIES = ["CreditCard:Apple", "CreditCard:CitiBank:3423"]
EXPENSES = ["PersonalDiet:Lunch", "PersonalDiet:Dinner", "Clothing", "Medical", "Sport", "Transportaion",
            f"{COMPANY}:Tax", "RemunerationTax"]
EQUITIES = ["OpenBlancing"]

EXPENSE_TYPE = [
    [  # lunch, dinner
        lambda: randint(0, 2),
        ["Github Restaurant", "KFC", "Mcdonald", "隆江猪脚饭"],
        ["Eating Lunch", "Eating Dinner", "Fried Chicken"],
        [
            [
                [*list(map(lambda item: f"Liabilities:{item}", LIABILITIES)),
                 *list(map(lambda item: f"Assets:{item}", ASSETS))],
                lambda: f"{randint(10, 30) * -1} {COMMODITIES[0]}"
            ],
            [
                list(map(lambda item: f"Expenses:{item}", [EXPENSES[0], EXPENSES[1]])),
                lambda: ""
            ]
        ]
    ],
    [  # cloth
        lambda: random.choice([0, 0, 0, 1]),
        ["H & M", "UNIQLO", "Nike", "Adidas", "Vans"],
        ["T-shirt", "shoes", "jeans"],
        [
            [
                list(map(lambda item: f"Assets:{item}", ASSETS)),
                lambda: f"{randint(10, 30) * -1} {COMMODITIES[0]}"
            ],
            [
                ["Expenses:Clothing"],
                lambda: ""
            ],
        ]
    ],
    [  # remuneration
        lambda: random.choice([0, 1]),
        ["Doge Random House", "The Zhang Book Group", "Scgolastic"],
        ["Remuneration of <How to learn Zhang>", "Annual Remuneration",
         "Remuneration of <Good Good study, Day Day Up>"],
        [
            [
                list(map(lambda item: f"Income:{item}",
                         ["Publisher:DogeRandomHouse", "Publisher:TheZhangBookGroup", "Publisher:Scgolastic"])),
                lambda: f"{randint(10, 50) * -1} {COMMODITIES[0]}"
            ],
            [
                list(map(lambda item: f"Assets:{item}", ASSETS)),
                lambda: ""
            ],
            [
                ["Expenses:RemunerationTax"],
                lambda: f"{randint(2, 5)} {COMMODITIES[0]}"
            ],
        ]
    ]
]
BUDGETS = [
    ["food", "Take out Food", "Daily Necessary", 500],
    ["shopping", "Shopping", "Daily Necessary", 300],
    ["habit", "Habit", "Spiritual Needs", 300]
]

BUDGETS_MAPPING ={
    "PersonalDiet:Lunch": "food",
    "PersonalDiet:Dinner": "food",
    "Clothing": "shopping",
    "Sport": "habit"
}

IMAGES = [
    "1.jpeg", "2.jpg"
]


def random_in_list(l):
    return random.choice(l)


class Cli:

    def run(self):
        content = []
        beginning = arrow.Arrow(1970, 1, 1)
        beginning_format = beginning.format("YYYY-MM-DD")
        # init options
        content.append("option \"title\" \"My Accounting\"")
        content.append(f"option \"operating_currency\" \"{COMMODITIES[0]}\"")

        content.append("\n")
        # init currency
        for idx, commodity in enumerate(COMMODITIES):
            content.append(f"{beginning_format} commodity {commodity}")
            content.append("  precision: 2")
            content.append(f"  prefix: \"{COMMODITIES_SYMBOL[idx]}\"")

        content.append("\n")

        # open income account
        comma_commodities = ", ".join(COMMODITIES)
        for income in INCOMES:
            content.append(f"{beginning_format} open Income:{income} {comma_commodities}")

        content.append("\n")

        # open assets account
        for account in ASSETS:
            content.append(f"{beginning_format} open Assets:{account} {comma_commodities}")

        # open liability account
        content.append("\n")
        for account in LIABILITIES:
            content.append(f"{beginning_format} open Liabilities:{account} {comma_commodities}")

        # open expense account
        content.append("\n")
        for account in EXPENSES:
            content.append(f"{beginning_format} open Expenses:{account} {comma_commodities}")
            if account in BUDGETS_MAPPING:
                content.append(f"  budget: {BUDGETS_MAPPING[account]}")

        # open expense account
        content.append("\n")
        for account in EQUITIES:
            content.append(f"{beginning_format} open Equity:{account} {comma_commodities}")

        now = arrow.now()


        # balance all assets account:
        content.append("\n")
        target_month = now.shift(months=-3)
        beginning_of_zhang = arrow.Arrow(target_month.year, target_month.month, 1, 1, 1, 1).shift(days=-1).format(
            "YYYY-MM-DD HH:mm:ss")

        for account in ASSETS:
            amount = random.randint(130000, 170000)
            content.append(
                f"{beginning_of_zhang} balance Assets:{account} {amount} {COMMODITIES[0]} with pad Equity:{EQUITIES[0]}")

        # init budget

        for budget in BUDGETS:
            content.append(f"{beginning_of_zhang} budget {budget[0]} CNY")
            content.append(f"  alias: \"{budget[1]}\"")
            content.append(f"  category: \"{budget[2]}\"")
            content.append(f"\n")

        # loop month
        content.append("\n")
        for month_offset in [-3, -2, -1, 0]:
            content.append("\n")
            target_month = now.shift(months=month_offset)
            beginning_of_target_month = arrow.Arrow(target_month.year, target_month.month, 1, 1, 1, 1).format(
                "YYYY-MM-DD")
            # add budget amount
            for budget in BUDGETS:
                content.append(f"{beginning_of_target_month}  budget-add {budget[0]} {budget[3]} CNY")

            # loop month: salary at month first day
            salary_income = random.randint(2000, 3000)
            salary_tax = random.randint(100, 400)
            salary_asset = salary_income - salary_tax
            implicit_tax = f"{salary_tax} {COMMODITIES[0]}" if random.choice([True, False]) else ""
            time_of_salary = arrow.Arrow(target_month.year, target_month.month, 1, 8, 0, 0).format(
                "YYYY-MM-DD HH:mm:ss")
            content.append(f"{time_of_salary} \"{COMPANY}\" \"Salary\"")
            content.append(f"  Income:{COMPANY}:Salary {-1 * salary_income} {COMMODITIES[0]}")
            content.append(f"  Assets:CitiBank:9999 {salary_asset} {COMMODITIES[0]}")
            content.append(f"  Expenses:{COMPANY}:Tax {implicit_tax}")

            content.append("\n")

            # loop month: expense to buy something, lunch, dinner
            for day in range(1, calendar.monthrange(target_month.year, target_month.month)[1]):
                if target_month.month == now.month and day > now.day:
                    continue
                for [loop_executor, payee, narration, postings] in EXPENSE_TYPE:
                    for _loop_time in range(0, loop_executor()):
                        target_time = arrow.Arrow(target_month.year, target_month.month, day, random.randint(0, 23),
                                                  random.randint(0, 59), random.randint(0, 59)).format(
                            "YYYY-MM-DD HH:mm:ss")
                        content.append(f"{target_time} \"{random_in_list(payee)}\" \"{random_in_list(narration)}\"")
                        for [posting, amount_executor] in postings:
                            content.append(f"  {random_in_list(posting)} {amount_executor()}")

                        if random.randint(0, 59) < 10:
                            # add image
                            image_uuid = uuid.uuid4()
                            target_image = random.choice(IMAGES)
                            os.makedirs(f"data/attachments/{image_uuid}")
                            shutil.copy(f"images/{target_image}", f"data/attachments/{image_uuid}/{target_image}")
                            content.append(f"  document: \"attachments/{image_uuid}/{target_image}\"")

                        content.append("\n")

        # loop month: income for remuneration, interest
        # balance at end of month
        pass
        print("\n".join(content))


if __name__ == '__main__':
    fire.Fire(Cli)

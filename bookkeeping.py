import enum
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

class PaymentMethod(enum.Enum):
    cash = 1,
    credit_card = 2

expense_categories = {
    "food" : [
        "snacks",
        "lunch",
        "dinner",
        "drinks",
        "breakfast"
    ],
    "transportation" : [
        "ticket"
    ],
    "lifestyle" : [
        "easycard",  # 悠遊卡
        "haircut",
        "dn",  # daily neccesities
        "shopping",
        "online",  # online shopping
        "fee",
        "post",
        "taxi"
    ],
    "loans" : [
        "lend",
        "repayment"
    ],
    "healthcare" : [
        "medical bill",
        "medicine"
    ],
    "others" : [
        "incidental expenses",
        "fine"
    ]
}

income_categories = {
    "job" : [
        "tutor"
    ],
    "loans" : [
        "repayment"
    ],
    "others" : []
}


def plot_piechart(source_dict, figure_title):

    labels = list(source_dict.keys())
    values = np.array(list(source_dict.values()))

    fig = plt.figure(figsize=[10, 10])
    ax = fig.add_subplot(111)
    cmap = plt.cm.prism
    # colors = cmap(np.linspace(0., 1., len(category_values)))

    pie_wedge_collection = ax.pie(
        values,
        # colors=colors,
        explode=(values == max(values))*0.1,
        labels=labels,
        labeldistance=1.05,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90
    )

    for pie_wedge in pie_wedge_collection[0]:
        pie_wedge.set_edgecolor('white')

    # for text in pie_wedge_collection[1]:
    #     text.set_color('grey')
    # for autotext in pie_wedge_collection[2]:
    #     autotext.set_color('grey')

    ax.set_title(figure_title)
    ax.axis('equal')

YEAR_DATE = "2021.05"

with open("./Archived/記帳 " + YEAR_DATE + ".txt", "r") as bknotes:
    # global containers &
    #  analyzer variables
    expense_by_category = defaultdict(int)
    unidentified_titles = set()
    expense_by_title = defaultdict(int)
    date_expenses = defaultdict(int)  # the total expense of each date, format: { date : expense_of_this_date }
    paid_for_others = defaultdict(int)  # number of people paid for, format: { nb_of_people : times_paid_for_this_amount_of_people }

    date_of_month = 0

    monthly_total_expense = 0
    monthly_total_income = 0

    # cash_total_expense = 0
    # credit_card_total_expense = 0  # ! : credit card (includes apple pay and line pay)

    # cash_total_income = 0

    # times_paid_in_cash = 0
    # times_paid_with_credit_card = 0


    for bkline in bknotes:  # read line in file

        bkline = bkline.strip()   # strip newline and leading, trailing whitespaces
        if bkline == "":
            continue
        entry = bkline.split()

        if len(entry) == 1:  # date
            date_of_month = entry[0].split("/")[1]
        else:
            # number of people paid for (not including self)
            paid_for_nb_of_people = 0
            for idx, el in enumerate(entry):
                if "*" in el:
                    paid_for_nb_of_people = len(entry[idx])
                    del entry[idx]  # remove asterisks from list
                    paid_for_others[paid_for_nb_of_people] += 1

            # method of payment
            payment_method = PaymentMethod.cash
            if entry[0] == "!" or entry[0] == "！":  # paid with credit card
                payment_method = PaymentMethod.credit_card
                del entry[0]

                
            # calculate expense/income
            entry_sum = 0
            entry_title = ""
            entry_sum = int(entry[0])
            entry_title = " ".join(entry[1:])


            if entry_sum < 0:  # expense
                expense_sum = abs(entry_sum)
                monthly_total_expense += expense_sum
                expense_by_title[entry_title] += expense_sum
                # find in corresponding category
                found_category = False
                for category, items in expense_categories.items():
                    if entry_title in items:
                        found_category = True
                        expense_by_category[category] += expense_sum
                
                if not found_category:
                    unidentified_titles.add(entry_title)
                    expense_by_category["others"] += expense_sum


            else:  # income
                monthly_total_income += entry_sum 

            # if payment_method == PaymentMethod.cash:
            #     if entry_sum < 0:
            #         cash_total_expense += abs(entry_sum)
            #         times_paid_in_cash += 1
            #     else:
            #         cash_total_income += entry_sum
            
            # elif payment_method == PaymentMethod.credit_card:  # paid with credit card
            #     if entry_sum < 0:
            #         credit_card_total_expense += abs(entry_sum)
            #         times_paid_with_credit_card += 1
            #     else:  # seldom deal with credit card income, not implemented
            #         pass

    # generate report
    print("total expense: " + str(monthly_total_expense))
    print("total income: " + str(monthly_total_income))
    print("unidentified titles: " + str(unidentified_titles))

    with open("./bookkeep_history.txt", "a+") as bkhistory:
        bkhistory.write(YEAR_DATE + "\n")
        bkhistory.write("   total expense: " + str(monthly_total_expense) + "\n")
        bkhistory.write("   total income: " + str(monthly_total_income) + "\n")
        bkhistory.write("\n")

    # plot_piechart(expense_by_category, "Expense By Category")
    # plot_piechart(expense_by_title, "Expense By Title")

    # plt.tight_layout()
    # plt.show()
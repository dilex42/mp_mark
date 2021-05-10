import math

SUB_COST = 7
SUB_USER_PCT = 0.03
LIFE_EXP = 10
ORGANIC_COEF = 0.1
CPI = 1.1
APPSTORE_PCT = 0.3
REFUND_PCT = 0.05

GOAL = 10000

# subscription income after app store commision
actual_income_sub = SUB_COST * (1 - APPSTORE_PCT)
# on average from one subscriber we get
actual_income_sub *= LIFE_EXP
# we get SUB_USER_PCT subscribers but REFUND_PCT of them refund so
actual_subs_pct = SUB_USER_PCT * (1 - REFUND_PCT)
# from one install we get
income_per_user = actual_income_sub * actual_subs_pct
# we pay only for non-organic installs
cost_per_user = CPI * (1 - ORGANIC_COEF)
# our profit per user is
profit_per_user = income_per_user - cost_per_user
# to rich our goal
installs_needed = math.ceil(GOAL / profit_per_user)
# we spend money only on attracting users. I don't consider AppStore commission as spending money. Also some one-time fees for placing app on AppStore may apply.
money_spent = installs_needed * cost_per_user
print(
    f"We need {installs_needed} installs to reach our goal of ${GOAL} net profit. We gonna spend ${money_spent} to achive this."
)

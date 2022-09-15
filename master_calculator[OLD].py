import numpy as np
import scipy.optimize


"""
PART A
ALL INPUT DATA FROM THE ONLINE USER
"""


"""
A.1
FILL IN ALREADY PLACED BETS BELOW.
"""

"""
QUALIFYING BETS, BONUS OFFERS/MATCHED DEPOSITS BETS TO COMPLETE WAGERING REQUIREMENTS.
"""
wagerB_1 = 0
wagerB_X = 0
wagerB_2 = 0

oddsB_1 = 0.00
oddsB_X = 0.00
oddsB_2 = 0.00

"""
RISK-FREE BETS
"""
wagerR_1 = 0
wagerR_X = 0
wagerR_2 = 0

oddsR_1 = 0.00
oddsR_X = 0.00
oddsR_2 = 0.00

"""
FILL IN WHETHER RETURNED STAKE ON YOUR RISK-FREE BETS ARE IN FREEBET CREDITS OR CASH.
IF IN FREEBET CREDITS, SET stake_returned_as_freebet TO "True".
IF IN CASH, SET stake_returned_as_freebet TO "False".
"""
stake_returned_as_freebet = False

"""
FREEBETS
"""
wagerF_1 = 0
wagerF_X = 0
wagerF_2 = 0

oddsF_1 = 0.00
oddsF_X = 0.00
oddsF_2 = 0.00


"""
A.2
ODDS - FILL IN BEST AVAILABLE MARKET ODDS FOR EACH OUTCOME AT THE TIME THE POSITION IS ABOUT TO BE NEUTRALIZED.
"""
odds_1 = 0.00
odds_X = 0.00
odds_2 = 0.00


"""
ALL THE NECESSARY USER INPUT DATA HAS NOW BEEN COLLECTED -> SCRIPT READY TO BE EXECUTED.
"""


"""
PART B
CODE AND DOCUMENTATION
"""


"""
B.1
SETS UP NECESSARY PARAMETERS DEPENDING ON THE TYPE OF RISK-FREE BET OFFERED.
"""
if not stake_returned_as_freebet:
    share_returnedR_1 = 1
    share_returnedR_X = 1
    share_returnedR_2 = 1
else:
    share_returnedR_1 = 0.7
    share_returnedR_X = 0.7
    share_returnedR_2 = 0.7


"""
B.2
DEFINES PAYOFF FUNCTIONS.
NOTE THAT ALL FUNCTIONS ACT ON THE GLOBAL VARIABLES DEFINED IN PART A.
"""


def payoff_outcome_1(stakes_vector: list) -> float:
    """
    Computes the payoff in the case where outcome 1 occurs

    :param: list stakes_vector: A List containing the stakes on the three outcomes. E.g. [100, 240, 652] if 100 $
            was wagered on the first outcome, 240 $ on the second one and so on...

    :return: payoff in dollars
    :rtype: float
    """
    wager_1 = stakes_vector[0]
    wager_X = stakes_vector[1]
    wager_2 = stakes_vector[2]
    payoff = wagerB_1 * (oddsB_1 - 1) - wagerB_X - wagerB_2 + wagerR_1 * (oddsR_1 - 1) - (1 - share_returnedR_X) * wagerR_X - \
        (1 - share_returnedR_2) * wagerR_2 + wagerF_1 * (oddsF_1 - 1) + \
        wager_1 * (odds_1 - 1) - wager_X - wager_2
    return payoff


def payoff_outcome_X(stakes_vector: list) -> float:
    """
    Computes the payoff in the case where outcome X occurs

    :param: list stakes_vector: A List containing the stakes on the three outcomes. E.g. [100, 240, 652] if 100 $
            was wagered on the first outcome, 240 $ on the second one and so on...

    :return: payoff in dollars
    :rtype: float
    """
    wager_1 = stakes_vector[0]
    wager_X = stakes_vector[1]
    wager_2 = stakes_vector[2]
    payoff = wagerB_X * (oddsB_X - 1) - wagerB_1 - wagerB_2 + wagerR_X * (oddsR_X - 1) - (1 - share_returnedR_1) * wagerR_1 - \
        (1 - share_returnedR_2) * wagerR_2 + wagerF_X * (oddsF_X - 1) + \
        wager_X * (odds_X - 1) - wager_1 - wager_2
    return payoff


def payoff_outcome_2(stakes_vector: list) -> float:
    """
    Computes the payoff in the case where outcome 2 occurs

    :param: list stakes_vector: A List containing the stakes on the three outcomes. E.g. [100, 240, 652] if 100 $
            was wagered on the first outcome, 240 $ on the second one and so on...

    :return: payoff in dollars
    :rtype: float
    """
    wager_1 = stakes_vector[0]
    wager_X = stakes_vector[1]
    wager_2 = stakes_vector[2]
    payoff = wagerB_2 * (oddsB_2 - 1) - wagerB_1 - wagerB_X + wagerR_2 * (oddsR_2 - 1) - (1 - share_returnedR_1) * wagerR_1 - \
        (1 - share_returnedR_X) * wagerR_X + wagerF_2 * (oddsF_2 - 1) + \
        wager_2 * (odds_2 - 1) - wager_1 - wager_X
    return payoff


"""
B.3
THE FOLLOWING LINES OF CODE CATCHES OBVIOUS INPUT ERRORS.
WILL BE INTEGRATED WITH THE INPUT LATER ON.
"""
if wagerB_1 < 0 or wagerB_X < 0 or wagerB_2 < 0 or wagerR_1 < 0 or wagerR_X < 0 or wagerR_2 < 0 or wagerF_1 < 0 or wagerF_X < 0 or wagerF_2 < 0:
    raise ValueError(
        "The size of all wagers must be greater than or equal to zero")


"""
B.4
OUR AIM IS TO FIND THE STAKES VECTOR WHICH MAXIMIZES OUR NET PROFIT GIVEN THE FOLLOWING CONSTRAINTS:
wager_1 ≥ 0, wager_X ≥ 0, wager_2 ≥ 0
payoff_outcome_1 = payoff_outcome_X = payoff_outcome_2 WHICH TRANSLATES INTO THE TWO CONDITIONS:
payoff_outcome_1 - payoff_outcome_X = 0
payoff_outcome_1 - payoff_outcome_2 = 0
"""


"""
B.5
IN CASE THE HOUSE EDGE IS NEGATIVE (E.G. POSSIBLE BY COMBINING ODDS FROM DIFFERENT BETTING SOURCES)
THE ALGORITHM WILL RECOMMEND "INFINITE" WAGERS SINCE ARBITRAGE OPPORTUNITIES (IN PRACTICE NOT EXECUTABLE)
EXIST, HENCE IN THIS CASE A SLIGHT ADJUSTMENT IS NECESSARY FOR THE RESULT TO CONVERGE.
"""


def return_to_player(odds_1: float, odds_X: float, odds_2: float) -> float:
    '''
    Computes how much margin is applied to the game given the three odds

    :param: float odds_1: The odds offered on outcome 1
    :param: float odds_1: The odds offered on outcome X
    :param: float odds_1: The odds offered on outcome 2

    :return: Percentage of wagered money returned to the players in decimal form with 1 being 100 %
    :rtype: float

    '''
    return_to_player = 1 / (1 / odds_1 + 1 / odds_X + 1 / odds_2)
    return return_to_player


"""
B.6
EXECUTION
"""


def prepare_minimization(stakes_vector: list) -> float:
    """
    Prepares for optimization by returning -payoff since the scipy algorithms minimizes
    while our objective is to maximize

    The choice of payoff function is arbitrary since our main constraint forces them
    all to be equal

    :param: list stakes_vector: A List containing the stakes on the three outcomes. E.g. [100, 240, 652] if 100 $
            was wagered on the first outcome, 240 $ on the second one and so on...

    :return: -payoff in dollars
    :rtype: float
    """
    return -payoff_outcome_1(stakes_vector)


"""
B.6.1
SPLITS INTO CASES DEPENDING ON RTP OFFERED BY SPECIFIED ODDS.
UNDER NORMAL CIRCUMSTANCES THE FIRST CASE WILL COME INTO PLAY.
"""
epsilon = 0.001
rtp = return_to_player(odds_1, odds_X, odds_2)

if rtp < 1:
    store_odds_1 = odds_1
    store_odds_X = odds_X
    store_odds_2 = odds_2

elif rtp == 1:
    store_odds_1 = odds_1
    store_odds_X = odds_X
    store_odds_2 = odds_2

    # FOR THE ALGORITHM TO CONVERGE, ODDS ARE ADJUSTED SUCH THAT RTP FALLS BELOW 1
    odds_1 = odds_1 / (1 + epsilon)
    odds_X = odds_X / (1 + epsilon)
    odds_2 = odds_2 / (1 + epsilon)

else:
    store_odds_1 = odds_1
    store_odds_X = odds_X
    store_odds_2 = odds_2

    # FOR THE ALGORITHM TO CONVERGE, ODDS ARE ADJUSTED SUCH THAT RTP FALLS BELOW 1
    odds_1 = odds_1 / (rtp + epsilon)
    odds_X = odds_X / (rtp + epsilon)
    odds_2 = odds_2 / (rtp + epsilon)


"""
B.6.2
SETS UP CONSTRAINTS AND PRODUCES THE RESULT
https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
"""
initial_guess = (0, 0, 0)
bounds = ((0, None), (0, None), (0, None))
constraints = ({'type': 'eq', 'fun': lambda x: payoff_outcome_1(x) - payoff_outcome_X(x)},
               {'type': 'eq', 'fun': lambda x: payoff_outcome_1(x) - payoff_outcome_2(x)})
result = scipy.optimize.minimize(
    fun=prepare_minimization, x0=initial_guess, bounds=bounds, constraints=constraints)


"""
B.6.3
PRESENTS THE RESULT IN A READABLE FORMAT
"""
print('ODDS:')
print(f'1: {store_odds_1:.2f}')
print(f'X: {store_odds_X:.2f}')
print(f'2: {store_odds_2:.2f}')
print('')
print('RECOMMENDED WAGERS: ')
print(f'1: {result.x[0]:.0f} USTT')
print(f'X: {result.x[1]:.0f} USTT')
print(f'2: {result.x[2]:.0f} USTT')
print('')
print(
    f'NET PROFIT REGARDLESS OF OUTCOME WITH RECOMMENDED WAGERS IS {-result.fun:.0f} USTT')


"""
AS ONE NOTICES, WE HAVE CHOSEN TO GO WITH ORDINARY CONSTRAINED OPTIMIZATION TECHNIQUES
ANOTHER WAY TO SOLVE IT WOULD BE BY USE OF LINEAR PROGRAMMING METHODS
MORE ON LINEAR PROGRAMMING CAN BE FOUND ON https://en.wikipedia.org/wiki/Linear_programming OR BY CONSULTING
LP BOOKS, FOR EXAMPLE THE ONES BY DAVID LUENBERGER
"""

#!/usr/bin/env python3

__author__ = "Nick Schneider"
__version__ = "0.1.0"
__license__ = "Apache"

import datetime
import os
from bs4 import BeautifulSoup

from PyMessenger import Email, Messenger
import constants
import helpers


# Environment variables
FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL')  # Comma separate list of emails
PASSWORD = os.getenv('PASSWORD')
SHOULD_SEND_EMAIL = helpers.readBoolEnvVar('SHOULD_SEND_EMAIL', True)
USE_LOCAL = helpers.readBoolEnvVar('USE_LOCAL', False)


def check_angels_score():
    """ 
    Checks the Los Angeles Angels score from the previous day to see if it qualifies for a free Chick Fil A sandwich.
    At any home game, if the Angels score 7 or more runs, you can claim a chicken sandwich.
    """
    if USE_LOCAL:
        soup = BeautifulSoup(
            open('sample_pages/2023_angels_scores.html'), features="html.parser")
    else:
        url = f'https://www.baseball-reference.com/teams/LAA/{helpers.CURRENT_DATETIME.year}-schedule-scores.shtml#all_results'
        soup = helpers.fetch_soup(url)

    # The scores are duplicated on the page (once in the banner and once on the main page)
    # so in order to prevent duplicated work we have to narrow our search down to just the main content (table body or tbody), and not include the banner
    table = soup.find(id='team_schedule').tbody
    rows = table.find_all('tr')

    # Search for the last played game by checking each row to see if that row/game has been played or not
    # If it hasn't it will say preview in the main box and that is our trigger to know we need to stop
    game_num = 1
    for row in rows:
        # Skip the header rows which have the class='thead'
        if row.get('class') and 'thead' in row['class']:
            continue

        # Keep track of the previous game because once we find a game that hasn't been played yet we know the previous one we just checked is the last played game
        if game_num > 1:
            previous_game = {
                'game_num': game_num-1,
                'home_or_away': home_or_away,
                'runs_scored': runs_scored,
                'happened_yesterday': happened_yesterday,
                'game_date': game_date,
            }

        # Each row has multiple <td> columns with the different stats (Date, Opponent, Runs Scored, Runs Allowed, etc...)
        # Search through all those fields and extract the columns that we want, parsing the data to be easiest to work with
        #     - Played Yet?
        #     - Home or Away
        #     - Runs Scored
        fields = row.find_all('td')
        for field in fields:

            if field['data-stat'] == 'date_game':
                date_str = field['csk']
                game_date = datetime.datetime.strptime(
                    date_str, '%Y-%m-%d').date()

                happened_yesterday = helpers.check_yesterday(game_date)

            if field['data-stat'] == 'boxscore':
                game_happened = False if field.string == 'preview' else True

            if (field['data-stat'] == 'homeORvis'):
                home_or_away = 'away' if field.string == '@' else 'home'

            if (field['data-stat'] == 'R'):
                runs_scored = int(field.string)

        game_num += 1

        if not game_happened:
            print(previous_game)

            if previous_game['happened_yesterday'] and \
                    previous_game['home_or_away'] == 'home' and \
                    previous_game['runs_scored'] >= 7:
                return True
            else:
                return False


def check_lafc_score():
    """ 
    Checks the Los Angeles FC score from the previous day to see if it qualifies for a free Chick Fil A sandwich.
    At any home game, if LAFC wins, you can claim a chicken sandwich 
    """

    if USE_LOCAL:
        soup = BeautifulSoup(
            open('sample_pages/2023_lafc_scores.html'), features="html.parser")
    else:
        url = f'https://fbref.com/en/squads/81d817a3/{helpers.CURRENT_DATETIME.year}/matchlogs/c22/schedule/Los-Angeles-FC-Scores-and-Fixtures-Major-League-Soccer'
        soup = helpers.fetch_soup(url)

    # The scores are duplicated on the page (once in the banner and once on the main page)
    # so in order to prevent duplicated work we have to narrow our search down to just the main content (table body or tbody), and not include the banner
    table = soup.find(id='all_matchlogs').tbody
    rows = table.find_all('tr')

    # Search for the last played game by checking each row to see if that row/game has been played or not
    # If it hasn't it will say preview in the main box and that is our trigger to know we need to stop
    game_num = 1
    for row in rows:
        # Skip the header rows which have the class='thead'
        if row.get('class') and 'thead' in row['class']:
            continue

        # Keep track of the previous game because once we find a game that hasn't been played yet we know the previous one we just checked is the last played game
        if game_num > 1:
            previous_game = {
                'game_num': game_num-1,
                'home_or_away': home_or_away,
                'result': result,
                'happened_yesterday': happened_yesterday,
                'game_date': game_date,
            }

        # Checking to see if the item exists in the HTML as for the future games it doesn't
        if row.find('th').a:
            date_str = row.find('th').a.string
            game_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

            happened_yesterday = helpers.check_yesterday(game_date)

        # Each row has multiple <td> columns with the different stats (Date, Opponent, Runs Scored, Runs Allowed, etc...)
        # Search through all those fields and extract the columns that we want, parsing the data to be easiest to work with
        #   - Played Yet?
        #   - Home or Away?
        #   - Win or Loss?
        fields = row.find_all('td')
        for field in fields:
            if field['data-stat'] == 'result':
                if field.string is None:
                    game_happened = False
                else:
                    game_happened = True
                    result = field.string

            if (field['data-stat'] == 'venue'):
                home_or_away = field.string

        game_num += 1

        if not game_happened:
            print(previous_game)

            if previous_game['happened_yesterday'] and \
                    previous_game['home_or_away'] == 'Home' and \
                    previous_game['result'] == 'W':
                return True
            else:
                return False


def check_ducks_score():
    """ 
    Checks the Anaheim Ducks score from the previous day to see if it qualifies for a free Chick Fil A sandwich.
    At any home game, if the Ducks score 5 or more goals, you can claim a chicken sandwich 
    """

    if USE_LOCAL:
        soup = BeautifulSoup(
            open('sample_pages/2023_ducks_scores.html'), features="html.parser")
    else:
        url = f'https://www.hockey-reference.com/teams/ANA/{helpers.CURRENT_DATETIME.year}_games.html'
        soup = helpers.fetch_soup(url)

    # The scores are duplicated on the page (once in the banner and once on the main page)
    # so in order to prevent duplicated work we have to narrow our search down to just the main content (table body or tbody), and not include the banner
    table = soup.find(id='all_games').tbody
    rows = table.find_all('tr')

    # Search for the last played game by checking each row to see if that row/game has been played or not
    # If it hasn't it will say preview in the main box and that is our trigger to know we need to stop
    game_num = 1
    for row in rows:
        # Skip the header rows which have the class='thead'
        if row.get('class') and 'thead' in row['class']:
            continue

        # Keep track of the previous game because once we find a game that hasn't been played yet we know the previous one we just checked is the last played game
        if game_num > 1:
            previous_game = {
                'game_num': game_num-1,
                'home_or_away': home_or_away,
                'goals_scored': goals_scored,
                'happened_yesterday': happened_yesterday,
                'game_date': game_date,
            }

        # Checking to see if the item exists in the HTML as for the future games it doesn't
        if row.find('th').a:
            date_str = row.find('th').a.string
            game_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

            happened_yesterday = helpers.check_yesterday(game_date)

        # Each row has multiple <td> columns with the different stats (Date, Opponent, Runs Scored, Runs Allowed, etc...)
        # Search through all those fields and extract the columns that we want, parsing the data to be easiest to work with
        #     - Played Yet?
        #     - Home or Away
        #     - Goals Scored
        fields = row.find_all('td')
        for field in fields:
            if field['data-stat'] == 'game_outcome':
                game_happened = False if field.string is None else True

            if (field['data-stat'] == 'game_location'):
                home_or_away = 'away' if field.string == '@' else 'home'

            if (field['data-stat'] == 'goals'):
                goals_scored = int(field.string)

        game_num += 1

        if not game_happened:
            print(previous_game)

            if previous_game['happened_yesterday'] and \
                    previous_game['home_or_away'] == 'home' and \
                    previous_game['goals_scored'] >= 5:
                return True
            else:
                return False


def send_emails(subject: str, body: str, email_addresses: list[str]):
    if SHOULD_SEND_EMAIL:
        messenger = Messenger(FROM_EMAIL, PASSWORD)
        messenger.open_conn()

        for email in email_addresses:
            email = email.strip()
            msg = Email(email, subject, body)
            messenger.send_email(msg)

        messenger.close_conn()
        print(constants.EMAIL_SUCCESS_MSG)


def main():
    """ Main entry point of the app """

    # If the season is over for one of the teams and every game has been played
    # this will scan through all the games but ultimately won't do anything because there are no future games

    # Only run from March - October
    if constants.M_MARCH <= helpers.CURRENT_DATETIME.month <= constants.M_OCTOBER:
        if check_angels_score():
            body = f'{constants.ANGELS} won by 7 or more runs!'
            send_emails(helpers.generate_email_subject(
                constants.ANGELS), body, TO_EMAIL.split(','))
        else:
            helpers.print_criteria_not_met(constants.ANGELS)
    else:
        helpers.print_not_in_season(constants.ANGELS)

    print()  # For empty lines

    # Only run from October - April
    if helpers.CURRENT_DATETIME.month >= constants.M_OCTOBER or helpers.CURRENT_DATETIME.month <= constants.M_JUNE:
        if check_ducks_score():
            body = f'{constants.DUCKS} won by 5 or more goals!'
            send_emails(helpers.generate_email_subject(
                constants.DUCKS), body, TO_EMAIL.split(','))
        else:
            helpers.print_criteria_not_met(constants.DUCKS)
    else:
        helpers.print_not_in_season(constants.DUCKS)

    print()  # For empty lines

    # Always run because LAFC season is basically the whole year
    if check_lafc_score():
        body = f'{constants.LAFC} won at home!'
        send_emails(helpers.generate_email_subject(
            constants.LAFC), body, TO_EMAIL.split(','))
    else:
        helpers.print_criteria_not_met(constants.LAFC)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

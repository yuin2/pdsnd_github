import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        cities = ['chicago','new york city','washington']
        if city in cities:
            print('>> Looks like you want to hear about {}. If this is not true, restart the program now!'.format(city.title()))
            break
        else:
            print('>> Invalid input. Please try again.\n')

    # Get user input for filter (month, day, both or none).
    while True:
        data_filter = input('\nWould you like to filter the data by month, day, both, or not at all? Type “none” for no time filter at all.\n').lower()
        if data_filter == 'none':
            month = 'all'
            day = 'all'
            print('\n>> Calculating statistics for {}.\n'.format(city.title()))
            break
        elif data_filter == 'month':
            day = 'all'
            while True:
                month = input('\nWhich month - January, February...June?\n').lower()
                months = ['january', 'february', 'march', 'april', 'may', 'june']
                if month in months:
                    print('\n>> Calculating statistics for {}, {}.\n'.format(city.title(), month.title()))
                    break
                else:
                    print('>> Invalid input. Please try again.')
            break
        elif data_filter == 'day':
            month = 'all'
            while True:
                day = input('\nWhich day - Monday, Tuesday...Sunday?\n').lower()
                days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                if day in days_of_week:
                    print('\n>> Calculating statistics for {}, {}.\n'.format(city.title(), day.title()))
                    break
                else:
                    print('>> Invalid input. Please try again.')
            break
        elif data_filter == 'both':
            while True:
                month = input('\nWhich month - January, February...June?\n').lower()
                months = ['january', 'february', 'march', 'april', 'may', 'june']
                if month in months:
                    while True:
                        day = input('\nWhich day - Monday, Tuesday...Sunday?\n').lower()
                        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                        if day in days_of_week:
                            print('\n>> Calculating statistics for {}, {}, {}.\n'.format(city.title(), month.title(), day.title()))
                            break
                        else:
                            print('>> Invalid input. Please try again.')
                    break
                else:
                    print('>> Invalid input. Please try again.')
            break
        else:
          print('>> Invalid input. Please try again.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nPOPULAR TIMES OF TRAVEL\n')
    start_time = time.time()

    # TO DO: display the most common month
    # find the most popular month
    popular_month = df['Month'].mode()[0]
    print('Most common month: ', popular_month)

    # TO DO: display the most common day of week
    # find the most popular day
    popular_day = df['Day of Week'].mode()[0]
    print('Most common day of week: ', popular_day)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most common hour of day:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nPOPULAR STATIONS AND TRIP\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_name = df['Start Station'].mode()[0]
    popular_start_count = df['Start Station'].value_counts().max()
    print('Most common start station:', popular_start_name, ' | Count:', popular_start_count)

    # TO DO: display most commonly used end station
    popular_end_name = df['End Station'].mode()[0]
    popular_end_count = df['End Station'].value_counts().max()
    print('Most common end station:', popular_end_name, ' | Count:', popular_end_count)

    # TO DO: display most frequent combination of start station and end station trip
     # join the Start Station and End Station column to create a Trip column
    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']

    # find the most frequent trip
    popular_trip = df['Trip'].mode()[0]
    print('Most common trip from start to end(i.e. the most frequent combination of start station and end station:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nTRIP DURATION\n')
    start_time = time.time()

    # TO DO: display total travel time
    traveltime_sum = df['Trip Duration'].sum()
    print('Total travel time:', traveltime_sum)

    # TO DO: display mean travel time
    traveltime_mean = df['Trip Duration'].mean()
    print('Average travel time:', traveltime_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nUSER INFO\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    usertypes_count = df['User Type'].value_counts(dropna=False)
    print('Counts of each user type:\n{}'.format(usertypes_count))

    # TO DO: Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nCounts of each gender:\n{}'.format(gender_count))
    except Exception:
        print('\nNo gender data to share\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        birthyear_earliest = df['Birth Year'].min(skipna=True)
        birthyear_latest = df['Birth Year'].max(skipna=True)
        birthyear_common = df['Birth Year'].mode()[0]
        print('\nEarliest year of birth:', birthyear_earliest)
        print('Most recent year of birth:', birthyear_latest)
        print('Most common year of birth:', birthyear_common)
    except Exception:
        print('No birth year data to share')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays 5 rows if the user would like to see the raw data. If the user answers 'yes,' then the script should print 5 rows of the data at a time, then ask the user if they would like to see 5 more rows of the data. The script should continue prompting and printing the next 5 rows at a time until the user chooses 'no,' they do not want any more raw data to be displayed.
    """
    raw_data = input("\nWould you like to see the raw data? Enter 'yes' or 'no'.\n")
    if raw_data.lower() == 'yes' or raw_data.lower() == 'y':
        print(df.head(5))
        while True:
            start_row = 0
            more_data = input("\nWould you like to see 5 ADDITIONAL rows of raw data? Enter 'yes' or 'no'.\n")
            if more_data.lower() == 'yes' or more_data.lower() == 'y':
                five_rows = df.iloc[start_row: start_row + 5]
                print(five_rows)
                start_row = start_row + 5
                if five_rows.empty:
                    print('>> No more results, we have reached the end of the dataframe that you have requested.')
                    break
                else:
                    print(five_rows)
            elif more_data.lower() not in ['yes','no']:
                print("Invalid input. Please enter'yes' or 'no'.")
                continue
            else:
                break

def restart(df):
    """Restarts the script if the user answers 'yes'. If the user answers 'no,' then the script ends.
    """
    restart = input("\nWould you like to restart? Enter 'yes' or 'no'.\n")
    if restart.lower() != 'yes' restart.lower() != 'y':
        print('-'*40)
        break
    else:
        print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart(df)

if __name__ == "__main__":
	main()

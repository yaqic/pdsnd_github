import time
import pandas as pd
import numpy as np
import datetime as dt

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

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    prompt = "\nWould you like to see data for Chicago, New York, or Washington? "
    while True:
        city = input(prompt).lower().strip()
        if city == 'new york':
            city = 'new york city'
        if city in CITY_DATA.keys():
            break
        print("\nInvalid input, please enter again. Valid inputs are 'Chicago', 'New York', 'Washington'. ")
        
    prompt = "\nWould you like to filter the data by month, day, both, or not at all? Type 'None' for no time filter. "
    while True:
        apply_filter = input(prompt).lower()
        if apply_filter in ('month', 'day','both','none'):
            break
        print("\nInvalid input, please enter again. Valid inputs are 'month', 'day','both','none'. ")

    apply_month_filter = False
    apply_day_filter = False
    month = day = 'all'

    if apply_filter == 'both':
        apply_month_filter = apply_day_filter = True
    elif apply_filter == 'month':
        apply_month_filter = True
    elif apply_filter == 'day':
        apply_day_filter = True
        

    # get user input for month (all, january, february, ... , june)
    prompt_month = "\nWhich month? January, February, March, April, May, June "
    if apply_month_filter:
        while True:
            month = input(prompt_month).lower()
            if month in ('january', 'february', 'march', 'april', 'may', 'june'):
                break
            print("\nInvalid input, please enter again. Valid inputs are 'january', 'february', 'march', 'april', 'may', 'june'. ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    prompt_day = "\nWhich day? Please type your response as an integer (e.g. 0 = Monday, 6 = Sunday) "
    if apply_day_filter:
        while True:
            day = int(input(prompt_day))
            if day in range(7):
                break
            print("\nInvalid input, please enter again. Valid inputs are intergers from 0 to 6. ")

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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    # print('For the selected filter, the month with the most travels is: ' +
    #       str(months[most_common_month-1]).title() + '.')

    print('\nThe most popular month is: ' + str(most_common_month))

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    most_common_day = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')[most_common_day]
    print('\nThe most popular day of week is: ' + str(most_common_day))

    # display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.mode()[0]
    print('\nThe most popular start hour is: ' + str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print('\nThe most popular start station is: ' + most_common_start_station)


    # display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print('\nThe most popular end station is: ' + most_common_end_station)


    # display most frequent combination of start station and end station trip
    df['Start Station - End Station'] = (df['Start Station'] + ' - ' + df['End Station'])
    most_common_start_end_combination = str(df['Start Station - End Station'].mode()[0])
    print('\nThe most popular combination of start station and end station is: ' + most_common_start_end_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nThe total travel time in seconds is : ' + str(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("\nThe mean travel time in seconds is : " + str(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nUser types and their count:\n")
    print(user_types)   

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("\nGender of the users and their count:\n")
        print(gender)   
    except:
        print("\nThere is no gender information in the data set.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        print("\nThe earliest year of birth is " + str(earliest_birth_year))
        most_recent_birth_year = int(df['Birth Year'].max())
        print("\nThe most recent year of birth is " + str(most_recent_birth_year))
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nThe most common year of birth is " + str(most_common_birth_year))
    except:
        print("\nThere is no data of birth year in the data set.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        if view_data in ('yes','no'):
            break
        print('\nInvalid input, please enter "yes" or "no". ')
    
    start_loc = 0
    total_row = df.shape[0]
    while (view_data == 'yes'):
        if start_loc + 5 <= total_row:
            print(df.iloc[start_loc:(start_loc+5)])
            start_loc += 5
            while True:
                view_data = input("Do you wish to continue? (yes/no) ").lower()
                if view_data in ('yes','no'):
                    break
                print('\nInvalid input, please enter "yes" or "no". ')
        else:
            print(df.iloc[start_loc:])
            print('\n You have hit the end of the data set.')
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        
        time_stats(df)
        time.sleep(3)
        station_stats(df)
        time.sleep(3)
        trip_duration_stats(df)
        time.sleep(3)
        user_stats(df)
        time.sleep(3)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

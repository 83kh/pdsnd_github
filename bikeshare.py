import time
import calendar
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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    city_query = "Citys you can select: "
    for city_str in CITY_DATA.keys():
        city_query += "\n"
        city_query += city_str
    city_query += "\nWhich city do you want to explore? "
    while True:
        city_input = input(city_query)
        city = city_input.lower()
        if city in CITY_DATA.keys():
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ""
    month_query = "Which month do you want to explore? "
    month_name_list = list(calendar.month_name)
    month_name_list[0] = "All"
    while True:
        month_input = input(month_query)
        if month_input.title() in month_name_list:
            month = month_input.lower()
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    day_query = "Which day of week do you want to explore? "
    day_name_list = list(calendar.day_name)
    day_name_list.append("All")
    while True:
        day_input = input(day_query)
        if day_input.title() in day_name_list:
            day = day_input.lower()
            break

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
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day of week"] = df["Start Time"].dt.weekday
    
    if month != "all":
        df = df[df["month"] == list(calendar.month_name).index(month.title())]
        
    if day != "all":
        df = df[df["day of week"] == list(calendar.day_name).index(day.title())]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("Most common month : {0}".format(list(calendar.month_name)[df["month"].mode()[0]]))

    # TO DO: display the most common day of week
    print("Most common day of week : {0}".format(list(calendar.day_name)[df["day of week"].mode()[0]]))

    # TO DO: display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    print("Most common start hour : {0}".format(df["hour"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("Most commonly used start station : {0}".format(df["Start Station"].mode()[0]))

    # TO DO: display most commonly used end station
    print("Most commonly used end station : {0}".format(df["End Station"].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df["Station Pair"] = df["Start Station"] + " -> " + df["End Station"]
    print("Most frequent combination of start station and end station trip : {0}".format(df["Station Pair"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time : {0}".format(df["Trip Duration"].sum()))

    # TO DO: display mean travel time
    print("Mean travel time : {0}".format(df["Trip Duration"].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Counts of user types : \n{0}\n".format(df.groupby(by="User Type")["User Type"].count().to_string()))


    # TO DO: Display counts of gender
    if "Gender" in df.keys():
        print("Counts of gender : \n{0}\n".format(df.groupby(by="Gender")["Gender"].count().to_string()))

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.keys():
        print("Earliest year of birth : {0}".format(df["Birth Year"].min()))
        print("Recent year of birth : {0}".format(df["Birth Year"].max()))
        print("Most common year of birth : {0}".format(df["Birth Year"].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    curr_row = 0
    while True:
        next_rows_to_display = input("The number of rows you'd like to see : ")
        if next_rows_to_display.isdigit():
            num_of_rows = int(next_rows_to_display)
            next_row = curr_row + num_of_rows
            if next_row > len(df.index):
                next_row = len(df.index)
            print(df.iloc[curr_row:next_row].to_string())
            curr_row = next_row
            print("{0} / {1}".format(curr_row, len(df.index)))
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            show_raw_data = input("\nWould you like to see raw data? Enter yes or no.\n")
            if show_raw_data.lower() == 'yes':
                display_raw_data(df)
        else:
            print("No Data for the condition!")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
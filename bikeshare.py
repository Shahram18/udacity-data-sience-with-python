import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

message='\nA sample project to process BikeShare data using pandas and numpy.'
print(message)

def get_filters():
    #Get city name.
    while True:
        city=input('\nPlease choose a city between, Chicago, New York City, or Washington: ').lower()
        if city not in CITY_DATA.keys():
            print('\nInvalid city name!, Please choose a city between, Chicago, New York City, or Washington: ')
            continue
        else:
            break
    #Get data by month and day.
    while True:
        q=input('\nDo you want to filter data based on a specific date? Enter "yes" or "no": ').lower()
        a=['yes', 'no']
        if q in a:
            if q=='yes':
                while True:
                    month=input('\nEnter a month from January until June: ').lower()
                    month_list=['january', 'february', 'march', 'april', 'may', 'june']
                    if month not in month_list:
                        print('\nInvalid Input! You should select a month from first six months')
                        continue
                    else:
                        break
                while True:
                    day=input('\nEnter a day-name of the week (example: Monday) or "all": ').lower()
                    week=['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
                    if day not in week:
                        print('\nInvalid Input! Please type a day-name of the week (example: Monday)')
                        continue
                    else:
                        break
                message1='Processing data for {}\' filtered by month(s) {} and weekday(s) {}.\n'
                print(message1.format(city.title(), month.title(), day.title()))
            else:
                if q=='no':
                    month='all'
                    day='all'
                    message2='Processing data for {}\'s for the first six months of 2017.\n'
                    print(message2.format(city.title()))
                    break
        else:
            print('\nIs that a "yes" or "no"!')
            continue
        break
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    #Load data to a dataframe
    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))
    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #Extract dates to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour']=df['Start Time'].dt.hour
    #Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]
    #Filter by day of week 
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_res(df, month, day):
    #Find the most frequent times of travel.
    print('\nThe Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['month'] = df['Start Time'].dt.month_name()

    if month == 'all':
        #Find the most common month
        common_month=df['month'].mode()[0]
        print('\n{} is the most used common month.'.format(common_month))

    if day == 'all':
        #Find the most common day of week
        common_day=df['day_of_week'].mode()[0]
        print('\n{} is the most common day of the week.'.format(common_day))
    #Find the most common start hour
    common_hour=df['hour'].mode()[0]
    print('\n{} is the most ferquent hour.'.format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_res(df):
    #Find the most popular stations and trip.
    print('\The Most Popular Stations and Trip...\n')
    start_time = time.time()
    #Find most commonly used start station
    used_start_station=df['Start Station'].mode()[0]
    #Find most commonly used end station
    used_end_station=df['End Station'].mode()[0]
    #Find most frequent combination of start station and end station trip
    combine_station= df['Start Station'] + ' to ' + df['End Station']
    used_combine_station=combine_station.mode()[0]
    print('{} is the most popular start station.\n{} is the most popular end station.\
        \nThe most common trip from start to end {}'.format(used_start_station,used_end_station,used_combine_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_res(df):
    #Find the total and average trip duration.
    print('\Trip Duration...\n')
    start_time = time.time()
    #Find total travel time
    total_time=df['Trip Duration'].sum()
    #Find average travel time
    average_time=df['Trip Duration'].mean()

    print('\nTotal trip duration in seconds is: ', total_time)
    print('\nAverage trip duration in seconds is: ', average_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_res(df, city):
    #Find on bikeshare users.
    print('\nUser Count...\n')
    start_time = time.time()
    #Find counts of user types
    user_count=df['User Type'].value_counts()
    print('\nUser Count and user types:\n ',user_count)
    #Find counts of gender
    if city !='washington':
        gender_count=df['Gender'].value_counts()
        print('\nStats. about gender:\n ',gender_count)
    #Find the earliest, most recent, and most common year of birth
        earliest_yob=df['Birth Year'].min()
        recent_yob=df['Birth Year'].max()
        common_yob=df['Birth Year'].mode()[0]
        print('\nEarliest birth year: {}.\nMost recent birth year: {}.\
            \nMost common birth year: {}.'.format(earliest_yob, recent_yob, common_yob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    print('\Display raw data...\n')
    start_time = time.time()
    x = 0
    while True:
        raw = input('\nWould you like a sample of the raw data? Enter "yes" or "no": ')
        raw = raw.lower()
        if raw != 'yes':
            break
        else:
            x = x + 5
            print(df.iloc[x: x + 5])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_res(df, month, day)
        station_res(df)
        trip_duration_res(df)
        user_res(df, city)
        raw_data(df)
        
        restart=input('\nWould you like to restart? Enter "yes" or "no": \n')
        if restart.lower() != 'yes':
            break

if __name__ == '__main__' :
    main()
import time
import json
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = { 1:'Sunday', 2:'Monday', 3:'Tuesday', 4:'Wednesday', 5:'Thursday', 6:'Friday', 7:'Saturday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = state = month = day = ""

    print('\nHello! Let\'s explore some US bikeshare data!')
    # Gets user input for city (chicago, new york, washington).
    try:        
        while city == "":
            inputCity = input('\nWould you like to see data from Chicago, New York, or Washington? ')
            if inputCity != "":
                inputCity = inputCity.strip().lower()
                if inputCity in ('chicago', 'new york', 'newyork',  'washington'):
                    city = inputCity
                    if city in ('new york', 'newyork'):
                        city = 'new york'
                else:
                    print('\nThe input text wasn\'t one of the mentioned city names. \nPlease enter the name of the city.')
            else:
                print('\nPlease enter the name of the city.')
    except Exception as e:
        city = 'chicago'
        print ('There is something wrong, so the city \'chicago\' was selected as the default city.')        
        
    # Gets user input for one of the states : month, day, both, or none.
    try:       
        while state == "":
            inputState = input('\nWould you like to filter the data by month, day, both, or not at all? ' +
                               'Type \"none\" for no time filter. ')
            if inputState != "":
                inputState = inputState.strip().lower()
                if inputState in ('month', 'day', 'both', 'none'):
                    state = inputState
    except Exception as e:
        state = 'both'
        print ('There is something wrong, so the state \'both\' was selected as the default.')
    
    if state == 'none':
        month = 'all'
        day = 'all'
    elif state == 'month':
        day = 'all'
    elif state == 'day':
        month = 'all'

    # Gets user input for month (all, january, february, ... , june).
    if state in ('month', 'both'):
        try:            
            while month == "":
                inputMonth = input('\nWhich month? January, February, March, April, May, or June? ')
                if inputMonth != "":
                    inputMonth = inputMonth.strip().lower()
                    if inputMonth in MONTHS:
                        month = inputMonth                        
                    else:
                        print('\nThe input text wasn\'t one of the mentioned months.')
                else:
                    print('\nPlease enter the name of the mentioned months.')
        except Exception as e:
            month = 'all'
            print ('There is something wrong, so \'all\' months were selected.')

    # Gets user input for day of week (all, monday, tuesday, ... sunday).
    if state in ('day', 'both'):
        try:
            day = ""
            while day == "":
                print('\nWhich day? - 1=Sunday, 2=Monday, 3=Tuesday, 4=Wednesday, 5=Thursday, 6=Friday, or 7=Saturday?')
                inputDay = input('Please type your reponse as an integer (1-7): ')                
                if inputDay != "":
                    try:
                        inputDay = int(inputDay.strip())
                        if 1 <= inputDay <= 7:
                            day = DAYS[inputDay]
                        else:
                            print('\nThe input text wasn\'t valid number (1-7).')
                    except Exception as ee:
                        print('\nThe input text wasn\'t valid number (1-7).')                    
                else:
                    print('\nPlease enter the day number (1-7).')
        except Exception as e:
            day = 'all'
            print ('There is something wrong, so \'all\' days were selected.')

    print(f"\nFilter: city={city}, month={month}, day={day}")
    print('-'*60)    
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
    # Loads data file into a dataframe.  
    df = pd.read_csv(CITY_DATA[city])
    
    # Converts the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extracts month and day of week from Start Time to create new columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() 
    
    # Filters by month if applicable.
    if month != 'all':
        # Uses the index of the months list to get the corresponding int.      
        month = MONTHS.index(month) + 1
    
        # Filters by month to create the new dataframe.
        df = df[df['month'] == month] 
        
    # Filters by day of week if applicable.
    if day != 'all':
        # Filters by day of week to create the new dataframe.
        df = df[df['day_of_week'] == day.title()] 

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print(f'\nCalculating The Most Frequent Times of Travel in {city.title()} city.\n')
    start_time = time.time()
    if month == 'all':
        # Displays the most common month.
        popular_month = df['month'].mode()[0]
        print(f"\tMost popular month: {MONTHS[popular_month-1].title()}")

    if day == 'all':
        # Displays the most common day of week.
        popular_dow = df['day_of_week'].mode()[0]
        if month == 'all':
            print(f"\tMost popular day of week: {popular_dow}")
        else:
            print(f"\tMost popular day of week in {month.title()}: {popular_dow}")

    # Displays the most common start hour.
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    if month == 'all' and day == 'all':
        print(f"\tMost popular hour: {popular_hour}")
    elif month == 'all' and day != 'all':
        print(f"\tMost popular hour in {day.title()}s: {popular_hour}")
    elif month != 'all' and day == 'all':
        print(f"\tMost popular hour in {month.title()}: {popular_hour}")
    else:
        print(f"\tMost popular hour in {month.title()} on {day.title()}s: {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""

    print(f'\nCalculating The Most Popular Stations and Trip in {city.title()} on {month.title()} months at {day.title()} days.\n')
    start_time = time.time()

    # Displays most commonly used start station.
    popular_start_station = df['Start Station'].mode()[0]
    print(f"\tMost popular start station: {popular_start_station}")

    # Displays most commonly used end station.
    popular_end_station = df['End Station'].mode()[0]
    print(f"\tMost popular end station: {popular_end_station}")

    # Displays most frequent combination of start station and end station trip.    
    popular_trip = df.groupby(['Start Station','End Station']).size().idxmax()
    print(f"\tMost frequent combination of start station and end station trip: {popular_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print(f'\nCalculating Trip Duration in {city.title()} on {month.title()} months at {day.title()} days.\n')
    start_time = time.time()

    # Displays total travel time (sum , count).
    trip_count = df['Trip Duration'].count()
    trip_duration_sum = df['Trip Duration'].sum()

    # Displays mean travel time.
    trip_duration_mean = df['Trip Duration'].mean()
    print(f'Total duration: {trip_duration_sum//3600} hours, Count: {trip_count}, Average Duration: {trip_duration_mean//60} minutes.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print(f'\nCalculating User Stats in {city.title()} on {month.title()} months at {day.title()} days.\n')
    start_time = time.time()

    # Displays counts of user types.
    print('\nTrip counts per User Type ...')
    print(df.groupby(['User Type']).size().reset_index(name='trip_counts').to_string(index=False))    

    # The data for Gender and Birth Year columns, exists for two cities, chicago and new york city.
    if city == 'chicago' or city == 'new york':
        # Displays counts of gender.
        print('\nTrip counts per Gender ...')
        print(df.groupby(['Gender']).size().reset_index(name='trip_counts').to_string(index=False))

        # Displays earliest, most recent, and most common year of birth.
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print(f'\nBirth Year statistics: Earliest= {earliest_year}, Most recent= {recent_year}, Most common= {common_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def iterate_by_num(df, num):
    """Iterates df and each time, generate a string including content of num rows."""
    for i in range(df.count()[0]//num + 1):
        json_str=""
        for n in range(num):     
            # Checks the maximum existing rows in df.    
            if (i*num + n) <= (df.count()[0] - 1):
                json_str += json.dumps(json.loads(df.iloc[i*num + n].to_json()), indent=4) + '\n'

        yield json_str


def show_raw_data (df):
    """Shows the content of 5 rows of df for each time after asking user about that."""
    
    act = input('\nWould you like to view individual trip data? (Type yes or no): ')
    if act.lower() == 'yes' or act.lower() == 'y':
        for json_str in iterate_by_num(df, 5):
            print(json_str)
            act = input('Continu? (Type yes or no): ')
            if act.lower() == 'no' or act.lower() == 'n':
                break

def main():
    while True:
        # Asks user to specify a city, month, and day for filtering the data.
        city, month, day = get_filters()  

        # Loads data based on filters provided previous step.
        df = load_data(city, month, day)

        # Displays statistics on the most frequent times of travel for filtered data.
        time_stats(df, city, month, day)

        # Displays statistics on the most popular stations and trip for filtered data.
        station_stats(df, city, month, day)

        # Displays statistics on the total and average trip duration for filtered data.
        trip_duration_stats(df, city, month, day)     

        # Displays statistics on bikeshare users for filtered data.                        
        user_stats(df, city, month, day)

        # Shows the content of 5 rows of filtered data for each time.
        show_raw_data (df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

        print('\n========================================================================================')
        print('\n====================================== New Filter ======================================')

if __name__ == "__main__":
	main()

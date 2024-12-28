# This script analyzes app data from both Google Play Store and Apple App Store
# to identify profitable app opportunities in both markets

from csv import reader

# Import and structure the data
### Google Play Store data import ###
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]    # Store the header row separately
android = android[1:]         # Store all data except header

### Apple App Store data import ###
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]          # Store the header row separately
ios = ios[1:]               # Store all data except header

# Helper function to explore the dataset
def explore_data(dataset, start, end, rows_and_columns=False):
    """
    Prints a slice of the dataset and optionally shows total rows and columns
    
    Args:
        dataset: List of lists containing the data
        start: Starting index for the slice
        end: Ending index for the slice
        rows_and_columns: Boolean to print total dimensions
    """
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n')
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

# Print headers and sample data for both datasets
print(android_header)
print('\n')
explore_data(android, 0, 3, True)

print(ios_header)
print('\n')
explore_data(ios, 0, 3, True)

# Data cleaning: Remove incorrect data
print(android[10472])  # Print incorrect row for reference
del android[10472]     # Delete the incorrect row

# Remove duplicate entries
# First, create lists to track unique and duplicate apps
duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)

# Create a dictionary to keep only the version of each app with the most reviews
reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews

# Create clean dataset with only the highest-reviewed version of each app
android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)

# Function to check if app name is English
def is_english(string):
    """
    Checks if a string contains primarily English characters
    Returns False if more than 3 non-ASCII characters are found
    """
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    return non_ascii <= 3

# Filter out non-English apps
android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)

# Filter to keep only free apps
android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)

# Function to create frequency tables
def freq_table(dataset, index):
    """
    Creates a frequency table for a column in the dataset
    Returns percentages for each unique value
    """
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages

# Function to display sorted frequency tables
def display_table(dataset, index):
    """
    Displays a sorted frequency table for better readability
    """
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])

# Analysis of app genres and categories
# Calculate average ratings for iOS apps by genre
genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)

# Calculate average installs for Android apps by category
categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)

# Analysis of specific categories (e.g., BOOKS_AND_REFERENCE)
# Print details of apps in specific categories to identify opportunities
for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])

# The script concludes that creating a book-based app with additional features
# (like daily quotes, audio versions, quizzes, discussion forums) could be
# profitable for both markets, as there's significant user interest but room
# for innovative features beyond basic e-book functionality.

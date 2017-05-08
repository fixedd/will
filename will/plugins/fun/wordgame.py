from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import string
import requests
import random

WORD_GAME_TOPICS = [
    "3-Letter Words", "4-Letter Words", "5-Letter Words", "A Baseball Player's Name",
    "A bird", "A boy's name", "A drink",
    "A fish", "A Football Player's Name", "A girl's name",
    "A relative", "A river", "Abbreviations",
    "Acronyms", "Action Figures", "Action Words",
    "Actors", "Actresses", "Adjectives",
    "African Animals", "African Countries", "After-School Activities",
    "Airlines", "Alcoholic Drinks", "Amphibians",
    "An animal", "Animal Homes", "Animal noises",
    "Animals Found in Foreign Lands", "Animals in books or movies", "Animals That Advertise Products",
    "Animals That Are a Certain Color", "Animals That Fly", "Animals That Hop or Jump",
    "Animals That Live Underground", "Animals That Swim", "Animals",
    "Any Green Food or Drink", "Appliances ", "Appliances",
    "Arctic Animals", "Areas of Mathematics Study", "Areas of Study",
    "Articles of Clothing", "Artists", "Asian Animals",
    "Asian Capital Cities", "Asian Countries", "At The Zoo",
    "Athletes Who Do Commercials", "Athletes", "Australian/New Zealand Animals",
    "Authors", "Automobiles", "Awards/ceremonies",
    "Baby Clothes", "Baby foods", "Bad habits",
    "Bands with One-word Names", "Bathroom Accessories", "Beers",
    "Beverages", "Birds", "Blockbuster Movies",
    "Board games", "Bodies of water", "Bones of the Body",
    "Book Titles", "Books,Movies,or TV Shows about About Sports", "Boy Bands",
    "Breakfast Cereals", "Breakfast foods", "Building Toys",
    "Canadian Provinces", "Cancelled TV Shows", "Candy",
    "Canned Food", "Capitals", "Car Parts",
    "Card games", "Carpentry Tools", "Cars",
    "Cartoon characters", "Cat Breeds", "Celebrations Where Gifts Are Given",
    "Celebrities You'd Like to Meet", "Celebrities", "Chemicals",
    "Children's books", "Children's Games", "Children's Songs",
    "Children's TV Shows", "Childrens Books", "Chinese Food",
    "Christmas Carols", "Christmas songs", "Cities",
    "Classic Commercials", "Classic Movies", "Classic Toys",
    "Classical Music", "Clothing Worn by Cowboys", "Clothing",
    "Cocktails", "Cold Climates", "Cold Drinks",
    "Cold Places", "College Majors", "Colleges/Universities",
    "Colors", "Comedies", "Comedy Shows",
    "Companies", "Compound Nouns Formed With 'Life'", "Compound Nouns Formed With 'Light' (Flashlight,Spotlight,etc.)",
    "Compound Nouns Formed With 'Time'", "Computer parts", "Computer programs",
    "Condiments", "Constellations", "Contractions",
    "Cooking Shows", "Cooking utensils", "Cosmetics/Toiletries",
    "Countries", "Country Flags", "Country Names Beginning With a Particular Letter",
    "Couples", "Crimes", "Cruises",
    "Dairy Products", "Dangerous Animals", "Daytime TV Shows",
    "Desk Accessories", "Desserts", "Diet foods",
    "Diseases", "Disgusting Things to Eat or Drink ", "Disney Movies",
    "Dog Breeds", "Dolls", "Drugs that are abused",
    "Eighties Music", "Electronic gadgets", "Entertainment",
    "Equipment", "Ethnic foods", "European Animals",
    "European Capital Cities", "European Countries", "Excuses for being late",
    "Famous Artists", "Famous Characters", "Famous Children",
    "Famous duos and trios", "Famous Females", "Famous Paintings",
    "Famous Players", "Fantasy", "Farm Animals",
    "Fast Animals", "Fast Food Restaurant Names", "Fast-Food",
    "Fears", "Female Athletes", "Female Singers",
    "Female Stars", "Fictional characters", "Fictitious Places",
    "Fish", "Floor Coverings", "Flowers",
    "Folk Songs", "Food at a Carnival or Fair", "Food Found in a Casserole",
    "Food Found In a Deli ", "Food You Eat Raw", "Food/Drink that is green",
    "Foods you eat raw", "Footware", "Footwear",
    "Foreign Cities", "Foreign words used in English", "Foreign Words",
    "Foriegn cities", "Found in a Salad Bar", "Four-Legged Animals",
    "Fried Foods", "From TV,Movies,or Books ", "Fruits",
    "Furniture by Room (i.e. bedroom,kitchen,etc.)", "Furniture in This Room", "Furniture You Sit On (or At)",
    "Furniture", "Game terms", "Games",
    "Gardening Tasks", "Gems", "Gifts for the Bride & Groom",
    "Gifts", "Gifts/Presents", "Gourmet Foods",
    "Halloween costumes", "Health Food", "Heroes",
    "Historic events", "Historical Figures", "Hobbies",
    "Holiday Activities ", "Holiday Activities", "Holiday Songs",
    "Holidays", "Honeymoon spots", "Horror Movies",
    "Hors D'oeuvres", "Hot Drinks", "Hot Places",
    "Household chores", "Ice cream flavors", "In Europe",
    "In National Geographic Magazine", "In North America", "In the NWT (Northwest Territories,Canada)",
    "In Your Hometown", "Insects", "Internal Organs",
    "Internet lingo", "Internet", "iPhone Apps",
    "Islands", "Italian Food", "Items in a catalog",
    "Items in a kitchen", "Items in a Refrigerator", "Items in a suitcase",
    "Items in a vending machine", "Items in this room", "Items in Your Purse/Wallet",
    "Items you save up to buy", "Items you take on a road trip", "Items You Take On A Trip",
    "Junk Food", "Kinds of candy", "Kinds of Dances",
    "Kinds of soup", "Kitchen Appliances", "Lakes",
    "Languages", "Last Names", "Legal Terms",
    "Leisure activities", "Long-Running TV Series", "Love Songs",
    "Love Stories", "Low Calorie Foods", "Magazines",
    "Male Singers", "Male Stars", "Mammals",
    "Mascots", "Math Functions", "Math terms",
    "Mechanic's Tools", "Medical Terms", "Medicine Names",
    "Medicine/Drugs", "Men's Clothing", "Menu items",
    "Metals", "Mexican Food", "Mexican Foods",
    "Military Leaders", "Minerals", "Models",
    "Mountain Ranges", "Movie Stars (Dead)", "Movie Stars (Living)",
    "Movie Theme Songs", "Movie titles", "Movies on TV",
    "Music Programs", "Musical groups", "Musical Instruments",
    "Mythological Characters", "Names used in songs", "Names Used in the Bible",
    "Nationalities", "Newscasters/Journalists", "Nickelodeon",
    "Nicknames", "Nineties Music", "Nintendo",
    "North/South American Animals", "North/South American Countries", "Not On Planet Earth",
    "Notorious people", "Nouns", "Nursery Rhymes",
    "Nursing Terms", "Occupations", "Ocean things",
    "Oceans", "Offensive words", "Office Items",
    "Office Tools", "Olympic events", "On a Wine List",
    "Parks", "Parts of Speech", "Parts of the body",
    "People in Uniform", "People Who Do Dangerous Jobs", "People Who Do Door To Door",
    "People Who Work Alone", "People Who Work at Night", "People You Admire",
    "People You Aviod", "People's Names Used in Songs", "Periodic Table Elements",
    "Personality traits", "Pets", "Photography",
    "Pizza toppings", "Places in Europe", "Places To Hang Out",
    "Places to hangout", "Places You Wouldn't Want to live", "Played Inside",
    "Played Outside", "Plumbing Tools", "Political Figures",
    "Possessive Pronouns", "Presidents", "Prime Time TV",
    "Pro Sports Teams", "Produce", "Product Names",
    "Pronouns", "Provinces or States", "Punctuation",
    "Rappers", "Reality TV", "Reasons to be Absent",
    "Reasons to call 911", "Reasons to Go to the Principal's Office", "Reasons to make a phone call",
    "Reasons to quit your job", "Reasons to take out a loan", "Reference Books",
    "Reptiles", "Reptiles/Amphibians", "Restaurants",
    "Rivers", "Road Signs", "Sales Terms",
    "Sandwiches", "School subjects", "School supplies",
    "Science Fiction", "Science Terms", "Scientific Disciplines",
    "Seafood", "Seas", "Seventies Music",
    "Sex Symbols", "Shows You Don't Like", "Singers",
    "Sit Coms", "Sixties Music", "Slow Animals",
    "Snacks", "Soft Drinks", "Software",
    "Someone From Your Past", "Something you keep hidden", "Something you're afraid of",
    "Song titles", "Songs with a Name in the Title", "South American Countries",
    "Spices", "Spices/Herbs", "Spicy foods",
    "Sporting Events", "Sports equipment", "Sports equiptment",
    "Sports Mascots", "Sports Personalities", "Sports Played Indoors",
    "Sports Played Inside", "Sports played outdoors", "Sports Played Outside",
    "Sports Stars", "Sports Teams", "Sports Terms",
    "Sports", "Stars Who Appear in Both TV & Movies", "States",
    "Stones/Gems", "Store names", "Street Names",
    "Styles of Shoes", "Summer Olympics Sports", "Superlative Adjectives",
    "T.V. Show Theme Songs", "T.V. Shows", "Teaching Tasks",
    "Teaching Terms", "Team Names", "Television stars",
    "Terms of endearment", "Terms of Measurement", "Terms Referring to rain,snow,etc.",
    "Terms", "Theme Songs", "Things Animals Eat",
    "Things Associated with Autumn", "Things Associated with Spring", "Things Associated with Summer",
    "Things Associated with Winter", "Things at a carnival", "Things at a circus",
    "Things at a football game", "Things found at a bar", "Things Found in a Basement Cellar",
    "Things found in a desk", "Things found in a hospital", "Things Found in a Locker",
    "Things Found in a Park", "Things found in New York", "Things Found in the Cafeteria",
    "Things Found in the Water", "Things Found On a Map", "Things From a Stationary Store",
    "Things in a Classroom", "Things in a grocery store", "Things in a medicine cabinet",
    "Things in a park", "Things in a Souvenir Shop", "Things in the kitchen",
    "Things in the sky", "Things Made of Metal", "Things On a Beach",
    "Things Sold in Commercials", "Things that are black", "Things that are cold",
    "Things that Are Flat (Coin,Paper,Floor,Etc.)", "Things that are Found in the Ocean", "Things that are hot",
    "Things that Are in a Medicine Cabinet", "Things that Are in a Park", "Things that Are in the Sky",
    "Things That Are Loud", "Things that Are Made of Glass", "Things that Are Made of Plastic",
    "Things that Are Made of Wood", "Things that Are Naturally Round", "Things that Are Naturally Yellow,Blue,Red,Etc.",
    "Things That Are Red", "Things that are round", "Things that are square",
    "Things that are sticky", "Things that Are Terrifying", "Things That Are White",
    "Things that Burn", "Things that can get you fired", "Things that can kill you",
    "Things that Cost a Lot", "Things that Do Not Break When Dropped", "Things That Feel Hot",
    "Things That Feel Soft", "Things that Found at a Circus", "Things that grow",
    "Things that have buttons", "Things that have spots", "Things that have stripes",
    "Things that have wheels", "Things that Have Wings", "Things that Jump or Bounce",
    "Things that jump/bounce", "Things that Make You Itch", "Things that make you smile",
    "Things that People Lose", "Things that Smell Bad", "Things that Smell Good",
    "Things That Taste Spicy", "Things that use a remote", "Things that You Wear",
    "Things to do at a party", "Things to do on a date", "Things With Stripes",
    "Things with tails", "Things Worn From the Waist Down", "Things Worn From the Waist Up",
    "Things you buy for kids", "Things You Can See", "Things You Carry",
    "Things you do at work", "Things You Do Every Day", "Things you do everyday",
    "Things You Do in Gym Class", "Things You Do in Study Hall", "Things You Do While Watching TV",
    "Things You Don't Want to Hear", "Things you get in the mail", "Things you get tickets for",
    "Things you make", "Things You Need Tickets To See", "Things You Never Tasted",
    "Things You Plug in", "Things you replace", "Things you save up to buy",
    "Things You Scream at Officials", "Things you see at the zoo", "Things You See in a City",
    "Things you shouldn't touch", "Things you shout", "Things You Sit In/on",
    "Things you store items in", "Things You Study in Geography", "Things You Study in History",
    "Things you throw away", "Things you wear", "Things you're allergic to",
    "Titles people can have", "Tools", "Tourist attractions",
    "Toys", "Train Travel Destinations", "Trees",
    "Tropical Locations", "TV Character Names", "TV Shows",
    "TV Stars", "Types of Art (i.e. Fine,Abstract,etc.)", "Types of Cheese",
    "Types of Drink", "Types of drinks", "Types of Meat",
    "Types of Rocks", "Types of Toys", "Types of weather",
    "U.S. Cities", "Under Garments", "United States Capitals",
    "Units of Measure", "Vacation spots", "Vegetable Garden Plants",
    "Vegetables", "Vehicles", "Video games",
    "Villains", "Villains/Monsters", "Villians",
    "Wall Coverings", "Warm Climates", "Water Sports",
    "Ways to get from here to there", "Ways to kill time", "Weapons",
    "Weather", "Websites", "Weekend Activities",
    "Window Coverings", "Winter Olympics Sports", "Wireless things",
    "With A High Altitude", "Women's Clothing", "Words associated with exercise",
    "Words associated with money", "Words associated with winter", "Words Beginning With a Particular Letter",
    "Words Beginning With the Prefix '-Mis'", "Words Beginning With the Prefix '-Un'", "Words Ending in '-ed'",
    "Words Ending in '-ly'", "Words ending in '-n'", "Words Said In Anger",
    "Words That Can Be Used as Conjunctions", "Words that End in '-ing'", "Words with a Double Letter",
    "Words with double letters", "World Leaders/Politicians", "World Records",
]



class WordGamePlugin(WillPlugin):
    @respond_to("^(play a word game|scattegories)$")
    def word_game_round(self, message):
        "Play a game where you think of words that start with a letter and fit a topic."

        letter = random.choice(string.letters).upper()
        topics = []

        while len(topics) < 10:
            new_topic = random.choice(WORD_GAME_TOPICS)
            if new_topic not in topics:
                topics.append({
                    "index": len(topics) + 1,
                    "topic": new_topic
                })

        context = {
            "letter": letter,
            "topics": topics
        }
        self.say(rendered_template("word_game.html", context), message=message)

from django.contrib.auth.models import User 
from qpost.models import *
from authenticate.models import *
import random
from os import walk
from random import choice
from django.core.files import File
from django.utils import timezone
from datetime import timedelta

first_names = ['Bob', 'Hort', 'Whim', 'Trouble', 'Mechaniclon', 'Partario', 'Wheat', 'Barley', 'Rumple', 'Heidi', 'Banana', 'Casper', 'Dante', 'Ruble', 'Tomiko', 'Hotty', 'Rich', 'Ducks', 'Holly', 'Elmo', 'Gogo', 'Colombo', 'Mumsy', 'Dumbo', 'Betty', 'Matilda', 'Megatron', 'Shachou', 'John', 'Pocahontas', 'Phone', 'Samsung', 'PC', 'Board', 'Cable', 'Steel', 'Abcissa', 'Clock', 'Fire', 'Red', 'Blue', 'Green', 'Mustard', 'Scarlet', 'Trebuchet', 'Plane', 'Mug', 'Clock', 'Turkey', 'Pizza', 'Pho', 'Hum', 'Hoodie', 'Gauss', 'Djikstra', 'Bellman', 'Glass', 'Health', 'Code', 'Whiz', 'Gee', 'Stripe', 'Joe', 'Karam', 'IKEA', 'Mad', 'Tape', 'Shadow', 'Sonic', 'Tails', 'Xilia', 'Luke', 'Ash', 'Brock', 'Mario', 'Elevator', 'Exit', 'Turquoise', 'Dimension', 'Username']

last_names = ['Umbridge', 'Haze', 'Grey', 'Stuff', 'Safari', 'Meerkat', 'Delinquent', 'Shade', 'Code', 'Bootstrap', 'Perfect', 'Virtual', 'Trespass', 'Starships', 'Alice', 'Serenity', 'Stairway', 'Destruction', 'Stranger', 'Sun', 'Pierce', 'Rainbow', 'Concrete', 'Paradise', 'Plate', 'Stress', 'Test', 'Legion', 'Horde', 'Fusion', 'Icarus', 'Amnesia', 'Wrong', 'Spectrum', 'Shotgun', 'Black', 'White', 'Red', 'Yellow', 'Purple', 'Lilac', 'Violet', 'Heat', 'Willow', 'Heading', 'Subheading', 'Password', 'Alfredo', 'Facebook', 'Twitter', 'Pease', 'Global', 'Universe', 'Globule', 'Hello', 'Tease', 'Police', 'Hello', 'Twitch', 'Heater', 'Bubbles']

emails = ['@gmail.com', '@msn.com', '@hotmail.com', '@comcast.com', '@yahoo.com']

locs = ['Boston, MA', 'Chicago, IL', 'Houston, TX', 'San Fransisco, CA', 'Seattle, WA', 'New York, NY']

def generate_users(numUsers):
    usernames = {}
    for i in range(numUsers):
        first_name = first_names[random.randint(0, len(first_names) - 1)]
        last_name = last_names[random.randint(0, len(last_names) - 1)]
        username = (first_name.lower() + last_name.lower())
        while (username in usernames or len(User.objects.filter(username=username)) > 0):
            username += 'Xx'
            username = 'xX' + username
        usernames[username] = True
        password = 'hubba'
        email_suffix = emails[random.randint(0, len(emails) - 1)]
        email = (first_name.lower() + last_name.lower() + email_suffix)
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        location = locs[random.randint(0, len(locs) - 1)]
        stats = ''
        for i in range(9):
            random_stat = random.randint(0, 10)
            stats += str(random_stat)
            if not i==8:
                stats += ','
        description = 'I am The One. You are not The One. I will always be The One. Maybe you can be The Two. Then, together we could be The Three. How about it? Admittedly, I find myself very attracted to you.'
        quser = QUser(user=user, location=location, stats=stats,description=description)
        quser.save()

verbs = ['Cheese', 'Troll', 'Dance', 'Carry', 'Hit on', 'Flirt', 'Poke', 'Eat', 'Consume', 'Organize', 'Climb', 'Pickle', 'Wrap', 'Defy', 'Expatriate', 'Vulcanize', 'Gobble', 'Absolve', 'Help', 'Officiate', 'Develop', 'Intensify', 'Haunt', 'Hug', 'Envelop', 'Please', 'Force', 'Compile', 'Code']

helpers = ['the']

adjectives = ['Green', 'Red', 'Blue', 'Orange', 'Yellow', 'White', 'Black', 'Indigo', 'Fluttering', 'Sparkling', 'Tender', 'Moist', 'Soft', 'Cuddly', 'Warm', 'Fuzzy', 'Delicious', 'Accommodating', 'Supple', 'Shrimpy', 'Elegant', 'Omnivorous', 'Humble', 'Cordial', 'Jumbo', 'Plastic', 'Taut', 'Firm', 'Sweet', 'Juicy']

nouns = ['Shoes', 'Cheese', 'Pizza', 'Pho', 'Burrito', 'Manchego', 'Bubbles', 'Latte', 'Trash', 'Pinball', 'Pigeon', 'Dog', 'Gumbo', 'Doge', 'Chocolate', 'Plebe', 'Knave', 'Grub', 'Pumpkin', 'Clock', 'Homie', 'Jacket', 'Gobbledygook', 'Elevator', 'Treat', 'Hair', 'Carpet', 'Silk']

# def generate_quests(numQuests):
#     for i in range(numQuests):
#         random_verb = verbs[random.randint(0, len(verbs) - 1)]
#         random_helper = helpers[random.randint(0, len(helpers) - 1)]
#         random_adjective = adjectives[random.randint(0, len(adjectives) - 1)]
#         random_noun = nouns[random.randint(0, len(nouns) - 1)]
#         quest_name = (random_verb + ' ' + random_helper + ' ' + random_adjective + ' ' + random_noun)

#         def get_random_username():
#             users = User.objects.all()
#             random_user = users[random.randint(0, len(users) - 1)]
#             return random_user.username
        
#         poster = get_random_username()
#         description = 'Whatever you want it to be. Yo.'
#         rating = random.randint(0, 5)
#         stats = ''
#         for i in range(9):
#             random_stat = random.randint(0, 10)
#             stats += str(random_stat)
#             if not i==8:
#                 stats += ','
#         quest = Quest(name=quest_name, user_posted_name=poster, description=description, rating=rating, stats=stats, number_completed_users = 0)
#         quest.save()

minor_locs = ['House', 'Library', 'Bathroom', 'Kitchen', 'Diner', 'Lab', 'Chocolate Factory', 'Room', 'Hall', 'Country', 'Palace']

def add_posted_quests(max_num_posted):
    qusers = QUser.objects.all()
    for quser in qusers:
        num_quests = random.randint(0, max_num_posted)
        for i in range(num_quests):
            random_verb = verbs[random.randint(0, len(verbs) - 1)]
            random_helper = helpers[random.randint(0, len(helpers) - 1)]
            random_adjective = adjectives[random.randint(0, len(adjectives) - 1)]
            random_noun = nouns[random.randint(0, len(nouns) - 1)]
            quest_name = (random_verb + ' ' + random_helper + ' ' + random_adjective + ' ' + random_noun)
            if len(Quest.objects.filter(name=quest_name).filter(user_posted_name=quser.user.username)) > 0:
                continue
            description = "whatever you want it to be. Yo."
            rating = random.randint(0, 5)
            stats = ''
            for i in range(9):
                random_stat = random.randint(0, 10)
                stats += str(random_stat)
                if not i==8:
                    stats += ','
            city = quser.location
            quest = Quest(name = quest_name, 
                user_posted_name = quser.user.username,
                description = description, city = city, 
                rating = rating, stats = stats)
            quest.save()
            quser.posted_quests.add(quest)
            quser.save()

# def generate_challenges(numChallenges):
#     for i in range(numChallenges):
#         random_first_name = first_names[random.randint(0, len(first_names) - 1)]
#         random_minor_loc = minor_locs[random.randint(0, len(minor_locs) - 1)]
#         location = random_first_name + "'s " + random_minor_loc
        
#         random_verb = verbs[random.randint(0, len(verbs) - 1)]
#         random_helper = helpers[random.randint(0, len(helpers) - 1)]
#         random_adjective = adjectives[random.randint(0, len(adjectives) - 1)]
#         random_noun = nouns[random.randint(0, len(nouns) - 1)]
#         description = (random_verb + ' ' + random_helper + ' ' + random_adjective + ' ' + random_noun)
        
#         def get_random_quest():
#             quests = Quest.objects.all()
#             random_quest = quests[random.randint(0, len(quests) - 1)]
#             return random_quest

#         quest = get_random_quest()
#         challenge = Challenge(quest=quest, description=description, location=location)
#         challenge.save()

def add_challenges(max_num_challenges):
    quests = Quest.objects.all()
    for quest in quests:
        num_challenges = random.randint(1, max_num_challenges)
        for i in range(num_challenges):
            random_first_name = first_names[random.randint(0, len(first_names) - 1)]
            random_minor_loc = minor_locs[random.randint(0, len(minor_locs) - 1)]
            location = random_first_name + "'s " + random_minor_loc
            
            random_verb = verbs[random.randint(0, len(verbs) - 1)]
            random_helper = helpers[random.randint(0, len(helpers) - 1)]
            random_adjective = adjectives[random.randint(0, len(adjectives) - 1)]
            random_noun = nouns[random.randint(0, len(nouns) - 1)]
            description = (random_verb + ' ' + random_helper + ' ' + random_adjective + ' ' + random_noun)

            challenge = Challenge(quest=quest, description=description, location=location)
            challenge.save()

def add_icons_to_users():
    filenames = os.listdir( 'media/random_images/')
    qusers = QUser.objects.all()
    for quser in qusers:
        random_file_name = choice(filenames)
        path = "media/random_images/" + random_file_name
        f = File(open(path, 'rb'))
        quser.icon.save(random_file_name, f)

def add_icons_to_quests():
    filenames = os.listdir('media/random_images')
    quests = Quest.objects.all()
    for quest in quests:
        random_file_name = choice(filenames)
        path = "media/random_images/" + random_file_name
        f = File(open(path, 'rb'))
        quest.icon.save(random_file_name, f)

def add_allies(max_num_allies):
    qusers = QUser.objects.all()
    for quser in qusers:
        num_allies = random.randint(0, max_num_allies)
        random_users = random.sample(qusers, num_allies)
        for ally in random_users:
            if ally not in quser.allies.all():
                quser.allies.add(ally)    

# def add_posted_quests():
#     qusers = QUser.objects.all()
#     quests = Quest.objects.all()
#     for quest in quests:
#         poster = quest.user_posted_name
#         user_posted = User.objects.get(username = poster)
#         quest.city = user_posted.quser.location
#         quest.save()
#         user_posted.quser.posted_quests.add(quest)

    # for quser in qusers:
    #     num_quests = random.randint(0, 6)
    #     random_quests = random.sample(quests, num_quests)
    #     for quest in random_quests:
    #         if quest not in quser.current_quests.all():
    #             quser.posted_quests.add(quest)

# def add_current_quests(max_num_current):
#     qusers = QUser.objects.all()
#     quests = Quest.objects.all()
#     for quser in qusers:
#         num_quests = random.randint(0, max_num_current)
#         random_quests = random.sample(quests, num_quests)
#         for quest in random_quests:
#             if quest not in quser.posted_quests.all():
#                 questing_relation = Questing(current_user = quser, 
#                     current_quest = quest)
#                 questing_relation.save()

def add_current_quests(max_num_current):
    qusers = QUser.objects.all()
    quests = Quest.objects.all()
    for quser in qusers:
        city = quser.location
        possible_quests = Quest.objects.filter(city = city)
        if max_num_current < len(possible_quests):
            num_quests = random.randint(0, max_num_current)
        else:
            num_quests = random.randint(0, len(possible_quests))
        random_quests = random.sample(possible_quests, num_quests)
        for quest in random_quests:
            if quest not in quser.posted_quests.all() and quest not in quser.current_quests.all() and quest not in quser.completed_quests.all():
                questing_relation = Questing(current_user = quser, 
                    current_quest = quest)
                questing_relation.save()

def add_completed_quests(max_num_completed):
    qusers = QUser.objects.all()
    quests = Quest.objects.all()
    for quser in qusers:
        city = quser.location
        possible_quests = Quest.objects.filter(city = city)
        if max_num_completed < len(possible_quests):
            num_quests = random.randint(0, max_num_completed)
        else:
            num_quests = random.randint(0, len(possible_quests))
        random_quests = random.sample(possible_quests, num_quests)
        for quest in random_quests:
            if (quest not in quser.current_quests.all()) and \
                 (quest not in quser.posted_quests.all()) and \
                  (quest not in quser.completed_quests.all()):
                completed_relation = Completed(completed_user = quser, 
                    completed_quest = quest)
                completed_relation.save()

# def add_completed_quests(max_num_completed):
#     qusers = QUser.objects.all()
#     quests = Quest.objects.all()
#     for quser in qusers:
#         num_quests = random.randint(0, max_num_completed)
#         random_quests = random.sample(quests, num_quests)
#         for quest in random_quests:
#             if (quest not in quser.current_quests.all()) and \
#                 (quest not in quser.posted_quests.all()):
#                 completed_relation = Completed(completed_user = quser,
#                     completed_quest = quest)
#                 completed_relation.save()

def add_certificates():
    filenames = os.listdir('media/random_images')
    qusers = QUser.objects.all()
    for quser in qusers:
        for quest in quser.completed_quests.all():
            for challenge in quest.challenge_set.all():
                random_file_name = choice(filenames)
                path = "media/random_images/" + random_file_name
                f = File(open(path, 'rb'))
                cc = ChallengeCertificate(challenge = challenge, 
                        user_submitted_name = quser.user.username,
                        ver_notes = 'So fun! Wow! Yay! Yippee!')
                cc.ver_photo.save(random_file_name, f)

def add_comments():
    qusers = QUser.objects.all()
    for quser in qusers:
        for ally in quser.allies.all():
            completed_quests = ally.completed_quests.all()
            num_quests = random.randint(0, len(completed_quests))
            random_quests = random.sample(completed_quests, num_quests)
            for quest in random_quests:
                ally_completed_relation = Completed.objects.filter(
                    completed_user = ally, completed_quest = quest)
                if (len(ally_completed_relation) > 0):
                    ally_completed_relation = ally_completed_relation[0]
                else:
                    continue
                temp_comment = Comment(poster = quser, 
                    quest = ally_completed_relation)
                temp_comment.save()
                temp_comment.comment = quser.user.username + " says " \
                    + "heyheyhey about " + quest.name
                temp_comment.save()

def fast_data_gen(num_users, max_num_posted, max_num_challenges,
                    max_num_allies, max_num_current, max_num_completed):
    generate_users(num_users)
    add_posted_quests(max_num_posted)
    add_challenges(max_num_challenges)
    add_icons_to_users()
    add_icons_to_quests()
    add_allies(max_num_allies)
    add_current_quests(max_num_current)
    add_completed_quests(max_num_completed)
    add_certificates()
    add_comments()

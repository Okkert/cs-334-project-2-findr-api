import findr.app.posts as posts
import findr.app.groups as groups
import findr.app.auth as auth
import findr.app.models as models


users = [

    {
        "username": "janeybaby",
        "email": "janeybaby@hotmail.com",
        "password": "JaneyS12345!",
        "bio": "I’m fun, flirty and barely thirty! Send a friend req if you’re keen for a good time 😘",
        "avatar": "placeholder/u020.PNG",
        "userId": 1
    },
    {
        "username": "dyl_the_man",
        "email": "dyltheman@gmail.com",
        "password": "DylTheMan123!",
        "bio": "Here for a good time, not a long time 🍻",
        "avatar": "placeholder/u013.PNG",
        "userId": 1
    },
    {
        "username": "sebastian",
        "email": "seb95@gmail.com",
        "password": "Seb95sPassword!",
        "bio": "Looking for love in this lonely world we live in.",
        "avatar": "placeholder/u001.PNG",
        "userId": 1
    },
    {
        "username": "greg_loves_guns",
        "email": "gregory1996@yahoo.com",
        "password": "GregLovesGuns96!",
        "bio": "All I want in life is a beer and a betty. Ask me about my guns 💪.",
        "avatar": "placeholder/u004.PNG",
        "userId": 1
    },
    {
        "username": "sandra_and_karl",
        "email": "SandraKarlOosthuizen@gmail.com",
        "password": "LookingForA3rd!",
        "bio": "We are a quiet, simple couple from the West Coast looking for a young open-minded friend with whom to enjoy an occasional glass of wine. Serious enquiries only, please.",
        "avatar": "placeholder/u017.PNG",
        "userId": 1
    },
    {
        "username": "nickyishere",
        "email": "nicolette12221@yahoo.com",
        "password": "Str0ngP4ssword?",
        "bio": "Dental hygienist. Just been through a breakup - trying something new! I love cooking, watching movies and gentle asphyxiation.",
        "avatar": "placeholder/u012.PNG",
        "userId": 1
    },
    {
        "username": "dwightschrute",
        "email": "dwightschrute@gmail.com",
        "password": "ItIsMyPassw0rd!",
        "bio": "Bear, beets, Battlestar Galactica.",
        "avatar": "placeholder/u018.PNG",
        "userId": 1
    },
    {
        "username": "the_only_jessica",
        "email": "jessdutoit5554@gmail.com",
        "password": "IL0veH4rryStyl3s!",
        "bio": "I’m new to the area and my friend told me about this app. I can’t wait to make new friends!",
        "avatar": "placeholder/u016.PNG",
        "userId": 1
    },
    {
        "username": "karen_loves_wine",
        "email": "karenschultz@gmail.com",
        "password": "P1notage4Life!",
        "bio": "Stay-at-home mom of 4. Anti-vaxxer, anti-masker, and I will speak to the manager. I love pilates, brunch, and of course, wiiiine!  🍷🍷🍷",
        "avatar": "placeholder/u002.PNG",
        "userId": 1
    },
    {
        "username": "dirkvandermerwe",
        "email": "dirkvandermerwe@gmail.com",
        "password": "DirkVanDerMerwe1?",
        "bio": "Hello there. My name is Dirk. Please forgive me if my English is not very good, it is not my first language. Please only instant-message me if you are young and blonde and enjoy Scrabble. Kind regards, Dirk.",
        "avatar": "placeholder/u011.PNG",
        "userId": 1
    },
    {
        "username": "angie",
        "email": "angelagordons@gmail.com",
        "password": "Angela0nFindr420!",
        "bio": "She/her 🏳️‍🌈 follow me on Tik Tok @angie420.",
        "avatar": "placeholder/u021.PNG",
        "userId": 1
    },
    {
        "username": "swingeon",
        "email": "swingeon@hotmail.com",
        "password": "Swingeon12345!",
        "bio": "Swinging my way downtown.",
        "avatar": "placeholder/u006.PNG",
        "userId": 1
    }
]

group_data = [
    {
        "name": "Jane’s Boy Toys",
        "private": True,
        "description": "Good boys share their toys 👠💋",
        "members": [users[1], users[2], users[3], users[11]],
        "creator": users[0],
        "groupId": 1
    },
    {
        "name": "Oosthuizen Friends ",
        "private": True,
        "description": "Sandra and Karl’s group. Serious requests only, please.",
        "members": [users[2], users[5], users[7]],
        "creator": users[4],
        "groupId": 1
    },
    {
        "name": "Bush Babies",
        "private": False,
        "description": "I like limes, bats and bush babies.",
        "members": [users[0], users[7], users[8], users[11]],
        "creator": users[9],
        "groupId": 1
    },
    {
        "name": "Karen’s Hot Tub Party",
        "private": False,
        "description": "I bought a hot tub with the money I made from selling my ex-husband’s motorbike. Let’s get steamy!",
        "members": [users[1], users[3], users[5], users[6], users[7]],
        "creator": users[8],
        "groupId": 1
    },
    {
        "name": "Melkbos Milfs",
        "private": True,
        "description": "Good vibes only #livelaughlove",
        "members": [users[0], users[5]],
        "creator": users[8],
        "groupId": 1
    },
    {
        "name": "Nature Lovers",
        "private": True,
        "description": "For those passionate about botany 🍁🍃",
        "members": [users[2], users[1], users[5]],
        "creator": users[10],
        "groupId": 1
    },
    {
        "name": "Boer Soek Boer",
        "private": True,
        "description": "Die manne.",
        "members": [users[1], users[2], users[6], users[9], users[11]],
        "creator": users[3],
        "groupId": 1
    },
    {
        "name": "Desperate Housewives of Constantia",
        "private": False,
        "description": "Wives that desperately need some company. ",
        "members": [users[0], users[5], users[7]],
        "creator": users[8],
        "groupId": 1
    },
    {
        "name": "Lonely Programmers",
        "private": False,
        "description": "It's just me and Vim, man. Just me and Vim.",
        "members": [users[9], users[6], users[10]],
        "creator": users[11],
        "groupId": 1
    },
    {
        "name": "Karen's Wine Group",
        "private": False,
        "description": "Red, white, sparkling, sweet...we love them all!",
        "members": [users[0], users[6], users[10], users[1]],
        "creator": users[8],
        "groupId": 1
    },
    {
        "name": "Clifton Daddies",
        "private": False,
        "description": "How about I buy you a nice purse, honey?",
        "members": [users[0], users[5], users[7], users[10]],
        "creator": users[8],
        "groupId": 1
    },
    {
        "name": "Local Singles in The Area",
        "private": False,
        "description": "Looking to mingle",
        "members": [users[6], users[1], users[2], users[11]],
        "creator": users[3],
        "groupId": 1
    },
    {
        "name": "Swingers of Stellenbosch",
        "private": False,
        "description": "Give me a golf club and watch me swing.",
        "members": [users[4], users[11]],
        "creator": users[3],
        "groupId": 1
    }
]

post_data = [
    {
        "groupId": group_data[0],
        "userId": users[0],
        "postId": 1,
        "title": "Hey boys!",
        "description": "How’s everyone doing after yesterday? You are all such troopers 💋",
        "location": "Sea Point",
        "category": "Just chatting",
        "liked_by": [users[0], users[3]],
        "comments": [
            {
                "comment_id": 1,
                "userId": users[1],
                "comment": "When can I come around to fetch my sweater?"
            },
            {
                "comment_id": 1,
                "userId": users[11],
                "comment": "Wait, did you meet up without me? :("
            }
        ]
    },
    {
        "postId": 1,
        "userId": users[8],
        "groupId": group_data[3],
        "title": "Plans for Saturday",
        "description": "Okay, just to confirm: I’ll see you all at my place on Saturday at 19:00. "
                       "Who’s bringing which snacks? I made hummus!",
        "location": "Melkbos",
        "category": "Hot tub",
        "liked_by": [users[1], users[3], users[7]],
        "comments": [
            {
                "comment_id": 1,
                "userId": users[6],
                "comment": "I’ll bring beets."
            },
            {
                "comment_id": 1,
                "userId": users[7],
                "comment": "Ooh! I can bring baby carrots and gluten-free crackers (I saw a recipe on Pinterest)"
            },
            {
                "comment_id": 1,
                "userId": users[5],
                "comment": "Finger snacks in a hot tub? Is that really the best idea…?"
            }
        ]
    },
    {
        "postId": 1,
        "userId": users[4],
        "groupId": group_data[1],
        "title": "Meet and greet",
        "description": "Hello all from Sandra and Karl. We are hosting a games evening next Thursday evening. "
                       "There will be UNO and Monopoly (the Star Wars edition; it’s Karl’s favourite). "
                       "We would love for you all to join us so that we can get to know each one of you. "
                       "Please let us know before Tuesday if you will be attending so that Sandra can buy enough "
                       "ingredients for the bobotie. We are very excited to meet you lovely people.",
        "location": "Durbanville",
        "category": "Social",
        "liked_by": [users[7]],
        "comments": [
            {
                "comment_id": 1,
                "userId": users[7],
                "comment": "I love UNO!"
            }
        ]
    },
    {
        "postId": 1,
        "userId": users[7],
        "groupId": group_data[2],
        "title": "What is going on?",
        "description": "I think I accidentally joined this group. What even is a bush baby? "
                       "Can the admin please remove me?",
        "location": "Sea Point",
        "category": "Other",
        "liked_by": [],
        "comments": [
            {
                "comment_id": 1,
                "userId": users[11],
                "comment": "Hey, man. Just hang around. I think you’ll like it here."
            }
        ]
    },
    {
        "postId": 1,
        "userId": users[8],
        "groupId": group_data[4],
        "title": "Anti-mask protest",
        "description": "Who’s going to the Milnerton anti-mask protest on Wednesday morning? Last week there was quite "
                       "a turn-out (great opportunity to meet men who have their heads screwed on right!). "
                       "We can hang out at my place afterwards, I’ve got some cab-sav I’ve been dying to open!",
        "location": "Milnerton",
        "category": "Looking for connections",
        "liked_by": [users[0]],
        "comments": [
            {
                "comment_id": 1,
                "userId": users[0],
                "comment": "I’ll be there. gurl!"
            },
            {
                "comment_id": 1,
                "userId": users[5],
                "comment": "… Please remove me from this group"
            }
        ]
    },
    {
        "postId": 1,
        "userId": users[2],
        "groupId": group_data[5],
        "title": "Botany. right?",
        "description": "I have a slight suspicion that this group may not be what I expected… Can anyone direct me to "
                       "a group that could help me take care of my succulents?",
        "location": "Stellenbosch",
        "category": "Recommendation",
        "liked_by": [],
        "comments": []
    },
    {
        "postId": 1,
        "userId": users[11],
        "groupId": group_data[2],
        "title": "Happy birthday to me",
        "description": "Why did no one show up to my Spur birthday? I ordered a special cake.",
        "location": "Stellenbosch",
        "category": "Lego",
        "liked_by": [],
        "comments": []
    },
    {
        "postId": 1,
        "userId": users[9],
        "groupId": group_data[6],
        "title": "AI Partner Idea",
        "location": "Durbanville",
        "category": "Other",
        "liked_by": [],
        "description":"What if we made an AI partner for this group? So far I've got a discord bot that laughs at my jokes "
                      "when I tell it to. Their profile pic is pretty hot too.",
        "comments": [
            {
                "comment_id": 1,
                "userId": users[6],
                "comment": "Love the idea. Love the enthusiasm. Shall we do it in C?"
            }
        ]
    },
    {
        "postId": 1,
        "userId": users[2],
        "groupId": group_data[1],
        "title": "Very important! Don't miss it! Discount!",
        "location": "Melkbos",
        "category": "Lego",
        "liked_by": [],
        "description":"Join LEGO.com today and use discount code bugged_team_bob for 1.2% discount on your first purchase!",
        "comments": [
            {
                "comment_id": 1,
                "userId": users[0],
                "comment": "Lego is life"
            }
        ]
    },
    {
        "postId": 1,
        "userId": users[8],
        "groupId": group_data[2],
        "title": "Where are the bush babies?",
        "location": "Durbanville",
        "category": "Other",
        "liked_by": [],
        "description":"I thought this was an exotic animal trade group. ",
        "comments": [
            {
                "comment_id": 1,
                "userId": users[0],
                "comment": "We are the exotic animals Karen, get with it."
            }
        ]

    },
    {
        "postId": 1,
        "userId": users[1],
        "groupId": group_data[11],
        "title": "Single and ready to mingle",
        "location": "Stellenbosch",
        "category": "Other",
        "liked_by": [],
        "description":"Hey guys just thought I would update you to let you know I'm leaving my wife Susan.",
        "comments": [
            {
                "comment_id": 1,
                "userId": users[1],
                "comment": "I'm here for you sweety 😘"
            }
        ]
    },
    {
        "postId": 1,
        "userId": users[8],
        "groupId": group_data[9],
        "title": "Craving some wine",
        "location": "Paarl",
        "category": "Social",
        "liked_by": [],
        "description":"The kids say that I drink too much wine. How would they know?! 🙄 How else am I suppose to make it through Jenny's netball match...",
        "comments": [
            {
                "comment_id": 1,
                "userId": users[0],
                "comment": "#KarenLovesWine"
            }
        ]
    },
    {
        "postId": 1,
        "userId": users[6],
        "groupId": group_data[8],
        "title": "Anyone looking to c++ and chill?",
        "location": "Paarl",
        "category": "Social",
        "liked_by": [],
        "description":"Please let me know asap",
        "comments": [
            {
                "comment_id": 1,
                "userId": users[11],
                "comment": "Only if I get the keyboard this time"
            }
        ]
    }
]


def populate_database():
    for user in users:
        auth.register(user["username"], user["email"], user["password"])
        u = models.search_user_by_username(user["username"])
        print(u)
        print(u.user_id)
        user["userId"] = u.user_id
        models.update_userBio(user["userId"], user["bio"])
        models.update_userAvatar(user["userId"], f"https://storage.googleapis.com/findr-316018_bucket/{user['avatar']}")

    for group in group_data:
        group_details = {
            "title": group["name"],
            "desc": group["description"],
            "private": group["private"],
        }
        creator = group["creator"]
        user_id = creator["userId"]
        groups.create_group(group=group_details, user_id=user_id)

        g = models.search_group_by_name(group["name"])
        group["groupId"] = g.group_id
        members = group["members"]
        for member in members:
            groups.join_group(member["userId"], group["groupId"])

    print(users)

    for post in post_data:

        group = post["groupId"]
        author = post["userId"]

        post_detail = {
            "groupId": group["groupId"],
            "author": {
                "userId": author["userId"],
            },
            "title": post["title"],
            "postContent": post["description"],
            "location": post["location"],
            "category": post["category"]
        }
        posts.create_post(post=post_detail)
        p = models.get_post(group_id=group["groupId"], user_id=author["userId"], post_title=post["title"])
        post["postId"] = p.post_id

        likes = post["liked_by"]
        for like in likes:
            posts.like_post(post_id=post["postId"], user_id=like["userId"])

        for comment in post["comments"]:
            post_id = post["postId"]
            user = comment["userId"]
            content = comment["comment"]
            models.insert_comment(post_id=post_id, user_id=user["userId"], comment_content=content)


populate_database()


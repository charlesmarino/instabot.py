#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback

sys.path.append(os.path.join(sys.path[0], 'src'))

from check_status import check_status
from feed_scanner import feed_scanner
from follow_protocol import follow_protocol
from instabot import InstaBot
from unfollow_protocol import unfollow_protocol
from send import send_mail


def run_bot():
    bot = InstaBot(
        login=os.environ['INSTAGRAM_USERNAME'],
        password=os.environ['INSTAGRAM_PASSWORD'],
        like_per_day=400,
        media_max_like=0,
        media_min_like=5,
        follow_per_day=1,
        follow_time=5*60*60,
        unfollow_per_day=1,
        comments_per_day=0,
        comment_list=[["this", "the", "your"],
                        ["photo", "picture", "pic", "shot", "snapshot"],
                        ["is", "looks", "feels", "is really"],
                        ["great", "super", "good", "very good", "good",
                        "wow", "WOW", "cool", "GREAT","magnificent",
                        "magical", "very cool", "stylish", "beautiful",
                        "so beautiful", "so stylish",
                        "so professional","lovely", "so lovely",
                        "very lovely", "glorious","so glorious",
                        "very glorious", "adorable", "excellent",
                        "amazing"], [".", "..", "...", "!","!!",
                                    "!!!"]],
        tag_list=['dog','bitcoin', 'cryptocurrency', 'newyork', 'eastvillage', 'eth'],
        tag_blacklist=['ico'],
        user_blacklist={'hellokitty':'', 'hellokitty3':''},
        max_like_for_one_tag = 5,
        unfollow_break_min = 15,
        unfollow_break_max = 30,
        log_mod = 0,
        proxy=''
    )

    #print("# MODE 0 = ORIGINAL MODE BY LEVPASHA")
    #print("## MODE 1 = MODIFIED MODE BY KEMONG")
    #print("### MODE 2 = ORIGINAL MODE + UNFOLLOW WHO DON'T FOLLOW BACK")
    #print("#### MODE 3 = MODIFIED MODE : UNFOLLOW USERS WHO DON'T FOLLOW YOU BASED ON RECENT FEED")
    #print("##### MODE 4 = MODIFIED MODE : FOLLOW USERS BASED ON RECENT FEED ONLY")
    #print("###### MODE 5 = MODIFIED MODE : JUST UNFOLLOW EVERYBODY, EITHER YOUR FOLLOWER OR NOT")

    ################################
    ##  WARNING   ###
    ################################

    # DON'T USE MODE 5 FOR A LONG PERIOD. YOU RISK YOUR ACCOUNT FROM GETTING BANNED
    ## USE MODE 5 IN BURST MODE, USE IT TO UNFOLLOW PEOPLE AS MANY AS YOU WANT IN SHORT TIME PERIOD

    mode = 0 

    #print("You choose mode : %i" %(mode))
    #print("CTRL + C to cancel this operation or wait 30 seconds to start")
    #time.sleep(30)

    if mode == 0:
        bot.auto_mod()

    elif mode == 1:
        check_status(bot)
        while bot.self_following - bot.self_follower > 200:
            unfollow_protocol(bot)
            time.sleep(10 * 60)
            check_status(bot)
        while bot.self_following - bot.self_follower < 400:
            while len(bot.user_info_list) < 50:
                feed_scanner(bot)
                time.sleep(5 * 60)
                follow_protocol(bot)
                time.sleep(10 * 60)
                check_status(bot)

    elif mode == 2:
        bot.bot_mode = 1
        bot.new_auto_mod()

    elif mode == 3:
        unfollow_protocol(bot)
        time.sleep(10 * 60)

    elif mode == 4:
        feed_scanner(bot)
        time.sleep(60)
        follow_protocol(bot)
        time.sleep(10 * 60)

    elif mode == 5:
        bot.bot_mode = 2
        unfollow_protocol(bot)

    else:
        print("Wrong mode!")


if __name__ == '__main__':
    while True:
       try:
           run_bot()
       except:
           traceback.print_exc()
           send_mail('[Instabot] Exception occured', traceback.format_exc())


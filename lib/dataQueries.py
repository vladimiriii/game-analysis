# -*- coding: utf-8 -*-
import pandas as pd
import os, shutil
import json
from datetime import datetime, date, timedelta
from flask import session

from app.lib.models import Base, events, db_session

###############################################
# Functions                                   #
###############################################
def installs_check():

    # Create query
    query = ('''
            SELECT userid
                ,COUNT(row) AS records
            FROM events
            WHERE eventname = 'newPlayer'
            GROUP BY userid
            HAVING COUNT(row) > 1
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()
    print(df)

def installs_by_day():

    # Create query
    query = ('''
            SELECT COUNT(*) AS rows
                ,"eventDate"
                ,device
            FROM events
            WHERE eventname = 'newPlayer'
            GROUP BY "eventDate", device
            ORDER BY device, "eventDate" ASC
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/installs.csv')

def installs_by_country():

    # Create query
    query = ('''
            SELECT COUNT(*) AS rows
                ,usercountry
            FROM events
            WHERE eventname = 'newPlayer'
            GROUP BY usercountry
            ORDER BY rows DESC
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/installs_by_country.csv')

def installs_by_device():

    # Create query
    query = ('''
            SELECT COUNT(*) AS rows
                ,device
            FROM events
            WHERE eventname = 'newPlayer'
            GROUP BY device
            ORDER BY rows DESC
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/installs_by_device.csv')

def dau_count():

    # Create query
    query = ('''
            SELECT COUNT(DISTINCT userid) AS users
                ,"eventDate"
                ,device
            FROM events
            GROUP BY "eventDate", device
            ORDER BY device, "eventDate" ASC
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/daily_active_users.csv')

def mau_count():

    # Create query
    query = ('''
            SELECT COUNT(DISTINCT userid) AS users
            FROM events
            WHERE "eventDate" BETWEEN '2006-02-01' AND '2006-02-28'
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/monthly_active_users.csv')

def mau_by_device():

    # Create query
    query = ('''
            SELECT COUNT(DISTINCT userid) AS users
                ,device
            FROM events
            WHERE "eventDate" BETWEEN '2006-02-01' AND '2006-02-28'
            GROUP BY device
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/mau_by_device.csv')

def level_stats():

    # Create query
    query = ('''
            SELECT s."levelNumber"
                ,s.starts
                ,f.fails
                ,c.completes
                ,a.abandons
            FROM (
                SELECT "levelNumber"
                    ,COUNT(row) AS starts
                FROM events
                WHERE eventname = 'missionStarted'
                AND "versionName" = '1.1.0'
                GROUP BY "levelNumber"
            ) AS s
            LEFT OUTER JOIN (
                SELECT "levelNumber"
                    ,COUNT(row) AS fails
                FROM events
                WHERE eventname = 'missionFailed'
                AND "versionName" = '1.1.0'
                GROUP BY "levelNumber"
            ) AS f
            ON s."levelNumber" = f."levelNumber"
            LEFT OUTER JOIN (
                SELECT "levelNumber"
                    ,COUNT(row) AS completes
                FROM events
                WHERE eventname = 'missionCompleted'
                AND "versionName" = '1.1.0'
                GROUP BY "levelNumber"
            ) AS c
            ON s."levelNumber" = c."levelNumber"
            LEFT OUTER JOIN (
                SELECT "levelNumber"
                    ,COUNT(row) AS abandons
                FROM events
                WHERE eventname = 'missionAbandoned'
                AND "versionName" = '1.1.0'
                GROUP BY "levelNumber"
            ) AS a
            ON s."levelNumber" = a."levelNumber"
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/level_stats_110.csv')

def level_users():

    # Create query
    query = ('''
            SELECT "levelNumber"
                ,COUNT(DISTINCT userid) AS users
            FROM events
            WHERE eventname = 'missionStarted'
            GROUP BY "levelNumber"
            ORDER BY "levelNumber"
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/level_users.csv')

def daily_rounds():

    # Create query
    query = ('''
            SELECT edate
                ,device
                ,SUM(rows) AS games
                ,COUNT(user) AS users
            FROM (SELECT "eventDate" AS edate
                    ,device
                    ,userid AS user
                    ,COUNT(row) AS rows
                FROM events
                WHERE eventname = 'gameStarted'
                GROUP BY "eventDate", device, userid
                ) AS g
            GROUP BY device, edate
            ORDER BY device, edate
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/daily_rounds.csv')

def day_N_retention():

    # Create query
    query = ('''
            SELECT day_zero
                ,COUNT(a.userid) AS day_zero_users
                ,COUNT(b.userid) AS day_one_users
                ,COUNT(c.userid) AS day_seven_users
                ,COUNT(d.userid) AS day_fourteen_users
                ,COUNT(e.userid) AS day_twentyone_users
                ,COUNT(f.userid) AS day_twentyeight_users
            FROM (
                SELECT "eventDate" AS day_zero
                    ,userid
                FROM events
                WHERE eventname = 'newPlayer'
                GROUP BY day_zero, userid
                ) AS a
            LEFT OUTER JOIN (
                SELECT userid
                    ,"eventDate" - INTERVAL '1 day' AS day_one
                FROM events
                WHERE eventname = 'gameStarted'
                GROUP BY day_one, userid
                ) AS b
            ON a.day_zero = b.day_one
            AND a.userid = b.userid
            LEFT OUTER JOIN (
                SELECT userid
                    ,"eventDate" - INTERVAL '7 days' AS day_seven
                FROM events
                WHERE eventname = 'gameStarted'
                GROUP BY day_seven, userid
                ) AS c
            ON a.day_zero = c.day_seven
            AND a.userid = c.userid
            LEFT OUTER JOIN (
                SELECT userid
                    ,"eventDate" - INTERVAL '14 days' AS day_fourteen
                FROM events
                WHERE eventname = 'gameStarted'
                GROUP BY day_fourteen, userid
                ) AS d
            ON a.day_zero = d.day_fourteen
            AND a.userid = d.userid
            LEFT OUTER JOIN (
                SELECT userid
                    ,"eventDate" - INTERVAL '21 days' AS day_twentyone
                FROM events
                WHERE eventname = 'gameStarted'
                GROUP BY day_twentyone, userid
                ) AS e
            ON a.day_zero = e.day_twentyone
            AND a.userid = e.userid
            LEFT OUTER JOIN (
                SELECT userid
                    ,"eventDate" - INTERVAL '28 days' AS day_twentyeight
                FROM events
                WHERE eventname = 'gameStarted'
                GROUP BY day_twentyeight, userid
                ) AS f
            ON a.day_zero = f.day_twentyeight
            AND a.userid = f.userid
            GROUP BY day_zero
            ORDER BY day_zero
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/day_n_retention.csv')

def version_dates():

    # Create query
    query = ('''
            SELECT "versionName"
                ,MIN("eventDate") AS earliest_date
                ,MAX("eventDate") AS latest_date
            FROM events
            WHERE eventname = 'gameStarted'
            GROUP BY "versionName"
            ORDER BY "versionName"
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/version_dates.csv')

def campaign_info():

    # Create query
    query = ('''
            SELECT "campaignId"
                ,eventname
                ,COUNT(row) AS events
                ,MIN("eventDate") AS earliest_date
                ,MAX("eventDate") AS latest_date
            FROM events
            WHERE "campaignId" IS NOT NULL
            GROUP BY "campaignId", eventname
            ORDER BY "campaignId", eventname
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/campaign_info.csv')

def campaign_check():

    # Create query
    query = ('''
            SELECT userid
                ,COUNT(row) AS records
            FROM events
            WHERE "campaignId" IS NOT NULL
            GROUP BY userid
            HAVING COUNT(row) > 1
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()
    print(df)

def country_check():

    # Create query
    query = ('''
            SELECT userid
                ,COUNT(event_count)
            FROM (
                SELECT userid
                    ,COUNT(row) AS event_count
                    ,usercountry
                FROM events
                GROUP BY userid, usercountry
            ) AS a
            GROUP BY userid
            HAVING COUNT(event_count) > 1
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()
    print(df)

def day_N_retention_by_device(device):

    # Create query
    query = ("""
            SELECT day_zero
                ,COUNT(a.userid) AS day_zero_users
                ,COUNT(b.userid) AS day_one_users
                ,COUNT(c.userid) AS day_seven_users
                ,COUNT(d.userid) AS day_fourteen_users
                ,COUNT(e.userid) AS day_twentyone_users
                ,COUNT(f.userid) AS day_twentyeight_users
            FROM (
                SELECT "eventDate" AS day_zero
                    ,userid
                FROM events
                WHERE eventname = 'gameStarted'
                AND device = '""" + device + """'
                GROUP BY day_zero, userid
                ) AS a
            LEFT OUTER JOIN (
                SELECT userid
                    ,"eventDate" - INTERVAL '1 day' AS day_one
                FROM events
                WHERE eventname = 'gameStarted'
                AND device = '""" + device + """'
                GROUP BY day_one, userid
                ) AS b
            ON a.day_zero = b.day_one
            AND a.userid = b.userid
            LEFT OUTER JOIN (
                SELECT userid
                    ,"eventDate" - INTERVAL '7 days' AS day_seven
                FROM events
                WHERE eventname = 'gameStarted'
                AND device = '""" + device + """'
                GROUP BY day_seven, userid
                ) AS c
            ON a.day_zero = c.day_seven
            AND a.userid = c.userid
            LEFT OUTER JOIN (
                SELECT userid
                    ,"eventDate" - INTERVAL '14 days' AS day_fourteen
                FROM events
                WHERE eventname = 'gameStarted'
                AND device = '""" + device + """'
                GROUP BY day_fourteen, userid
                ) AS d
            ON a.day_zero = d.day_fourteen
            AND a.userid = d.userid
            LEFT OUTER JOIN (
                SELECT userid
                    ,"eventDate" - INTERVAL '21 days' AS day_twentyone
                FROM events
                WHERE eventname = 'gameStarted'
                AND device = '""" + device + """'
                GROUP BY day_twentyone, userid
                ) AS e
            ON a.day_zero = e.day_twentyone
            AND a.userid = e.userid
            LEFT OUTER JOIN (
                SELECT userid
                    ,"eventDate" - INTERVAL '28 days' AS day_twentyeight
                FROM events
                WHERE eventname = 'gameStarted'
                AND device = '""" + device + """'
                GROUP BY day_twentyeight, userid
                ) AS f
            ON a.day_zero = f.day_twentyeight
            AND a.userid = f.userid
            GROUP BY day_zero
            ORDER BY day_zero
            ;""")
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/day_n_retention_' + device + '.csv')

def more_than_a_day():

    # Create query
    query = ('''
            SELECT  COUNT(c.userid) AS one_time_users
                ,COUNT(a.userid) AS all_users
                ,a."eventDate"
                ,a.device
            FROM  (
                SELECT userid
                    ,"eventDate"
                    ,device
                FROM events
                GROUP BY userid, "eventDate", device
            ) AS a
            LEFT OUTER JOIN (
                SELECT userid
                    ,COUNT("eventDate") AS dates
                FROM (
                    SELECT userid
                        ,"eventDate"
                    FROM events
                    GROUP BY userid, "eventDate"
                    ) AS b
                GROUP BY b.userid
                HAVING COUNT("eventDate") = 1
                ) AS c
            ON a.userid = c.userid
            GROUP BY a."eventDate", device
            ORDER BY a."eventDate"
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/more_than_a_day.csv')

def totalPurchases():

    # Create query
    query = ('''
            SELECT COUNT(userid)
                ,AVG(revenue)
                ,percentile_disc(0.5) WITHIN GROUP (ORDER BY revenue)
            FROM (
                SELECT userid
                    ,SUM(to_number(amount, '9999')) AS revenue
                FROM events
                WHERE eventname = 'itemPurchased'
                GROUP BY userid
                ) AS a
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()
    print(df)
    # df.to_csv('./static/data/public/raw_data/totalPurchases.csv')

def purchasesOverTime():

    # Create query
    query = ('''
            SELECT item
                ,"eventDate"
                ,SUM(to_number(amount, '9999'))
            FROM events
            WHERE eventname = 'itemPurchased'
            GROUP BY item, "eventDate"
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/purchasesOverTime.csv')

def payingUsers():

    # Create query
    query = ('''
            SELECT COUNT(DISTINCT userid)
                ,"eventDate"
            FROM events
            WHERE eventname = 'itemPurchased'
            GROUP BY "eventDate"
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/payingUsers.csv')

def revenueByCountry():

    # Create query
    query = ('''
            SELECT SUM(to_number(amount, '9999'))
                ,usercountry
            FROM events
            WHERE eventname = 'itemPurchased'
            GROUP BY usercountry
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/revenueByCountry.csv')

def revenueByDevice():

    # Create query
    query = ('''
            SELECT SUM(to_number(amount, '9999'))
                ,device
            FROM events
            WHERE eventname = 'itemPurchased'
            GROUP BY device
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/revenueByDevice.csv')

def topLevelsWhenPurchasing():

    # Create query
    query = ('''
            SELECT COUNT(DISTINCT m.userid) AS Users
                ,m.last_level
            FROM (
                SELECT fp.userid
                    ,MAX(to_number("levelNumber", '9999')) OVER (
                    PARTITION BY
                    fp.userid
                    ) AS last_level
                FROM (  SELECT a.userid,
                            a.first_purchase
                        FROM (
                            SELECT userid
                                ,MIN("eventTimestamp") OVER (
                                PARTITION BY
                                userid
                                ) AS first_purchase
                            FROM events
                            WHERE eventname = 'itemPurchased'
                            ) AS a
                        GROUP BY a.userid, a.first_purchase
                    ) AS fp
                LEFT OUTER JOIN (
                    SELECT userid
                        ,"levelNumber"
                        ,"eventTimestamp"
                    FROM events
                    WHERE "levelNumber" IS NOT NULL
                    AND eventname = 'missionStarted'
                ) AS al
                ON fp.userid = al.userid
                AND fp.first_purchase > al."eventTimestamp"
            ) AS m
            GROUP BY m.last_level
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/levelPurchases.csv')

def userSpendingTypes():

    # Create query
    query = ('''
            SELECT cat.category
                ,cat.device
                ,COUNT(cat.userid) AS Users
                ,SUM(cat.total_spend) AS Revenue
            FROM (
                SELECT CASE WHEN sums.total_spend = 1 THEN '1 purchase'
                    WHEN sums.total_spend BETWEEN 2 AND 3 THEN '2-3 Purchases'
                    WHEN sums.total_spend BETWEEN 4 AND 5 THEN '4-5 Purchases'
                    WHEN sums.total_spend BETWEEN 6 AND 7 THEN '6-7 Purchases'
                    WHEN sums.total_spend BETWEEN 8 AND 9 THEN '8-9 Purchases'
                    ELSE '10+ Purchases'
                    END AS category
                    ,sums.device
                    ,sums.userid
                    ,sums.total_spend
                    FROM (
                        SELECT SUM(to_number(amount, '9999')) AS total_spend
                            ,userid
                            ,device
                        FROM events
                        WHERE eventname = 'itemPurchased'
                        GROUP BY userid, device
                    ) as sums
                ) cat
            GROUP BY category, device
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/userSpendingTypes.csv')

def coinEconomy():

    # Create query
    query = ('''
            SELECT SUM(used) AS coins_used
                ,SUM(received) AS coins_received
                ,"eventDate"
            FROM (
                SELECT "eventDate"
                    ,CASE WHEN eventname = 'coinsUsed' THEN to_number(amount, '9999999') ELSE 0 END AS used
                    ,CASE WHEN eventname = 'coinsReceived' THEN to_number(amount, '9999999') ELSE 0 END AS received
                FROM events
                WHERE eventname = 'coinsUsed'
                OR eventname = 'coinsReceived'
                ) AS a
            GROUP BY "eventDate"
            ORDER BY "eventDate"
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/coinEconomy.csv')

def campaignRevenue():

    # Create query
    query = ('''
            SELECT cid."campaignId"
                ,rev.usercountry
                ,rev.device
                ,COUNT(rev.userid)
                ,SUM(rev.revenue)
            FROM (
                SELECT userid
                    ,usercountry
                    ,device
                    ,SUM(CASE WHEN eventname = 'itemPurchased' THEN to_number(amount, '9999999') ELSE 0 END) AS revenue
                FROM events
                GROUP BY userid, usercountry, device
                ) AS rev
            LEFT JOIN (
                SELECT userid
                    ,"campaignId"
                FROM events
                GROUP BY userid, "campaignId"
                ) AS cid
            ON cid.userid = rev.userid
            GROUP BY cid."campaignId", rev.usercountry, rev.device
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    df.to_csv('./static/data/public/raw_data/campaignRevenue.csv')

def campaignCheck():

    # Create query
    query = ('''
            SELECT COUNT(DISTINCT userid)
            FROM events
            WHERE userid NOT IN (
                SELECT DISTINCT userid
                FROM events
                WHERE "campaignId" IS NOT NULL
                )
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()
    print(df)

def individualCampaignUsers():

    # Create query
    query = ('''
            SELECT a.userid
                ,SUM(to_number(amount, '9999999')) AS revenue
            FROM events AS a
            INNER JOIN (
                SELECT DISTINCT userid
                FROM events
                WHERE "campaignId" = '9s5vVew1HvRvFU+l8FHarl/rh1WBtudlUUe+K5CuudM='
            ) b
            ON a.userid = b.userid
            WHERE eventname = 'itemPurchased'
            GROUP BY a.userid
            ORDER BY revenue DESC
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()
    print(df)

def timeOnLevel():

    # Create query
    print('Querying database...')
    query = ('''
            SELECT userid
                ,"levelNumber" AS level
                ,eventname
                ,"eventTimestamp" AS etime
            FROM events
            WHERE eventname = 'missionStarted'
            OR eventname = 'missionCompleted'
            ORDER BY userid, level, etime
            ;''')
    query_results = db_session.execute(query)

    # Process Results
    print('Extracting results...')
    df = pd.DataFrame(query_results.fetchall())
    df.columns = query_results.keys()

    # Loop through with
    print('Processing data...')
    times = {}
    for index, row in df.iterrows():
        if int(index) % 1000000 == 0:
            print(str(index) + " rows processed...")

        cur_row = index
        next_row = index + 1

        try:
            next_event = df.at[next_row, 'eventname']
            if row['eventname'] == 'missionStarted' and next_event == 'missionCompleted':
                next_lvl = df.at[next_row, 'level']
                next_userid = df.at[next_row, 'userid']
                complete_time = df.at[next_row, 'etime']
                if row['userid'] == next_userid and row['level'] == next_lvl:
                    if row['level'] not in times:
                        times[row['level']] = []
                    time_diff = (complete_time - row['etime']).total_seconds()
                    times[row['level']].append(time_diff)
        except:
            break

    # Consolidate results
    print("Consolidating results...")
    first_loop = True
    for key in times:
        row = pd.DataFrame([[int(key), len(times[key]), (sum(times[key]) / len(times[key]))]], columns=['Level', 'Completions', 'Average Completion Time'])
        if first_loop:
            first_loop = False
            results_df = row
        else:
            results_df = results_df.append(row)

    # Sort and Reindex
    results_df.sort_values('Level', axis=0, ascending=True, inplace=True)
    results_df.reset_index(drop=True, inplace=True)
    # print(results_df)

    # Convert to CSV
    print("Coverting to CSV...")
    results_df.to_csv('./static/data/public/raw_data/completionTimes.csv')


#--------------------------------------------
# Run Functions
#--------------------------------------------

# installs_check()
# installs_by_day()
# installs_by_country()
# installs_by_device()
# dau_count()
# mau_count()
# mau_by_device()
# level_stats()
# level_users()
# daily_rounds()
# day_N_retention()
# day_N_retention_by_device('ANDROID')
# version_dates()
# campaign_info()
# campaign_check()
# country_check()
# more_than_a_day()
# totalPurchases()
# purchasesOverTime()
# payingUsers()
# revenueByCountry()
# revenueByDevice()
# topLevelsWhenPurchasing()
# userSpendingTypes()
# coinEconomy()
# campaignRevenue()
# campaignCheck()
# individualCampaignUsers()
# timeOnLevel()

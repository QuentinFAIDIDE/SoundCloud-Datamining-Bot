################################################################################
#IMPORTS
import soundcloud
import sys
import operator
from math import sqrt
################################################################################

################################################################################
#REGISTERING APP
def register():
    client = soundcloud.Client(client_id='47b5a3d7a326382120d95d8c663b47f7')
    return client
################################################################################

################################################################################
def searchForUser(client, name):
    container = client.get('/users', q=name)
    return container[0]
################################################################################

################################################################################
def extractProfile(client, user, shortversion = False, custom_profile=None, tracklimit=250):
    end_page = False
    failcount = 0
    if custom_profile != None:
        profile = custom_profile
        len_beg = len(profile)
    else:
        profile = {}
        len_beg = 0
    likes_href = ('users/' + str(user.id) + '/favorites' )
    #likes_href = ('stop')
    comments_href = ('users/' + str(user.id) + '/comments' )
    #comments_href = ('stop' )
    playlists_href = ('users/' + str(user.id) + '/playlists' )
    reposted_done = False
    end_playlist = False
    print("Profiling " + user.username)

    while(not end_page):
        #querying all data
        if likes_href != 'stop':
            while True:
                try:
                    likes = client.get( likes_href , limit=100, linked_partitioning=1 )
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    continue
                break
            if hasattr(likes, 'next_href'):
                likes_href = likes.next_href
            else:
                likes_href = 'stop'

        if comments_href != 'stop':
            while True:
                try:
                    comments = client.get( comments_href , limit=100, linked_partitioning=1 )
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    continue
                break
            if hasattr(comments, 'next_href'):
                comments_href = comments.next_href
            else:
                comments_href = 'stop'

        if playlists_href != 'stop':
            while True:
                try:
                    playlists = client.get(playlists_href , limit=100, linked_partitioning=1 )
                    failcount = 0
                except:
                    failcount += 1
                    if failcount >5:
                        end_playlist = True
                        playlists_href = 'stop'
                        break
                    continue
                break
            if hasattr(playlists, 'next_href'):
                playlists_href = playlists.next_href
            else:
                playlists_href = 'stop'

        if not reposted_done:
            while True:
                try:
                    reposts = client.get((
                                'https://api-v2.soundcloud.com/profile/soundcloud:users:'
                                + str(user.id) + '?limit=100'))
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    continue
                break


        if(reposted_done and likes_href == 'stop' and playlists_href == 'stop' and comments_href == 'stop'):
            end_page = True



        #processing playlists to extract tracks who are not from user
        if end_page == False and playlists_href != 'stop' :
            for playlist in playlists.collection:
                for track in playlist.tracks:
                    if track['user_id'] != user.id:
                        if user.username.lower() not in track['title'].lower():
                            if profile.has_key(str(track['id'])):
                                profile[str(track['id'])] += 2
                            else:
                                profile[str(track['id'])] = 2

        #processing all reposts to extract tracks who are not from user
        if (not reposted_done) and end_page == False:
            for tracks in reposts.collection:
                if hasattr(tracks, 'track'):
                    if user.username.lower() not in tracks.track['title'].lower():
                        if profile.has_key(str(tracks.track['id'])):
                            profile[str(tracks.track['id'])] += 1
                        else:
                            profile[str(tracks.track['id'])] = 1
            reposted_done = True

        #processing all comments to get the tracks user commented
        #checking as always if they are not from him
        if comments_href != 'stop' and end_page == False:
            for comment in comments.collection:
                if profile.has_key(str(comment.track_id)):
                    profile[str(comment.track_id)] += 1
                else:
                    profile[str(comment.track_id)] = 1

        #processing all likes to extract tracks who are not from user
        if end_page == False and likes_href != 'stop':
                for tracks in likes.collection:
                    if user.username.lower() not in tracks.title.lower():
                        if profile.has_key(str(tracks.id)):
                            profile[str(tracks.id)] += 1
                        else:
                            profile[str(tracks.id)] = 1
        if (len(profile))>200 and shortversion==True: end_page = True

    #returning taste profile
    return profile
################################################################################

################################################################################
#PEARSON CORRELATION SCORE
#compare correlation between p1 and p2 critics and ignore grade inflation
def compare(p1, p2):
    si={}
    for item in p1:
        if item in p2: si[item]=1

    n=len(si)
    print(n)
    if n==0: return 0

    sum1=sum([p1[it] for it in si])
    sum2=sum([p2[it] for it in si])

    sum1Sq=sum([pow(p1[it],2) for it in si])
    sum2Sq=sum([pow(p2[it],2) for it in si])

    pSum=sum([p1[it]*p2[it] for it in si])

    #Pearson score computation
    covariance=pSum-(sum1*sum2/n)
    stdDev=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if stdDev==0: return 0
    r=covariance/stdDev

    return r
################################################################################

################################################################################
#Better never use this one (inneficient and long)
def profileFollowings(client, user, sorted=False):
    end_page = False
    follow_href = ('users/' + str(user.id) + '/followings' )
    followers_profile = {}
    followings_count = 0
    userprof = extractProfile(client, user)
    cor = 0.0
    while not end_page:
        while True:
            try:
                followings = client.get(follow_href, limit=100, linked_partitioning=1 )
            except:
                continue
            break
        followings_count += 100
        if hasattr(followings, 'next_href'):
            follow_href = followings.next_href
        else:
            end_page = True
        for item in followings.collection:
            buffer_profile = extractProfile(client, item, shortversion = True)
            merge(followers_profile, buffer_profile)
            if compare(buffer_profile, userprof) != 0:
                merge(followers_profile, buffer_profile)
                merge(followers_profile, buffer_profile)
        if(followings_count >1000): end_page = True

        return followers_profile
################################################################################

################################################################################
def merge(p1, p2):
    for key in p2:
        if p2.has_key(key) and p1.has_key(key):
            p1[key] += p2[key]
        else:
            p1[key] = p2[key]
################################################################################

################################################################################
def linkFromId(client, id):
    try:
        track = client.get('tracks/' + id )
    except:
        print ("unable to link to track id: " + str(id))
        return 'None'
    return track.permalink_url
################################################################################

################################################################################
def linksFromProfile(client, profile):
    sorted_tuples = sorted(profile.items(), key=operator.itemgetter(1))
    try:
        track = client.get('tracks/' + id )
        size = len(sorted_tuples)
        listOfLinks = []
    except:
        print ("unable to link to track id: " + str(id))
        return 'None'
    return track.permalink_url
################################################################################

################################################################################
def getSuggestionsFromProfile(client, profile, n=20):
    sorted_tuples = sorted(profile.items(), key=operator.itemgetter(1))
    size = len(profile)
    listOfLinks = []
    name = ''
    for i in range(1,n):
        name = linkFromId(client, sorted_tuples[size-i][0])
        if name != 'None':
            listOfLinks.append(name)
        else:
            n+=1
    return listOfLinks
################################################################################

################################################################################
def printSuggestions(profilename):
    actualclient = register()
    user = searchForUser(actualclient, profilename)
    profile = profileFollowings(actualclient, user)
    suggestions = getSuggestionsFromProfile(actualclient, profile, 30)
    print(profilename + " should like these tracks:")
    for item in suggestions: print item

def getSuggestions(profilename):
    actualclient = register()
    user = searchForUser(actualclient, profilename)
    profile = profileFollowings(actualclient, user)
    suggestions = getSuggestionsFromProfile(actualclient, profile, 30)
    return suggestions
################################################################################

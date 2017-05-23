################################################################################
#IMPORTS
import soundcloud
from math import sqrt

################################################################################

################################################################################
#REGISTERING APP
def register():
    client = soundcloud.Client(client_id='47b5a3d7a326382120d95d8c663b47f7')
    return client

def searchForUser(client, name):
    container = client.get('/users', q=name)
    return container[0]

def extractProfile(client, user):
    end_page = False
    profile = {}
    likes_href = ('users/' + str(user.id) + '/favorites' )
    comments_href = ('users/' + str(user.id) + '/comments' )
    playlists_href = ('users/' + str(user.id) + '/playlists' )
    reposted_done = False

    while(not end_page):
        #querying all data
        print('Downloading likes...')
        if likes_href != 'stop':
            likes = client.get( likes_href , limit=100, linked_partitioning=1 )
            if hasattr(likes, 'next_href'):
                likes_href = likes.next_href
            else:
                likes_href = 'stop'

        print('Downloading comments...')
        if comments_href != 'stop':
            comments = client.get( comments_href , limit=100, linked_partitioning=1 )
            if hasattr(comments, 'next_href'):
                comments_href = comments.next_href
            else:
                comments_href = 'stop'

        print('Downloading playlists...')
        if playlists_href != 'stop':
            playlists = client.get(playlists_href , limit=100, linked_partitioning=1 )
            if hasattr(playlists, 'next_href'):
                playlists_href = playlists.next_href
            else:
                playlists_href = 'stop'

        print('Downloading reposts...')
        if not reposted_done:
            reposts = client.get((
                        'https://api-v2.soundcloud.com/profile/soundcloud:users:'
                        + str(user.id) + '?limit=500'))

        if(reposted_done and likes_href == 'stop' and playlists_href == 'stop' and comments_href == 'stop'):
            end_page = True



        #processing playlists to extract tracks who are not from user
        print('Processing playlists...')
        for playlist in playlists.collection:
            for track in playlist.tracks:
                if track['user_id'] != user.id:
                    if user.username.lower() not in track['title'].lower():
                        if profile.has_key(str(track['id'])):
                            profile[str(track['id'])] += 1
                        else:
                            profile[str(track['id'])] = 1

        #processing all reposts to extract tracks who are not from user
        if not reposted_done:
            print('Processing reposts...')
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
        print('Processing comments...')
        for comment in comments.collection:
            if profile.has_key(str(comment.track_id)):
                profile[str(comment.track_id)] += 1
            else:
                profile[str(comment.track_id)] = 1

        #processing all likes to extract tracks who are not from user
        print('Processing likes...')
        liked = []
        for tracks in likes.collection:
            if user.username.lower() not in tracks.title.lower():
                if profile.has_key(str(tracks.id)):
                    profile[str(tracks.id)] += 1
                else:
                    profile[str(tracks.id)] = 1
        print(len(profile))

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

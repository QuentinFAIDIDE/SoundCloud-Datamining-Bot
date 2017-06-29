#!/usr/bin/env python

import SCDB
import sys
import os
import clusters
import signal

###################################################################################################
def main(args):
    def usage():
        print >>sys.stderr, "Usage:"
        print >>sys.stderr, "sctoolbox correlates common_tracks [user1] [user2]"
        print >>sys.stderr, "sctoolbox correlates pearson_tastes [user1] [user2]"
        print >>sys.stderr, "sctoolbox suggest [user] bestlikes [n]"
        print >>sys.stderr, "sctoolbox suggest [user] following_tournament [n]"
        print >>sys.stderr, "sctoolbox suggest [user] following_tournament_short [n]"
        print >>sys.stderr, "sctoolbox suggest [user] following_tournament [n] --nomix"
        print >>sys.stderr, "sctoolbox suggest [user] following_tournament_short [n] --nomix"
        print >>sys.stderr, "sctoolbox suggest [user] following_tournament_playlimit [n] --nomix [playlimit]"
        print >>sys.stderr, "sctoolbox suggest [user] following_tournament_playlimit [n] [playlimit]"
        print >>sys.stderr, "sctoolbox searchUser [username]"
        print >>sys.stderr, "sctoolbox searchTrack [trackname]"
        print >>sys.stderr, "sctoolbox getTrackScore [trackname]"
        print >>sys.stderr, "sctoolbox similar [trackname]"
        print >>sys.stderr, "sctoolbox draw_style_galaxy [user] [jpg_path]"

    paths = []

    client = SCDB.register()

    ##############################################################################
    if len(args) == 5 and args[1] == 'correlates' and args[2] == 'pearson_tastes':
        user1 = SCDB.searchForUser(client, args[3])
        user2 = SCDB.searchForUser(client, args[4])

        puser1 = SCDB.extractProfile(client, user1)
        puser2 = SCDB.extractProfile(client, user2)

        r = SCDB.comparePearson(puser1, puser2)

        print 'Correlation score between users (pearson):', r
    ##############################################################################

    ##############################################################################
    elif len(args) == 5 and args[1] == 'correlates' and args[2] == 'common_tracks':
        user1 = SCDB.searchForUser(client, args[3])
        user2 = SCDB.searchForUser(client, args[4])

        puser1 = SCDB.extractProfile(client, user1)
        puser2 = SCDB.extractProfile(client, user2)

        r = SCDB.compareCommonTracks(puser1, puser2)

        print 'Correlation score between users (common tracks):', r
    ##############################################################################

    ##############################################################################
    elif len(args) == 5 and args[1] == 'suggest' and args[3] == 'following_tournament':
        print('Launching tournament between tracks from followings, might take a while...')
        user = SCDB.searchForUser(client, args[2])
        profile = SCDB.profileFollowings(client, user)
        suggestions = SCDB.getSuggestionsFromProfile(client, profile, int(args[4]))
        print(args[2] + " should like these tracks:")
        for item in suggestions: print item
    ##############################################################################

    ##############################################################################
    elif len(args) == 5 and args[1] == 'suggest' and args[3] == 'bestlikes':
        print('Rating tracks user liked, reposted, or commented, and playlisted, might take a while...')
        user = SCDB.searchForUser(client, args[2])
        profile = SCDB.sortProfileFromFollowings(client, user)
        suggestions = SCDB.getSuggestionsFromProfile(client, profile, int(args[4]))
        print(args[2] + " best likes are:")
        for item in suggestions: print item
    ##############################################################################

    ##############################################################################
    elif len(args) == 5 and args[1] == 'suggest' and args[3] == 'following_tournament_short':
        print('Launching short tournament between tracks from followings...')
        user = SCDB.searchForUser(client, args[2])
        profile = SCDB.profileFollowingsShort(client, user)
        suggestions = SCDB.getSuggestionsFromProfile(client, profile, int(args[4]))
        print(args[2] + " should like these tracks:")
        for item in suggestions: print item
    ##############################################################################

    ##############################################################################
    elif len(args) == 6 and args[1] == 'suggest' and args[3] == 'following_tournament' and args[5] == '--nomix':
        print('Launching tournament between tracks from followings, might take a while...')
        user = SCDB.searchForUser(client, args[2])
        profile = SCDB.profileFollowings(client, user)
        suggestions = SCDB.getSuggestionsFromProfile(client, profile, int(args[4]), no_mix = True)
        print(args[2] + " should like these tracks:")
        for item in suggestions: print item
    ##############################################################################

    ##############################################################################
    elif len(args) == 6 and args[1] == 'suggest' and args[3] == 'following_tournament_short' and args[5] == '--nomix':
        print('Launching short tournament between tracks from followings...')
        user = SCDB.searchForUser(client, args[2])
        profile = SCDB.profileFollowingsShort(client, user)
        print('Generating big profile...')
        suggestions = SCDB.getSuggestionsFromProfile(client, profile, int(args[4]), no_mix=True)
        print(args[2] + " should like these tracks:")
        for item in suggestions: print item
    ##############################################################################

    ##############################################################################
    elif len(args) == 7 and args[1] == 'suggest' and args[3] == 'following_tournament_playlimit' and args[5] == '--nomix':
        print('Launching custom tournament between tracks from followings...')
        user = SCDB.searchForUser(client, args[2])
        profile = SCDB.profileFollowings(client, user)
        suggestions = SCDB.getSuggestionsFromProfile(client, profile, int(args[4]), no_mix=True, played_limit=int(args[6]))
        print(args[2] + " should like these tracks:")
        for item in suggestions: print item
    ##############################################################################

    ##############################################################################
    elif len(args) == 6 and args[1] == 'suggest' and args[3] == ' following_tournament_playlimit ':
        print('Launching custom tournament between tracks from followings...')
        user = SCDB.searchForUser(client, args[2])
        profile = SCDB.profileFollowings(client, user)
        suggestions = SCDB.getSuggestionsFromProfile(client, profile, int(args[4]), no_mix=False, played_limit=int(args[5]))
        print(args[2] + " should like these tracks:")
        for item in suggestions: print item
    ##############################################################################

    ##############################################################################
    elif len(args) == 3 and args[1] == 'searchUser':
        container = client.get('/users', q=args[2])
        n=1
        for item in container:
            print('############################')
            print('#'+str(n))
            n+=1
            print('username:' + item.username)
            print('permalink:' + item.permalink)
        print('############################')
    ##############################################################################

    ##############################################################################
    elif len(args) == 4 and args[1] == 'draw_style_galaxy':
        print('Identifying user...')
        user = SCDB.searchForUser(client, args[2])
        print('Downloading followers list...')
        followers_list = SCDB.getFollowerList(client, user)
        followers_list = SCDB.exctractsample(followers_list)
        row, col, data = SCDB.getCommentsData(client, followers_list)
        print('Generating clusters...')
        rotdata = clusters.rotatematrix(data)
        tagclust = clusters.hcluster(rotdata)
        print("Generationg dendrogram drawing...")
        clusters.drawdendrogram(tagclust,col,jpeg=args[3])
    ##############################################################################

    ##############################################################################
    ##############################################################################

    ##############################################################################
    ##############################################################################

    ##############################################################################
    ##############################################################################

    ##############################################################################
    ##############################################################################

    else:
        usage()

###################################################################################################
if __name__ == '__main__':
    main(sys.argv)

import SCDB
import sys

def main(args):
    def usage():
        print >>sys.stderr, "Usage:"
        print >>sys.stderr, "sctoolbox correlates common_tracks [user1] [user2]"
        print >>sys.stderr, "sctoolbox correlates pearson_tastes [user1] [user2]"
        print >>sys.stderr, "sctoolbox suggest [user] following_tournament [n]"
        print >>sys.stderr, "sctoolbox suggest [user] following_tournament_short [n]"
        print >>sys.stderr, "sctoolbox suggest [user] following_tournament_filter_mainstream [n]"
        print >>sys.stderr, "sctoolbox searchUser [username]"
        print >>sys.stderr, "sctoolbox searchTrack [trackname]"
        print >>sys.stderr, "sctoolbox getTrackScore [trackname]"
        print >>sys.stderr, "sctoolbox similar [trackname]"

    paths = []

    client = SCDB.register()

    if len(args) == 4 and args[1] == 'correlates' and args[2] == 'pearson_tastes':
        user1 = SCDB.searchForUser(client, args[2])
        user2 = SCDB.searchForUser(client, args[3])

        puser1 = SCDB.extractProfile(client, user1)
        puser2 = SCDB.extractProfile(client, user2)

        r = SCDB.comparePearson(puser1, puser2)

        print 'Correlation score between users (pearson):', r


    elif len(args) == 4 and args[1] == 'correlates' and args[2] == 'common_tracks':
        user1 = SCDB.searchForUser(client, args[2])
        user2 = SCDB.searchForUser(client, args[3])

        puser1 = SCDB.extractProfile(client, user1)
        puser2 = SCDB.extractProfile(client, user2)

        r = SCDB.compareCommonTracks(puser1, puser2)

        print 'Correlation score between users (common tracks):', r

    else:
        usage()

if __name__ == "__main__":
    main(sys.argv)

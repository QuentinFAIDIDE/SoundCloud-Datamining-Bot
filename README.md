# SCTOOLBOX
##What ?
A toolbox to mine data from soundcloud, make tracks suggestions, analyse the
correlation between users and their tastes, and analyse track data for example
by giving a success score.
##How ?
'''
sctoolbox correlates common_tracks [user1] [user2]
sctoolbox correlates pearson_tastes [user1] [user2]
sctoolbox suggest [user] following_tournament [n]
sctoolbox suggest [user] following_tournament_short [n]
sctoolbox suggest [user] following_tournament_filter_mainstream [n]
sctoolbox searchUser [username]
sctoolbox searchTrack [trackname]
sctoolbox getTrackScore [trackname]
sctoolbox similar [trackname]
'''

##IMPORTANT
**Not all functions are implemented, and more is to come, and you might find some bug.**
You can make suggestions and analyse correlations between users. Downloading and processing
the data might take some time if you try to make suggestions.

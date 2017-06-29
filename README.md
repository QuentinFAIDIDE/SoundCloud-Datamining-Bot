# SCTOOLBOX
# What ?
Soundcloud cli toolbox used to:<br />
-Generate a list of music suggestions that fits the tastes of a targeted user using user-based collective filtering <br />
-Sort for the best likes from a user using users with similar tastes from his followings <br />
-Create a drawing where you can see group of tastes from the targeted user followers <br />
-Find correlations between users <br />
-Search for user <br />
WORK IN PROGRESS BUT FUNCTIONAL <br />
# How ?

Usage:<br />
sctoolbox correlates common_tracks [user1] [user2]<br />
sctoolbox correlates pearson_tastes [user1] [user2]<br />
sctoolbox suggest [user] bestlikes [n]<br />
sctoolbox suggest [user] following_tournament [n]<br />
sctoolbox suggest [user] following_tournament_short [n]<br />
sctoolbox suggest [user] following_tournament [n] --nomix<br />
sctoolbox suggest [user] following_tournament_short [n] --nomix<br />
sctoolbox suggest [user] following_tournament_playlimit [n] --nomix [playlimit]<br />
sctoolbox suggest [user] following_tournament_playlimit [n] [playlimit]<br />
sctoolbox searchUser [username] <br />
sctoolbox searchTrack [trackname] <br />
sctoolbox getTrackScore [trackname] <br />
sctoolbox similar [trackname] <br />
sctoolbox draw_style_galaxy [user] [jpg_path] <br />


# Important
Not all functions are implemented yet, more is to come, and you might find some bugs. <br />
You can make suggestions and analyse correlations between users. Downloading and processing
the data might take some time if you try to make suggestions.

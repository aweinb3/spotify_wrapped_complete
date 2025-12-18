#%%
### COMBINING JSON & FORMATTING EXPORT

# import libraries
import pandas as pd
import glob
import json

# read in json files
dfs = [pd.DataFrame(json.load(open(f))) for f in glob.glob("avi_history copy/Streaming_History_Audio*.json")]
df = pd.concat(dfs, ignore_index=True)

# drop podcast/audiobook columns
songs_df = df.drop(columns=["episode_name", "episode_show_name", "spotify_episode_uri", "audiobook_title", "audiobook_uri", "audiobook_chapter_uri", "audiobook_chapter_title"])
 
# simplify column names
songs_df.rename(columns={
    "master_metadata_track_name": "track",
    "master_metadata_album_artist_name": "artist",
    "master_metadata_album_album_name": "album"
}, inplace=True)

# convert ms_played into s_played
songs_df["ms_played"] = songs_df["ms_played"]/1000
songs_df.rename(columns={"ms_played": "s_played"}, inplace=True)

# check output
songs_df.info()

#%%

### EXPORT TO CSV

songs_df.to_csv('streams_raw.csv')
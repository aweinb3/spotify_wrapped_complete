# Spotify Wrapped Complete  

**Live App Link:** https://spotifywrappedcomplete.streamlit.app
  
## 1. Overview
If you're a Spotify user, you've probably noticed that Wrapped has gone from a genuine year-end highlight to something that feels increasingly generic. There are two main things that have always bothered me.  
1. **Wrapped stops collecting data in the beginning of November,** leaving the last couple months of the year unaccounted for.
2. **Looking back historically is surprisingly hard.** You can find your old generated playlists, but your stats essentially disappear once the annual campaign is done.

This project started as a way to solve both these problems.  

Spotify actually gives you access to your extended streaming history via your [account privacy tab](https://www.spotify.com/ca-en/account/privacy/), and once I received mine I was able to look back on over a decade of listening. Unlike third party services like Last.fm (which I love don't get me wrong), this lets you look back on *all* your data, not just what starts being collected when you sign up for the service.  

## 2. Process  
When wrapped came out this year, a lot of jokes circulated about how the internet goes crazy over what's essentially just some simple SQL queries. That curiosity pushed me to see how much of Wrapped I could recreate using my raw data.  

I started by just reopening my Wrapped and taking note of every metric that was offered, and then worked on rebuilding those insights in a Jupyter notebook. Within a couple hours I was able to reproduce most of the core outputs: top tracks, artists, listening time, grouped by year, as well as all time cumulative stats.  

To make the project usable by others, I added a lightweight frontend UI using streamlit. With some assistance from Claude, I was able to develop an interactive interface that simplifies use and avoids the need to install anything locally or write any code yourself.

## 3. Tools
- Python
- pandas
- Streamlit
- Plotly

## 4. Takeaways & Next Steps
I ended up learning much more from this project than initially intended. Beyond an exercise to reinforce my pandas skills, and an excuse to reminisce on my favourite albums through high school, it forced me to think about:  
- Data ingestion from raw user files
- Cleaning messy real-world data
- Translating analysis into a usable interface
- UX decisions around what insights actually matter

This is intentionally an MVP, but I hope to expand it in the future. I'm already thinking about.
- Connecting to more insights via Spotify's API (genres, artist popularity)
- More behavioral insights (already looking into skip rates, seasonal trends, etc.)
- Building a more enjoyable UI in framer.

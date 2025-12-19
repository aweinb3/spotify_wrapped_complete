# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Wrapped Dupe", layout="wide")

st.title("Wrapped Dupe")
st.markdown("Upload your Spotify Extended Streaming History to see your listening stats")

# File upload
uploaded_files = st.file_uploader(
    "Upload your Spotify JSON files (you can select multiple)",
    type=['json'],
    accept_multiple_files=True
)

if uploaded_files:
    # Process uploaded files
    try:
        dfs = []
        for file in uploaded_files:
            data = json.load(file)
            dfs.append(pd.DataFrame(data))
        
        df = pd.concat(dfs, ignore_index=True)
        
        # Convert timestamp to datetime
        df['ts'] = pd.to_datetime(df['ts'])
        
        # Convert ms_played to s_played
        df['s_played'] = df['ms_played'] / 1000
        
        st.success(f"✅ Loaded {len(df):,} streams from {len(uploaded_files)} file(s)")
        
        # Get date range from data
        min_date = df['ts'].min()
        max_date = df['ts'].max()
        
        st.write(f"Data range: {min_date.date()} to {max_date.date()}")
        
        # Date range selection
        st.subheader("Select Time Period")
        
        # Generate list of available full years
        min_year = min_date.year
        max_year = max_date.year
        available_years = list(range(max_year, min_year - 1, -1))
        date_options = [str(year) for year in available_years]

        # Add custom option
        # date_options = ["Custom"] + [str(year) for year in available_years]
        
        selected_option = st.selectbox("Select a year:", date_options)
        
        # Full year selection
        year = int(selected_option)
        start_date = pd.Timestamp(f"{year}-01-01").date()
        end_date = pd.Timestamp(f"{year}-12-31").date()
        #st.info(f"Showing data for: {start_date} to {end_date}")
        
        # Filter data
        filtered = df[(df['ts'] >= pd.Timestamp(start_date, tz="UTC")) & (df['ts'] <= pd.Timestamp(end_date, tz="UTC"))].copy()
        
        if len(filtered) == 0:
            st.warning("No data available for the selected time period.")
        else:
            st.write(f"**{(filtered['s_played'] >= 30).sum():,} full streams** in selected period.")
            
            # Calculate metrics
            st.subheader("📊 Your Listening Stats")
            
            # Total minutes
            tot_minutes = filtered['s_played'].sum() / 60
            
            # Unique counts
            unique_songs = filtered['master_metadata_track_name'].nunique()
            unique_albums = filtered['master_metadata_album_album_name'].nunique()
            unique_artists = filtered['master_metadata_album_artist_name'].nunique()
            
            # Display summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Minutes", f"{tot_minutes:,.0f}")
            with col2:
                st.metric("Unique Songs", f"{unique_songs:,}")
            with col3:
                st.metric("Unique Albums", f"{unique_albums:,}")
            with col4:
                st.metric("Unique Artists", f"{unique_artists:,}")
            
            st.divider()
            
            # Creating columns for top streams, albums, artists
            col1, col2, col3 = st.columns(3)

            # Top 5 Songs (by stream count, 30+ seconds)
            with col1:
                st.subheader("🎵 Top 5 Songs")
                streams = filtered[filtered['s_played'] >= 30].copy()
                top_songs = (
                    streams.groupby('master_metadata_track_name')
                    .size()
                    .sort_values(ascending=False)
                    .head(5)
                )
                
                for idx, (song, count) in enumerate(top_songs.items(), 1):
                    st.write(f"**{idx}.** {song} — *{count} streams*")
            
            # Top 5 Albums (by streams)
            with col2:
                st.subheader("💿 Top 5 Albums")
                top_albums = (
                    streams.groupby('master_metadata_album_album_name')['s_played']
                    .size()
                    .sort_values(ascending=False)
                    #.head(5)
                    .iloc[1:6] # just so that linkedin screenshot isnt "FUCK YOU SKRILLEX"
                )
                
                for idx, (album, count) in enumerate(top_albums.items(), 1):
                    st.write(f"**{idx}.** {album} — *{count} streams*")
                
            # Top 5 Artists (by total minutes)
            with col3:
                st.subheader("🎤 Top 5 Artists")
                top_artists = (
                    filtered.groupby('master_metadata_album_artist_name')['s_played']
                    .sum()
                    .div(60)
                    .sort_values(ascending=False)
                    .head(5)
                )
                
                for idx, (artist, minutes) in enumerate(top_artists.items(), 1):
                    st.write(f"**{idx}.** {artist} — *{minutes:,.0f} minutes*")
    
        st.divider()
        
        st.subheader("📈 All-Time Stats")
        
        # Making chart for all time streaming minutes
        
        st.subheader("Minutes Streamed by Year")
        yearly_minutes = (
            df.groupby(df['ts'].dt.year)['s_played']
            .sum()
            .div(60)
            .reset_index()
        )
        
        yearly_minutes.columns = ['Year', 'Minutes']
        
        fig = px.bar(yearly_minutes, x='Year', y='Minutes', color='Minutes', color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)


        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🎵 Top Songs (All-Time)")
            all_time_songs = (
                df[df['s_played'] >= 30]
                .groupby(['master_metadata_track_name', 'master_metadata_album_artist_name'])
                .size()
                .sort_values(ascending=False)
                .head(20)
            )
            for idx, ((song, artist), count) in enumerate(all_time_songs.items(),1):
                st.write(f"**{idx}. {song}** *{artist} - {count:,} streams*")
        
        with col2:
            st.subheader("💿 Top Albums (All-Time)")
            all_time_albums = (
                df[df['s_played'] >= 30]
                .groupby(['master_metadata_album_album_name', 'master_metadata_album_artist_name'])
                .size()
                .sort_values(ascending=False)
                .head(20)
            )
            for idx, ((album, artist), count) in enumerate(all_time_albums.items(),1):
                st.write(f"**{idx}. {album}** *{artist} - {count:,} streams*")
        
        with col3:
            st.subheader("🎤 Top Artists (All-Time)")
            all_time_artists = (
                df.groupby('master_metadata_album_artist_name')['s_played']
                .sum()
                .div(3600)
                .sort_values(ascending=False)
                .head(20)
            )
            for idx, (artist, hours) in enumerate(all_time_artists.items(),1):
                st.write(f"**{idx}. {artist}** - *{hours:.1f} hours*")
        
    except Exception as e:
        st.error(f"Error processing files: {str(e)}")
        st.write("Make sure you're uploading valid Spotify Extended Streaming History JSON files.")

else:
    st.info("👆 Upload your Spotify JSON files to get started")
    st.markdown("""
    ### How to get your data:
    1. Go to your [Spotify Account Privacy Settings](https://www.spotify.com/account/privacy/)
    2. Scroll down and check box for "Preparing Extended streaming history" (you only need this one)
    3. Click on "Request data"
    3. Wait for Spotify to prepare your data (can take a few hours to a few days)
    4. Download files from email
    5. Upload all files here!

    ** Note: it will take a moment for all files to upload to the website  
    ** Other note: We do not store your data!! Everything occurs securly on streamlit's servers.
    """)

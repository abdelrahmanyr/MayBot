import discord
from discord.ext import commands
from discord import utils
import math
import random
import itertools
import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

st = "67587c0f933aa8ab2e59377a14d0d315"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = "4d35b62383e543679384be5c9ff3fd6a",
                                                           client_secret = "100c64fa520d4f98969c5b1bfdd92e46",))
class Recommendations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description = "Returns an artist's information, albums and top tracks based on the input from Spotify.",
                      usage = "`.artist [artist name]`"
                     )
    async def artist(self, ctx, *, artist = None):

        if artist is None:
            await ctx.send(":question: | Give an artist name to search for.")
        else:
            results = sp.search(q={artist}, type='artist')
            items = results['artists']['items']
            try:
                artist = items[0]
            except IndexError:
                await ctx.send(":bangbang: | Sorry I couldn't find any results")
            artist_name = artist['name']
            artist_genres = artist['genres']
            artist_genre = " - ".join(f"{genre.capitalize()}" for genre in artist_genres)
            artist_followers = artist['followers']['total']
            artist_link = str(artist['external_urls']['spotify'])

            top_tracks_response = sp.artist_top_tracks(artist['id'])['tracks']
            top_tracks = list(itertools.islice(top_tracks_response, 0, None))
            tracks = "\n".join(f"- {str(track['name'])}" for track in top_tracks)

            albums_response = list(sp.artist_albums(artist['id'], album_type = "album")['items'])
            albums = []
            for i in albums_response:
                albums.append(i['name'])
            albums = list(dict.fromkeys(albums))
            album = "\n".join(f"- {str(album)}" for album in albums)

            image_url = artist['images'][0]['url']

            embed = discord.Embed(
                                  description = f"**• Genres:** {artist_genre} \n **• Followers:** {artist_followers} \n **• Spotify link:** __[Link]({artist_link})__",
                                  color = discord.Colour.dark_red()       
                                 )
            embed.set_author(name = artist_name, icon_url = image_url)
            embed.add_field(name = "Top tracks", value = tracks, inline = False)
            embed.add_field(name = "Albums", value = album)
            embed.set_image(url = image_url)
            await ctx.send(embed = embed)


    @commands.command(description = "Returns an album's information, and tracks based on the input from Spotify.",
                      usage = "`.album [album name]`"
                     )
    async def album(self, ctx, *, album = None):

        if album is None:
            await ctx.send(":question: | Give an album name to search for.")
        else:
            results = sp.search(q={album}, type='album')
            items = results['albums']['items']
            try:
                album = items[0]
            except IndexError:
                await ctx.send(":bangbang: | Sorry I couldn't find any results")
            album_name = album['name']
            album_link = str(album['external_urls']['spotify'])
            album_artist = album['artists'][0]['name']
            album_date = album['release_date']
            album_tracks_number = album['total_tracks']            
            album_image = album['images'][0]['url']
            album_tracks = sp.album_tracks(album['id'])['items']
            tracks_list = list(itertools.islice(album_tracks, 0, None))
            tracks = "\n".join(f"{tracks_list.index(track) + 1} - {track['name']}" for track in tracks_list)

            embed = discord.Embed(description = f"**• Artist:** {album_artist} \n **• Release date:** {album_date} \n **• Total tracks:** {album_tracks_number} \n **• Spotify link:** __[Link]({album_link})__",
                                  color = discord.Color.dark_red()
                                 )
            embed.set_author(name = album_name, icon_url = album_image)
            embed.add_field(name = f"Tracks", value = tracks)
            embed.set_image(url = album_image)
            await ctx.send(embed = embed)



    @commands.command(description = "Returns a list of tracks in a playlist based on the input from Spotify.",
                      usage = "`.playlist [playlist name]`")
    async def playlist(self, ctx, *, playlist = None):

        if playlist is None:
            await ctx.send(":question: | Give a playlisy name to search for.")
        else:
            results = sp.search(q={playlist}, type='playlist')
            items = results['playlists']['items']
            try:
                playlist = items[0]
            except IndexError:
                await ctx.send(":bangbang: | Sorry I couldn't find any results")

            playlist_name = playlist['name']
            playlist_owner = playlist['owner']['display_name']
            playlist_tracks_n = playlist['tracks']['total']
            playlist_link = str(playlist['external_urls']['spotify'])

            playlist_id = playlist['uri']
            playlist_tracks = sp.playlist_tracks(playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track', ))['items']
            playlist_tr = list(itertools.islice(playlist_tracks, 0, None))
            tracks = "\n".join(f"{playlist_tr.index(track) + 1} - {track['track']['name']}" for track in playlist_tr)[:1023]
            image_url = playlist['images'][0]['url']

            embed = discord.Embed(description = f"**• Owner:** {str(playlist_owner)}\n **• Total Tracks:** {playlist_tracks_n} \n **• Spotify Link:** __[Link]({playlist_link})__",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = playlist_name, icon_url = image_url)
            embed.add_field(name = "Total Tracks", value = f"{tracks}")
            embed.set_image(url = image_url)
            await ctx.send(embed = embed)

    @commands.command(description = "Returns a track's information, and similar tracks based on the input from Spotify.",
                      usage = "`.track [track name]`")
    async def track(self, ctx, *, track = None):

        if track is None:
            await ctx.send(":question: | Give a track name to search for.")
        else:
            results = sp.search(q={track}, type='track')
            items = results['tracks']['items']
            try:
                track = items[0]
            except IndexError:
                await ctx.send(":bangbang: | Sorry I couldn't find any results")

            track_name = track['name']
            track_url = str(track['external_urls']['spotify'])
            track_album = track['album']['name']
            track_artist = track['album']['artists'][0]['name']

            track_recommendations = sp.recommendations(seed_tracks = [track['id']], limit = 5)['tracks']
            recommendations_list = list(itertools.islice(track_recommendations, 0, None))
            recommendations = "\n".join(f"- {recommendation['name']} - ({recommendation['album']['artists'][0]['name']})" for recommendation in recommendations_list)

            image_url = track['album']['images'][0]['url']


            embed = discord.Embed(description = f"**• Artist:** {str(track_artist)}\n **• Album:** {track_album} \n **• Spotify link:** __[Link]({track_url})__",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = track_name, icon_url = image_url)
            embed.add_field(name = "Simillar tracks", value = recommendations)
            embed.set_image(url = image_url)
            await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Recommendations(client))
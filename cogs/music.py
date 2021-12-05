import discord

from discord.ext import commands, menus
from typing import Union
import random
import wavelink
import asyncio
import itertools
import random
import ksoftapi
import dbl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from lyricsgenius import Genius
gn = Genius("-HL3Je0SfWKj5r44QMyoxYxq_ZKERBQ0x0jOmjiXCUXenH8hFtw7_b4LM3aTTd5G")
st = "67587c0f933aa8ab2e59377a14d0d315"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = "4d35b62383e543679384be5c9ff3fd6a",
                                                           client_secret = "100c64fa520d4f98969c5b1bfdd92e46",))
kclient = ksoftapi.Client('ac8f0be3bfd40393c7c6aa58fb0c8c61de7f4064')

class Track(wavelink.Track):
    __slots__ = ('requester', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.requester = kwargs.get('requester')

class MusicController:

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None

        self.next = asyncio.Event()
        self.queue = asyncio.Queue()
        self.previous = []

        self.volume = 100
        self.loop_state = "0"
        self.now_playing = None

        self.bot.loop.create_task(self.controller_loop())
    
    def format_time(self, time):
        time = round(time)
        hours, remainder = divmod(time / 1000, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours != 0:
            return '%02d:%02d:%02d' % (hours, minutes, seconds)
        else:
            return '%02d:%02d' % (minutes, seconds)

    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player = self.bot.wavelink.get_player(self.guild_id)
        await player.set_volume(self.volume)

        while True:
            if self.now_playing:
                await self.now_playing.delete()

            self.next.clear()

            if self.loop_state == "1":
                song = self.previous[0]
            elif self.loop_state == "2":
                await self.queue.put(self.previous[0])
                song = await self.queue.get()
            else:
                song = await self.queue.get()
                if song.id == "QAAAkQIAKEhPVyBUTyBNQVNURVIgQSBUUkFDSyBJTiBVTkRFUiAzIFNFQ09ORFMAD0R5bGFuIFRhbGxjaGllZgAAAAAAAAu4AAswY0t0eDI5MUktRQABACtodHRwczovL3d3dy55b3V0dWJlLmNvbS93YXRjaD92PTBjS3R4MjkxSS1FAAd5b3V0dWJlAAAAAAAAAAA=":
                    old_song = song
                    tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{old_song.title} Audio")
                    song = Track(tracks[0].id, tracks[0].info, requester = song.requester)
                    song.title, song.uri = old_song.title, old_song.uri
            await player.play(song)
            
            self.now_playing = await self.channel.send(f":play_pause: | __Now playing:__ **{song}** **`[{self.format_time(song.length)}]`**.")

            await self.next.wait()

class PaginatorSource(menus.ListPageSource):
    """Player queue paginator class."""

    def __init__(self, entries, *, per_page = 10, ctx, player, controller, bot):
        super().__init__(entries, per_page = per_page)
        self.ctx = ctx
        self.bot = bot
        self.player = player
        self.controller = controller

    def format_time(self, time):
        time = round(time)
        hours, remainder = divmod(time / 1000, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours != 0:
            return '%02d:%02d:%02d' % (hours, minutes, seconds)
        else:
            return '%02d:%02d' % (minutes, seconds)
            
    async def format_page(self, menu: menus.Menu, page):
        guild = self.ctx.guild
        totald = self.player.current.length
        try:
            for song in self.controller.queue._queue:
                totald += song.length
        except AttributeError:
            totald = self.player.current.track_length
        if self.controller.loop_state == "0":
            loop_state = "Disabled"
        elif self.controller.loop_state == "1":
            loop_state = "Track Looping"
        elif self.controller.loop_state == "2":
            loop_state = "Queue Looping"
        tracks_list = '\n'.join(f"**{list(self.controller.queue._queue).index(song) + 1}** • **{str(song)}** **`[{self.format_time(song.length)}]`**" for index, song in enumerate(page, 1))
        embed = discord.Embed(title = "MayBot Queue:", colour = discord.Colour.dark_red())
        embed.description = f"__Upcoming Tracks | {len(self.controller.queue._queue)}__\n{tracks_list}"
        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
        embed.add_field(name = f"Current Track", value = f"**- {self.player.current.title}** `[{self.format_time(self.player.current.length)}]`", inline = False)
        embed.add_field(name = f"Total Duration", value =f"**[{self.format_time(totald)}]**", inline = True)
        embed.add_field(name = f"Loop State", value = loop_state)
        embed.set_footer(text = f"{guild.name}'s queue", icon_url = guild.icon_url)
        return embed

    def is_paginating(self):
        # We always want to embed even on 1 page of results...
        return True

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc0Nzk2NTEyNTU5OTgyMTkxNCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEyODcxNjgyfQ.rXjO968rh8zgJRgXJZr3GZzKw8JExp_vVtbB6l5x8Ts" 
        self.dbl = dbl.DBLClient(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth='nice', webhook_port=8080)

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot = self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        node = await self.bot.wavelink.initiate_node(host = "http://maylava.herokuapp.com",
                                                     port = 4623,
                                                     rest_uri = "http://maylava.herokuapp.com",
                                                     password = "youshallnotpass",
                                                     identifier = "MAIN",
                                                     region = "europe")
        node.set_hook(self.on_event_hook)

    async def on_event_hook(self, event):
        if isinstance(event, (wavelink.TrackEnd, wavelink.TrackException)):
            controller = self.get_controller(event.player)
            controller.next.set()

    def get_controller(self, value: Union[commands.Context, wavelink.Player]):
        if isinstance(value, commands.Context):
            gid = value.guild.id
        else:
            gid = value.guild_id

        try:
            controller = self.controllers[gid]
        except KeyError:
            controller = MusicController(self.bot, gid)
            self.controllers[gid] = controller

        return controller

    def format_time(self, time):
        time = round(time)
        hours, remainder = divmod(time / 1000, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours != 0:
            return '%02d:%02d:%02d' % (hours, minutes, seconds)
        else:
            return '%02d:%02d' % (minutes, seconds)

    async def has_voted(self, ctx):
        db = await self.dbl.get_user_vote(ctx.author.id)
        if db == True:
            print("true")
            pass
        else:
            print("not true")
            embed = discord.Embed(title = "Vote",
                                  description = f":o: | To use this command you have to vote for me at __**[top.gg](http://gestyy.com/er3AB8)**__ and __**[discordbotlist.com](http://gestyy.com/er3AMy)**__\nTo avoid going through annoying ads and voting every 12 hours apply a premium plan on our [__**patreon page**__](https://www.patreon.com/MayBot1), for more information use `.premium`.",          
                                  colour = discord.Colour.dark_red()
                                 )
            await ctx.send(embed = embed)
            return False
            

    def play_embed(self, ctx, track, player):
        if player.is_playing:
            embed = discord.Embed(title = "Enqueued:",
                            description = f":play_pause: | __**[{str(track)}]({track.uri})**__",
                            color = discord.Colour.dark_red()
                            )
            embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")
            embed.add_field(name = "Track Duration", value = f"**`[{self.format_time(track.length)}]`**", inline = False)
        if not player.is_playing:
            embed = discord.Embed(title = "Playing:",
                            description = f":play_pause: | __**[{str(track)}]({track.uri})**__",
                            color = discord.Colour.dark_red()
                            )
            embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")
            embed.add_field(name = "Track Duration", value = f"**`[{self.format_time(track.length)}]`**", inline = False)
        return embed
    
    def spotify_track(self, link):
        track = sp.track(link)
        track_name = track['name']
        track_url = str(track['external_urls']['spotify'])
        track_artist = track['artists'][0]['name']
        track_cover = track['album']['images'][0]['url']
        return track_name, track_url, track_artist, track_cover

    def spotify_album(self, link):
        album_tracks = sp.album_tracks(link)
        tracks = []
        for track in album_tracks['items']:
            track = sp.track(track['id'])
            tracks.append(track)
        return tracks

    def spotify_playlist(self, link):
        playlist_tracks = sp.playlist_tracks(link)
        tracks = []
        for track in playlist_tracks['items']:
            track = sp.track(track['track']['id'])
            tracks.append(track)
        return tracks
    
    def spotify_artist(self, link):
        artist_tracks = sp.artist_top_tracks(link)
        tracks = []
        for track in artist_tracks['tracks']:
            track = sp.track(track['id'])
            tracks.append(track)
        return tracks

    @commands.command(name = "connect", aliases = ["c", "join"],
                      description = "Connects the bot to the mentioned voice channel, if a channel was not mentioned then the bot connects to the message author voice channel.",
                      usage = "`.connect\n.connect [voice channel]`"
                     )
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.send(":question: | No channel to join, Type the desired channel's name or join one.")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.send(f":gear: | Connecting to **`{channel.name}`**..", delete_after = 5)

        await player.connect(channel.id)
        await asyncio.sleep(1)
        if player.is_paused:
            await player.set_pause(pause = False)
            
        controller = self.get_controller(ctx)
        controller.channel = ctx.channel
    
    @commands.command(aliases = ["p"],
                      description = "Plays a track, livestream or a playlist, if a URL was not specified then searches Youtube for the query and plays the first result and if an attachment was sent with the command without a query your attachment is played.",
                      usage = "`.play [URL]\n.play [query]\n.play (attatchment)`"
                     )
    async def play(self, ctx, *, query: str = None):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

 

        if player.channel_id == ctx.author.voice.channel.id:
            if query is None and ctx.message.attachments:
                query = ctx.message.attachments[0].url

            if query.startswith("http"):
                tracks = await self.bot.wavelink.get_tracks(query)
                if query.startswith("https://open.spotify.com/track"):
                    name, url, artist, cover = self.spotify_track(query)
                    tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{name} - {artist} Audio")
                    track = Track(tracks[0].id, tracks[0].info, requester = ctx.author)
                    yt_link = track.uri
                    track.title, track.uri, track.thumb = f"{name} - {artist}", url, cover
                    controller = self.get_controller(ctx)
                    await controller.queue.put(track)
                    embed = self.play_embed(ctx, track, player)
                    embed.add_field(name = "Youtube Link", value = f"[Link]({yt_link})")
                    embed.set_thumbnail(url = cover)
                    await ctx.send(embed = embed)

                elif query.startswith("https://open.spotify.com/album"):
                    album_name = sp.album(query)['name']
                    album_url = sp.album(query)['external_urls']['spotify']
                    tracks = self.spotify_album(query)
                    fake = await self.bot.wavelink.get_tracks("https://www.youtube.com/watch?v=0cKtx291I-E")

                    for track_ in tracks:
                        track = Track(fake[0].id, fake[0].info, requester = ctx.author)
                        track.title, track.uri, track.thumb, track.length = f"{track_['name']} - {track_['artists'][0]['name']}", str(track_['external_urls']['spotify']), track_['album']['images'][0]['url'], track_['duration_ms']
                        controller = self.get_controller(ctx)
                        await controller.queue.put(track)
                    embed = discord.Embed(title = "Enqueued Album:",
                                                description = f":play_pause: | __**[{album_name}]({album_url})**__",
                                                color = discord.Colour.dark_red()
                                         )
                    embed.add_field(name = "Playlist Player", value = f"{ctx.author.mention}")
                    embed.add_field(name = "Number of Tracks", value = f"{len(tracks)}", inline = True)
                    embed.set_thumbnail(url = track_['album']['images'][0]['url'])
                    await ctx.send(embed = embed)

                elif query.startswith("https://open.spotify.com/playlist"):
                    playlist = sp.playlist(query)
                    playlist_name = playlist['name']
                    playlist_url = playlist['external_urls']['spotify']
                    tracks = self.spotify_playlist(query)
                    fake = await self.bot.wavelink.get_tracks("https://www.youtube.com/watch?v=0cKtx291I-E")

                    for track_ in tracks:
                        track = Track(fake[0].id, fake[0].info, requester = ctx.author)
                        track.title, track.uri, track.thumb, track.length = f"{track_['name']} - {track_['artists'][0]['name']}", str(track_['external_urls']['spotify']), track_['album']['images'][0]['url'], track_['duration_ms']
                        controller = self.get_controller(ctx)
                        await controller.queue.put(track)
                    embed = discord.Embed(title = "Enqueued Playlist:",
                                                description = f":play_pause: | __**[{playlist_name}]({playlist_url})**__",
                                                color = discord.Colour.dark_red()
                                         )
                    embed.add_field(name = "Playlist Player", value = f"{ctx.author.mention}")
                    embed.add_field(name = "Number of Tracks", value = f"{len(tracks)}", inline = True)
                    embed.set_thumbnail(url = playlist['images'][0]['url'])
                    await ctx.send(embed = embed)
                
                elif query.startswith("https://open.spotify.com/artist"):
                    artist = sp.artist(query)
                    artist_name = artist['name']
                    artist_url = artist['external_urls']['spotify']
                    tracks = self.spotify_artist(query)
                    fake = await self.bot.wavelink.get_tracks("https://www.youtube.com/watch?v=0cKtx291I-E")

                    for track_ in tracks:
                        track = Track(fake[0].id, fake[0].info, requester = ctx.author)
                        track.title, track.uri, track.thumb, track.length = f"{track_['name']} - {track_['artists'][0]['name']}", str(track_['external_urls']['spotify']), track_['album']['images'][0]['url'], track_['duration_ms']
                        controller = self.get_controller(ctx)
                        await controller.queue.put(track)
                    embed = discord.Embed(title = "Enqueued Playlist:",
                                                description = f":play_pause: | __**[{artist_name}- Top Tracks]({artist_url})**__",
                                                color = discord.Colour.dark_red()
                                         )
                    embed.add_field(name = "Playlist Player", value = f"{ctx.author.mention}")
                    embed.add_field(name = "Number of Tracks", value = f"{len(tracks)}", inline = True)
                    embed.set_thumbnail(url = artist['images'][0]['url'])
                    await ctx.send(embed = embed)     

                elif isinstance(tracks, wavelink.player.TrackPlaylist):
                    tracks_p = tracks.tracks
                    playlist_duration = 0
                    for track_p in tracks_p:
                        track_p = Track(track_p.id, track_p.info, requester = ctx.author)
                        controller = self.get_controller(ctx)
                        await controller.queue.put(track_p)
                        playlist_duration += track_p.length
                    
                    link = str(query)
                    track_embed = discord.Embed(title = "Enqueued Playlist:",
                                                description = f":play_pause: | __**[{tracks.data['playlistInfo']['name']}]({link})**__",
                                                color = discord.Colour.dark_red()
                                               )
                    track_embed.add_field(name = "Playlist Player", value = f"{ctx.author.mention}")
                    track_embed.add_field(name = "Total Duration", value = f"`[{self.format_time(playlist_duration)}]`", inline = True)
                    track_embed.add_field(name = "Number of Tracks", value = f"{len(tracks_p)}", inline = True)
                    await ctx.send(embed = track_embed)
                
                
                elif tracks[0].is_stream:
                    track = Track(tracks[0].id, tracks[0].info, requester = ctx.author)
                    track.length = 0
                    controller = self.get_controller(ctx)
                    await controller.queue.put(track)
                    if player.is_playing:
                        link = str(track.uri)
                        embed = discord.Embed(title = "Enqueued Stream:",
                                        description = f":play_pause: | __**[{str(track)}]({link})**__",
                                        color = discord.Colour.dark_red()
                                        )
                        embed.add_field(name = "Stream Player", value = f"**{ctx.message.author.mention}**")

                    if not player.is_playing:
                        link = str(track.uri)
                        embed = discord.Embed(title = "Playing Stream:",
                                        description = f"**:play_pause: __| [{str(track)}]({link})**__",
                                        color = discord.Colour.dark_red()
                                        )
                        embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")
                    await ctx.send(embed = embed)

                else:
                    track = Track(tracks[0].id, tracks[0].info, requester = ctx.author)

                    controller = self.get_controller(ctx)
                    await controller.queue.put(track)
                    embed = self.play_embed(ctx, track, player)
                    await ctx.send(embed = embed)
                
                
            else:
                tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{query}")
                track = Track(tracks[0].id, tracks[0].info, requester = ctx.author)

            
                controller = self.get_controller(ctx)
                await controller.queue.put(track)
                
                embed = self.play_embed(ctx, track, player)
                await ctx.send(embed = embed)
            if not tracks:
                return await ctx.send(f":grey_question: | No tracks found with this query.")

    @commands.command(aliases = ["scd"],
                      description = "Searches SoundCloud for the query and plays the first result found.",
                      usage = "`.soundcloud [query]`"
                     )
    async def soundcloud(self, ctx, *, query: str):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        if player.channel_id == ctx.author.voice.channel.id:
            tracks = await self.bot.wavelink.get_tracks(f"scsearch:{query}")
            track = Track(tracks[0].id, tracks[0].info, requester = ctx.author)

            controller = self.get_controller(ctx)
            await controller.queue.put(track)
            
            embed = self.play_embed(ctx, track, player)
            await ctx.send(embed = embed)

            if not tracks:
                return await ctx.send(f":grey_question: | No tracks found with this query.")

    @commands.command(aliases = ["sc"],
                      description = "Searches Youtube for the query then returns a list for the first 10 results (to play a result type its number before the timeout of 20 seconds).",
                      usage = "`.search [query]`"
                     )
    async def search(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{query}")

        if not tracks:
            return await ctx.send(f":grey_question: | No tracks found with this query.")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)



        if player.channel_id == ctx.author.voice.channel.id:

            emojis = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:"]
            list_ = zip(emojis, tracks)
            embed = discord.Embed(title = "Search Results:",
                              description = "\n".join(f"{emoji} | **{track}** **`[{self.format_time(track.length)}]`**" for emoji, track in list_),
                              color = discord.Colour.dark_red()
                              )
            embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
            embed.set_footer(text = f"Requested by: {ctx.message.author} | Type the track number to play.", icon_url = ctx.message.author.avatar_url)

            await ctx.send(embed = embed)


            msg = await self.bot.wait_for('message', timeout = 20.0)
            controller = self.get_controller(ctx)
            track = Track(tracks[int(msg.content) - 1].id, tracks[int(msg.content) - 1].info, requester=ctx.author)
            await controller.queue.put(track)
            embed2 = self.play_embed(ctx, track, player)
            await ctx.send(embed = embed2)



    @commands.command(description = "Plays a random Queen song of their greatest songs.",
                      usage = "`.queen`"
                     )
    async def queen(self, ctx):

        playlist = await self.bot.wavelink.get_tracks("https://www.youtube.com/playlist?list=PLIexzKuu-if5FnrlmC0-cCxzLf1GPErAC")
        facts = ["**Freddie** designed the Queen crest, using the astrological signs of the four members: two Leos, one Cancer and one Virgo. Despite this, Freddie claimed not to believe in astrology.",
                 "**Brian**'s guitar (the __Red Special__) is over 200 years old.\nHe and his Dad built it from scratch, using the wood from a 200-year-old mantelpiece.",
                 "The videos for `We Will Rock You` and `Spread Your Wings` were both shot in Roger's backyard.",
                 "The song `Keep Yourself Alive` was released as a single twice, in 1973 and 1975. It failed to make the top 40 both times.",
                 "**Freddie** wrote `Crazy Little Thing Called Love` while in the bath.\nRumour has it that he had his piano moved to his bathside. Did the piano not get wet? Did his bathwater not get cold?",
                 "The loosely-connected duo of albums `A Night At The Opera` and `A Day At The Races` were both named after silent movies by *The Marx Brothers*. The follow-up, `News Of The World`, was named after *Murdoch's* ill-fated rag.",
                 "**Freddie** died on November 24 1991, from Aids related pneumonia\nHe had only publicly announced he was suffering from Aids the day before.",
                 "According to __the Guinness Book Of Records__, *the Official International Queen Fan Club* is the longest running rock group fan club in the world.",
                 "**Brian May** and **Roger Taylor** were playing in the band *Smile* alongside *Tim Staffell*. But *Tim* wasn’t so interested, so recommended his flatmate **Farrokh Bulsara**.\n**Farrokh** became known to the world as **Freddie Mercury**. *Smile* became known to the world as__** Queen**__.",
                 "The band only released `Another One Bites The Dust` as a single because *Michael Jackson* suggested they do so (after dropping by backstage at their LA show).",
                 "__**Queen**__'s collaboration with *David Bowie* on `Under Pressure` wasn't planned, *Bowie* just happened to be by the studio while __**Queen**__ were recording the song.",
                 "In 2002, __**Queen**__ were given the 2,207th star on the *Hollywood Walk Of Fame*.",
                 "As **Freddie** had a famously unusual overbite and distinct front teeth as a result of a malocclusion, he had wanted to fix his overbite for quite some time, but feared the operation would damage his voice.",
                 "**Brian** has a PhD in astrophysics from __Imperial College London__. In 2007, he was appointed __Chancellor of Liverpool John Moores University__.",
                 "__**Queen**__ released a Christmas song in 1984 called `Thank God It’s Christmas` – and it spent six weeks on the Singles Chart, peaking at No. 21.",
                 "**Freddie** had a long-term relationship with *Mary Austin*. However, their relationship ended when he began having an affair with someone else.\n**Freddie** and **Mary** remained close friends, though. He once said of her: “All my lovers asked me why they couldn’t replace *Mary*, but it’s simply impossible. The only friend I’ve got is Mary and I don’t want anybody else.”",
                 "The four tracks **Roger** wrote, were `Radio Ga Ga`, `A Kind of Magic`, `The Invisible Man`, and `These Are the Days of Our Lives`.",
                 "**Freddie** required his assistants to have a pen and paper with them at all times in case he was inspired and needed to jot down some ideas.",
                 "The lyrics for __**Queen**__’s song `Life Is Real` began while the band were flying over the Atlantic from New York.",
                 "In 1999, **Roger** could be seen in the background of a Royal Mail stamp featuring **Freddie**. This caused a stir, since the only living people meant to appear on British stamps are members of the Royal Family.",
                 "**Roger**’s middle name is **Meddows**. Incidentally, he admitted that he “hated the title of the second album, `Queen II`, it was so unimaginative.”",
                 "In his will, **Freddie** is said to have left £500,000 to his chef *Joe Fanelli*, £500,000 to his personal assistant *Peter Freestone* and £100,000 to his driver *Terry Giddings*, I wish I were any of them, not just had the chance to meet him and listen to his voice directly but having this money.",
                 "**John** is not just the band's bassist but also a trained electronics engineer, and he sometimes built equipment for the band to use – including the __Deacy Amp__.",
                 "According to **Freddie**’s friend *David Wigg*, the star believed his stage image prevented him from keeping relationships.\n“I created a monster. I’m handicapped because people think I’m like that. When I’m trying to get a relationship together I’m the nicest person you could meet, my dear. I’m a peach,” he told his friend.",
                 "**Freddie** didn’t think he was a very good pianist, and feared playing `Bohemian Rhapsody` live.",
                 "The __Wembley Live Aid__ show was a platform for performances from some of the UK music industry’s leading lights, including former *Beatle Paul McCartney* and guitar virtuoso *Eric Clapton* – but it was __**Queen**__ that stole the show.\nIn 2005, __**Queen**__'s __Live Aid__ set was voted the greatest rock gig of all time.",
                 "**Freddie**'s ‘bottomless mic’ was one of the singer’s more memorable trademarks, along with his all-white outfits and chevron moustache.\nBut it actually came by total chance, as in one of __**Queen**__'s early shows, **Freddie**'s microphone stand broke – but instead of finding a new one, he held the stand containing the microphone and kept singing and it acted as a great prop for him.",
                 "__**Queen**__ managed to have a total of 26 years in the U.K. Album charts, which is more than any other artist to date.",
                 "__**Queen**__ wrote the soundtrack to the 1980 film `Flash Gordon`, which included the single `Flash.`",
                 "*Paul Rogers* joined __**Queen**__ as a lead singer replacement in 2005 in the __Queen + Paul Rodgers__ tour.",
                 "In 1974, **Brian** was diagnosed with hepatitis after falling in the first month of __**Queen**__'s U.S. tour.",
                 "**John Deacon** was actually the last in a long line of bassists __**Queen**__ tried, including *Douglas Bogie*. He joined in 1971 and is obviously the most famous and longest bassist they have had",
                 "In 2002 __**Queen**__'s `Bohemian Rhapsody` was voted “The UK’s favorite hit of all time” in a poll carried out by __Guinness World Records__.",
                 "**Freddie** chose to have paintings made of his cats. He also loved to call them whilst on tour to chat.",
                 "In 2006 the `Queen Greatest Hits` album became the best-selling album of all time in the U.K. as proven by a study by the __Official UK Charts Company__, beating the likes of *The Beatles* and *Oasis*.",
                 "__**Queen**__ won numerous *Ivor Novello* awards for a range of accolades including their 1974 hit `Killer Queen`, the 1975 worldwide hit `Bohemian Rhapsody`, and their overall outstanding contribution to music"
                ]
        fact = random.choice(facts)
        songs = list(playlist.tracks)
        song = random.choice(songs)
        track = Track(song.id, song.info, requester = ctx.author)

        results = sp.search(q={track}, type='track')
        items = results['tracks']['items']
        if items[0]['album']['id'] == "6i6folBtxKV28WX3msQ4FE":
            sp_track = items[1]
        else:
            sp_track = items[0]
        image_url = sp_track['album']['images'][0]['url']
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        if player.channel_id == ctx.author.voice.channel.id:

            await ctx.send(f":headphones: | I picked you a random queen song, have fun.", delete_after = 5)

            link = str(track.uri)
            embed = self.play_embed(ctx, track, player)
            embed.add_field(name = "Fun Fact", value = f"{fact}[⁽ᴿᵉᶠᵉʳᵉⁿᶜᵉ⁾](https://www.nme.com/photos/50-geeky-facts-about-queen-1419950)")
            embed.set_thumbnail(url = image_url)
            await ctx.send(embed = embed)
            controller = self.get_controller(ctx)
            await controller.queue.put(track)

    @commands.command(aliases = ["np", "Now"],
                      description = "Returns an embed containing information about the currently playing song and track looping state.",
                      usage = "`.nowplaying`"
                     )
    async def nowplaying(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if not player.current:
            return await ctx.send(":question: | Nothing is currently playing, I guess you have to play a track first.")

        if player.current.is_stream:
            track_length = "0:00:00"
            track_position = "0:00:00"
            track_left = " ∞ "
            player_tracker = "🔴▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬🔴"
        else:
            track_length = self.format_time(player.current.length)
            track_position = self.format_time(player.position)
            time_left = int(player.current.length) - int(player.position)
            track_left = self.format_time(time_left)

            player_tracker = ""
            
            length = round(player.current.length // 20) 
            position = round(player.position // length)
            
            for i in range(20):
                if i == position:
                   player_tracker += ":radio_button:" 
                else:
                   player_tracker += "▬"

        if controller.loop_state == "1":
            loop_state = "Enabled"
        else:
            loop_state = "Disabled"

        embed = discord.Embed(title = "Now Playing:",
                              description = f":play_pause: | __**[{player.current.title}]({player.current.uri})**__ \n\n[{track_position} {player_tracker} {track_length}]",
                              color = discord.Colour.dark_red()
                              )
        embed.add_field(name = "Track Player", value = f"{player.current.requester.mention}")
        embed.add_field(name = "Time Left", value = f"`[{track_left}]`")
        embed.add_field(name = "Track Loop", value = f"{loop_state}")
        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["repeat"],
                     description = "Changes the player's loop state depending on the specified state, there are 3 states activated respectively when no state is specified which are:\nQueue looping, Track looping, Disabled.",
                     usage = "`.loop\n.loop 'queue'/'all'/'on'\n.loop 'track'/'one'/'current'\n.loop 'off'/'disable'/'stop'`"
                     )
    async def loop(self,ctx, state : str = None):
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if player.channel_id == ctx.author.voice.channel.id:
            if player.current:
                try:
                    controller.previous.pop(0)
                except IndexError:
                    pass
                controller.previous.append(player.current)

                if state is None:
                    if controller.loop_state == "0" :
                        controller.loop_state = "2"
                        message = ":repeat: | Queue looping has been **enabled**."
                    elif controller.loop_state == "2" :
                        controller.loop_state = "1"
                        message = ":repeat_one: | Track looping has been **enabled**."
                    elif controller.loop_state == "1" :
                        controller.loop_state = "0"
                        message = ":arrow_right: | Looping has been **disabled**."
                else:
                    if state.lower() in ["queue", "all", "on"]:
                        controller.loop_state = "2"
                        message = ":repeat: | Queue looping has been **enabled**."
                    elif state.lower() in ["track", "one", "current"]:
                        controller.loop_state = "1"
                        message = ":repeat_one: | Track looping has been **enabled**."
                    elif state.lower() in ["off", "disable", "stop"]:
                        controller.loop_state = "0"
                        message = ":arrow_right: | Looping has been **disabled**."

                await ctx.send(message)
            else:
                await ctx.send(":question: | You have to play a track first.")

    @commands.command(aliases = ["ls"],
                      description = "Returns the lyrics depending on the input query, if no input then returns the lyrics of the currently playing track, lyrics source is KSoft.Si API.",
                      usage = "`.lyrics\n.lyrics [query]`"
                     )
    async def lyrics(self, ctx, *, query : str = None):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if query is None:
            query = str(player.current)
        if query == 'None':
            await ctx.send(f":question: | Please either play a song or write its name.")
        try:
            if query != "None":
                results = await kclient.music.lyrics(query)
        except ksoftapi.NoResults:
            await ctx.send(":question: | No lyrics found for this query")
        else:
            first = results[0]

        embed = discord.Embed(title = "Lyrics:",
                             description = f"__**{first.name} - {first.artist}**__ \n{first.lyrics}"[:2047],
                             color = discord.Colour.dark_red()          
                             )
        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
        embed.set_thumbnail(url = first.album_art)
        embed.set_footer(text = f"Requested by: {ctx.message.author}\nPowered by: KSoft.Si", icon_url = ctx.message.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["lsg"],
                      description = "Returns the lyrics depending on the input query, if no input then returns the lyrics of the currently playing track, lyrics source is Genius.",
                      usage = "`.lyricsgenius\n.lyricsgenius [query]`")
    async def lyricsgenius(self, ctx, *, query : str = None):
        await ctx.channel.trigger_typing()
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if query is None:
            query = str(player.current)
        if query == 'None':
            await ctx.send(f":question: | Please either play a song or write its name.")
        if query != "None":
            song = gn.search_song(query)
        try:
            song_obj = gn.song(song_id = song.id)
        except:
            await ctx.send(":question: | No lyrics found for this query")
        else:

            cover = song_obj['song']['song_art_image_url']
            artist = song.artist
            url = song.url
            name = song.title
            lyrics = song.lyrics

        embed = discord.Embed(title = "Lyrics:",
                             description = f"__**[{name} - {artist}]({url})**__ \n{lyrics}"[:2047],
                             color = discord.Colour.dark_red()          
                             )
        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
        embed.set_thumbnail(url = cover)
        embed.set_footer(text = f"Requested by: {ctx.message.author}\n", icon_url = ctx.message.author.avatar_url)

        await ctx.channel.trigger_typing()
        await ctx.send(embed = embed)
    @commands.command(aliases = ["q"],
                      description = "Returns the server's queued tracks.",
                      usage = "`.queue`"
                     )
    async def queue(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        upcoming = list(itertools.islice(controller.queue._queue, 0, None))

        if not player.current:
            await ctx.send(":question: | There are no tracks currently in the queue, you can add more tracks with the `play` command.")
        else:
            entries = upcoming
            pages = PaginatorSource(entries=entries, ctx = ctx, player = player, controller = controller, bot = self.bot)
            paginator = menus.MenuPages(source=pages, timeout=None, delete_message_after=True)

            await paginator.start(ctx)
        


    @commands.command(aliases = ["mix"],
                      description = "Shuffles the queue, it must contain more than 3 tracks to be shuffled in a right way.",
                      usage = "`.shuffle`"
                     )
    async def shuffle(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if player.channel_id == ctx.author.voice.channel.id:
            if player.current:
                if controller.queue.qsize() < 3:
                    return await ctx.send(":no_entry: | You need more than 3 tracks in your queue to shuffle.")
                else:
                    random.shuffle(controller.queue._queue)
                    await ctx.send(":twisted_rightwards_arrows: | Your queue has been shuffled.")
            else:
                await ctx.send(f":question: | You need to put more tracks in your queue to shuffle.")

    @commands.command(aliases = ["eq"],
                      description = "Displays the currently applied equalizer or changes the player's equalizer depending on the specified name, the current equalizers are:\nDefault, Boost, Metal, Piano.",
                      usage = "`.equalizer\n.equalizer [equalizer name]`"
                     )
    async def equalizer(self, ctx: commands.Context, *, equalizer: str = None):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        vote = await self.has_voted(ctx)
        if vote != False:
            if not player.is_connected:
                return
            if player.channel_id == ctx.author.voice.channel.id:
    
                if player.current:
                    if equalizer is None:
                        if player.equalizer.name == "Flat":
                            eq_name = "default"
                        else:
                            eq_name = player.equalizer.name
                        await ctx.send(f":level_slider: | The currently applied equalizer is **{str(eq_name).capitalize()}**.")
                    else:
                        eqs = {'default': wavelink.Equalizer.flat(),
                               'boost': wavelink.Equalizer.boost(),
                               'metal': wavelink.Equalizer.metal(),
                               'piano': wavelink.Equalizer.piano()}
                
                        eq = eqs.get(equalizer.lower(), None)
    
                        if not eq:
                            keys = list(eqs)
                            list_ = ", ".join(f"`{key.capitalize()}`" for key in keys)
                            return await ctx.send(f":no_entry: | You have entered a wrong equalizer name, currently available equalizers are:\n{list_}.")
                        await ctx.send(f":level_slider: | **{equalizer.capitalize()}** equalizer has been applied.")
                        await player.set_eq(eq)
                else:
                    await ctx.send(f":question: | You can't apply an equializer without playing a song.")


    @commands.command(description = "Applies nightcore effect on the player, rate of nightcore depends on your input which must be more than 1 (decimals like: 1.1, 2.35 are allowed).",
                      usage = "`.nightcore [rate]`"
                     )
    async def nightcore(self, ctx, *, rate : float):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        vote = await self.has_voted(ctx)
        if vote != False:
            if not player.is_connected:
                return
            if player.channel_id == ctx.author.voice.channel.id:
                if rate < 1:
                    await ctx.send(f":question: | The rate has to be more than 1, You can use `.vapourwave` instead.")
                else:
                    filter_ = wavelink.Timescale(rate = rate)
                    await player.set_filter(filter = wavelink.Filter(timescale = filter_))
                    await ctx.send(f":cd: | Nightcore filter has been set to **{rate}**.")


    @commands.command(aliases = ["vaporwave"],
                      description = "Applies vapourwave effect on the player, rate of vapourwave depends on your input which must be less than 1 (decimals like: 0.1, 0.25 are allowed).",
                      usage = "`.vapourwave [rate]`"
                     )
    async def vapourwave(self, ctx, *, rate : float):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        vote = await self.has_voted(ctx)
        if vote != False:
            if not player.is_connected:
                return
            if player.channel_id == ctx.author.voice.channel.id:
                if rate > 1:
                    await ctx.send(f":question: | The rate has to be less than 1, You can use `.nightcore` instead.")
                else:
                    filter_ = wavelink.Timescale(rate = rate)
                    await player.set_filter(filter = wavelink.Filter(timescale = filter_))
                    await ctx.send(f":dvd: | Vapourwave filter has been set to **{rate}**.")


    @commands.command(description = "Changes the pitch of the tracks, it could be higher or lower depending on the pitch you choose.",
                      usage = "`.pitch [pitch]`"
                     )
    async def pitch(self, ctx, *, pitch : float):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        vote = await self.has_voted(ctx)
        if vote != False:
            if not player.is_connected:
                return
            if player.channel_id == ctx.author.voice.channel.id:
                filter_ = wavelink.Timescale(pitch = pitch)
                await player.set_filter(filter = wavelink.Filter(timescale = filter_))
                await ctx.send(f":control_knobs: | The pitch has been changed to **{pitch}**")


    @commands.command(description = "Changes the pitch of the tracks, it could be higher or lower depending on the pitch you choose.",
                      usage = "`.pitch [pitch]`"
                     )
    async def speed(self, ctx, *, speed : float):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        vote = await self.has_voted(ctx)
        if vote != False:
            if not player.is_connected:
                return
            if player.channel_id == ctx.author.voice.channel.id:
                filter_ = wavelink.Timescale(speed = speed)
                await player.set_filter(filter = wavelink.Filter(timescale = filter_))
                await ctx.send(f":control_knobs: | The speed has been changed to **{speed}**")

    @commands.command(aliases = ["vol"],
                      description = "Displays the current volume, or changes the player's volume depending on the level input which must be an integer between 0 and 1000.",
                      usage = "`.vol\n.vol [level]`"
                     )
    async def volume(self, ctx, *, vol: int = None):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        vote = await self.has_voted(ctx)
        if player.channel_id == ctx.author.voice.channel.id:
            if vote != False:
                if vol is None:
                    await ctx.send(f":loud_sound: | The current player volume is `{player.volume}`.")
                else:
                    controller = self.get_controller(ctx)
                    vol = max(min(vol, 1000), 0)
                    controller.volume = vol

                await ctx.send(f":loud_sound: | Setting the player volume to `{vol}`.")
                await player.set_volume(vol)


    @commands.command(description = "Seeks the current track to the specified position, position must be in seconds.",
                      usage = "`.seek [position]`"
                     )
    async def seek(self, ctx,* , position = 0):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.channel_id == ctx.author.voice.channel.id:
            await player.seek(position = position * 1000)

            if not player.is_playing:
                await ctx.send(f":question: | Nothing is currently playing.")

            if player.is_playing:
                if player.current.is_stream:
                    await ctx.send(f":no_entry_sign: | You can't seek in a live stream.")
                else:
                    await ctx.send(f":fast_forward: | Your track has been seeked to **`[{self.format_time(position * 1000)}]`**.")

    @commands.command(aliases = ["s"],
                      description = "Skips to the next track in the queue or stops if no tracks were added to the queue.",
                      usage = "`.skip`"
                     )
    async def skip(self, ctx, number : int = 1):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.channel_id == ctx.author.voice.channel.id:
            if player.current:
                await ctx.send(f":track_next: | The current track has been skipped.")
            if not player.is_playing:
                await ctx.send(f":question: | There is no current track to skip.")
            await player.stop()

    @commands.command(aliases = ["cq"],
                      description = "Clears the queue and the current track.",
                      usage = "`.clearqueue`"
                     )
    async def clearqueue(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if player.channel_id == ctx.author.voice.channel.id:
            if not player.current or not controller.queue._queue:
                await ctx.send(f":no_entry: | You can't clear an empty queue.")
            else:
                await player.stop()
                controller.queue._queue.clear()
                await ctx.send(":wastebasket: | Your queue has been cleared.")

    @commands.command(aliases = ["r"],
                     description = "Removes a track from the queue depending on the number entered.",
                     usage = "`.remove [track number]`"
                     )
    async def remove(self, ctx, number : int):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if player.channel_id == ctx.author.voice.channel.id:
            if not controller.queue._queue:
                await ctx.send(f":no_entry: | You can't remove an item from an empty queue.")
            else:
                if number == 0:
                    await player.stop()
                else:
                    value = controller.queue._queue[number - 1]
                    await ctx.send(f":track_next: | **{value.title}** has been removed.")
                    controller.queue._queue.remove(value)
            
    @commands.command(aliases = ["st"],
                      description = "Skips to a specified song in the queue removing all the songs before it.",
                      usage = "`.skipto [track number]`"
                     )
    async def skipto(self, ctx, number : int):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if player.channel_id == ctx.author.voice.channel.id:
            if not controller.queue._queue:
                await ctx.send(f":no_entry: | You can't skip an item from an empty queue.")
            else:
                number = number - 1
                for n in range(number):
                    value = controller.queue._queue[0]
                    controller.queue._queue.remove(value)
                await player.stop()
                await ctx.send(f":track_next: | Player has skipped to **{controller.queue._queue[0].title}**.")

    @commands.command(description = "Moves a song in the queue to a new position depending on the input.",
                      usage = "`.move [track position] [new position]`"
                     )
    async def move(self, ctx, track : int, pos : int):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if player.channel_id == ctx.author.voice.channel.id:
            if not controller.queue._queue:
                await ctx.send(f":no_entry: | You can't move an item from an empty queue.")
            else:
                pos = pos - 1
                track = track - 1
                value = controller.queue._queue[track]
                controller.queue._queue.remove(value)
                controller.queue._queue.insert(pos, value)
                await ctx.send(f"**:track_next: | {value.title}** has been moved to position **{pos + 1}**")

    @commands.command(description = "Pauses the player untill it's resumed again.",
                      usage = "`.pause`"
                     )
    async def pause(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.channel_id == ctx.author.voice.channel.id:
            if not player.is_paused:
                await ctx.send(f":pause_button: | Player has been paused.")
            await player.set_pause(pause = True)

    @commands.command(description = "Resumes the player.",
                      usage = "`.resume`"
                     )
    async def resume(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.channel_id == ctx.author.voice.channel.id:
            if player.is_paused:
                await ctx.send(f":arrow_forward: | Player has been resumed.")
            await player.set_pause(pause = False)


    @commands.command(aliases = ["sp"],
                      description = "Stops the player, clears the queue, and disconnects the bot from the voice channel.",
                      usage = "`.stop`"
                     )
    async def stop(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.channel_id == ctx.author.voice.channel.id:
            try:
                del self.controllers[ctx.guild.id]
            except KeyError:
                await player.disconnect()
                return await ctx.send(":question: | There was no controller to stop.")

            await player.destroy()
            await ctx.send(f":stop_button: | Player has stopped and disconnected.")

    @commands.command(aliases = ["dc", "leave"],
                      description = "Disconnects the bot from the voice channel without clearing the queue but pausing the current track untill it connects again..",
                      usage = "`.disconnect`"
                     )
    async def disconnect(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            channel = ctx.author.voice.channel

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if player.channel_id == ctx.author.voice.channel.id:
            if player.is_connected:
                await ctx.send(f":eject: | Disconnecting from **`{channel.name}`**.")
            await player.set_pause(pause = True)
            await player.disconnect()

def setup(client):
    client.add_cog(Music(client))

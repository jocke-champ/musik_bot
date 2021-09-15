import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #allt musikrelaterat
        self.is_playing = False

        # 2d -array som innehåller [låt, kanal]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

     #söker objektet på youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #hämtar första url:en
            m_url = self.music_queue[0][0]['source']

            #ta bort det första elementet när du spelar det
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #försök att ansluta till röstkanalen om du inte redan är ansluten

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            #ta bort det första elementet när du spelar det
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="p", help="Spelar en låt från youtube")
    async def p(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #du måste vara ansluten så att boten vet vart den ska gå
            await ctx.send("Gå med i en röstkanal, din sussy baka!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Kunde inte ladda in sången, kan vara för att det är en spellista eller livestream, sånt kan jag inte ;(")
            else:
                await ctx.send("La till sången till kön :)")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="k", help="Visar sånger i kön")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Ingen musik i kön :(")

    @commands.command(name="s", help="Skippar låten som spelas")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            #försäker spela nästa sång i kön
            await self.play_music()

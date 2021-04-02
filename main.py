import discord
from discord.ext import commands
from pretty_help import PrettyHelp # Because I'm lazy
import os
import datetime

client = commands.Bot(command_prefix="+", help_command=PrettyHelp())
token = os.getenv("DISCORD_BOT_TOKEN")


@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("me por modir"))
    print("Discord bot ready")



@client.command(
        name="ping",
        description="What do you think this would be?",
        brief="Check the bot's ping"
)
async def ping(ctx):
    await ctx.send(f"🏓 Pong, that took {int(client.latency * 1000)}ms")

@client.command(
        name="pong",
        description="This is like ping but with a surprise",
        brief="Like ping but with a surprise"
)
async def pong(ctx):
    await ctx.send(f"🏓 Ping, that took {int(client.latency * 1000)}ms"[::-1])

@client.command(
        name="whoami",
        description="Who am I? Who are you!? WHERE AM I?!? WHY AM I HERE?!?1?!1?!",
        brief="Who are you?"
)
async def whoami(ctx):
    await ctx.send(f"You're {ctx.message.author.name}, dum dum")



@client.command(
        name="idea",
        description="Suggest an idea for the app or the server",
        brief="Suggest an idea"
)
async def idea(ctx, idea_for="app", idea=None):
    channel = None

    if idea_for == "server":
        channel = client.get_channel(826514832005136465)

    elif idea_for == "app":
        channel = client.get_channel(790687893701918730)

    else:
        await ctx.send("Hey, the 1st parameter can only be \"app\" (suggest something for the mod) or \"server\" (suggest something for the server).")
        return

    if idea == None:
        await ctx.send("Hey, can you put your idea on the 2rd argument?")
        return

    emojis = ['⬆️', '⬇️']

    embed = discord.Embed(description="**Idea:** " + idea, color=0x1891fb)
    embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text="Send +idea " + idea_for + " \"your idea\" in <#814828261044650064> to do this")

    message = await channel.send(embed=embed)

    await ctx.message.delete()
    
    for emoji in emojis:
        await message.add_reaction(emoji)

@client.command(
        name="purge",
        description="Delete messages, I guess",
        brief="Delete messages"
)
async def purge(ctx, amount=1):
    if ctx.message.author.guild_permissions.manage_messages or ctx.message.author.name == "Iyxan23":
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(content="Purged " + str(amount) + " messages", delete_after=10)
    else:
        await ctx.send("oi mate, ya don't have the manage messages permission", delete_after=5)



@client.event
async def on_reaction_add(reaction, user):
    emojis = ['⬆️', '⬇️']

    # Check if this is us 
    if reaction.message.author == client.user and user != client.user:
        if reaction.emoji in emojis:
            for react_ in reaction.message.reactions:
                if react_.emoji == reaction.emoji:
                    continue

                users = await react_.users().flatten()
                if user in users:
                    await reaction.message.remove_reaction(react_.emoji, user)
                    return

client.run(token)

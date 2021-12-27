import discord

COLOR_ERROR = 0xff0000
COLOR_SUCCESS = 0x00ff00

def print_error(ctx, type, message):
    embed = discord.Embed(title="ERROR", color=COLOR_ERROR)
    embed.add_field(name=type, value=message, inline=False)
    polish_message(ctx, embed)
    return embed

def polish_message(ctx, embed):
    embed.set_footer(text=f"Responding to {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
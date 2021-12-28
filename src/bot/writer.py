import discord

COLOR_ERROR = 0xcc0000
COLOR_SUCCESS = 0x009e0c

def print_error(ctx, type, message):
    embed = discord.Embed(title="ERROR", color=COLOR_ERROR)
    embed.add_field(name=type, value=message, inline=False)
    polish_message(ctx, embed)
    return embed

def polish_message(ctx, embed):
    embed.set_footer(text=f"Responding to {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
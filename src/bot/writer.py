import discord

def print_error(ctx, type, message):
    embed = discord.Embed(title="ERROR", color=0xff0000)
    embed.add_field(name=type, value=message, inline=False)
    polish_message(ctx, embed)
    return embed

def polish_message(ctx, embed):
    embed.set_footer(text=f"Responding TO {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
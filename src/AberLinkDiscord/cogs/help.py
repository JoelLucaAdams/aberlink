import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.buttons import Paginator

from cogs import admin_roles, emojis
from AberLink import logger as logging

def setup(bot):
    bot.add_cog(Help(bot))

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass

class Help(commands.Cog):
    """
    Marking attendance of students during Discord practicals
    """

    def __init__(self, bot):
        self.bot = bot
        self.cmds_per_page = 3

    def get_command_signature(self, command: commands, ctx: Context):
        aliases = "|".join(command.aliases)
        cmd_invote = f'[{command.name} | {aliases}]' if command.aliases else command.name

        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f'{ctx.prefix}{full_invoke}{cmd_invote} {command.signature}'
        return signature 

    async def return_filtered_commands(self, walkabe, ctx: Context):
        filtered = []

        for c in walkabe.walk_commands():
            try:
                if c.hidden:
                    continue
                elif c.parent:
                    continue

                await c.can_run(ctx)
                filtered.append(c)
            except commands.CommandError:
                continue
        return self.return_sorted_commands(filtered)

    def return_sorted_commands(self, commandList):
        return sorted(commandList, key=lambda x: x.name)

    async def setup_help_pag(self, ctx: Context, entity=None, title=None):
        entity = entity or self.bot
        title = title or self.bot.description

        pages = []

        if isinstance(entity, commands.Command):
            filtered_commands = (list(set(entity.all_commands.values()))
            if hasattr(entity, "all_commands")
            else []
            )
        else:
            filtered_commands = await self.return_filtered_commands(entity, ctx)

        for i in range(0, len(filtered_commands), self.cmds_per_page):
            next_commands = filtered_commands[i: i + self.cmds_per_page]
            commands_entry = ""

            for cmd in next_commands:
                description = cmd.short_doc or cmd.description
                signature = self.get_command_signature(cmd, ctx)
                subcommand = 'Has subcommands' if hasattr(cmd, 'all_commands') else ''

                commands_entry += (
                    f'• **__{cmd.name}__**\n ```\n{signature}\n```\n{description}\n'
                    if isinstance(entity,  commands.Command)
                    else f'• **__{cmd.name}__**\n{description}\n    {subcommand}'
                )
                pages.append(commands_entry)

            await Pag(title=title, color=discord.Colour.blue(), entries=pages, length=10).start(ctx)


    '''@commands.command()
    async def help(self, ctx: Context, *, entity=None):
        """
        """
        if not entity:
            await self.setup_help_pag(ctx)'''



    '''@commands.command()
    async def help(self, ctx: Context, cog='1'):
        """
        Marks the student as present in the practical
        """
        helpEmbed = Embed(title='Help command', colour=discord.Colour.blue())
        helpEmbed.set_thumbnail(url=ctx.author.avatar_url)

        # Gets a list of all cogs
        cogs = [c for c in self.bot.cogs.keys()]

        totalPages = math.ceil(len(cogs) / 2)

        cog = int(cog)

        if cog > totalPages or cog < 1:
            await ctx.send(f"Invalid page number `{cog}` Please pick from `{totalPages}` pages.")
            return

        neededCogs = []
        for i in range(2):
            x = i + (int(cog) - 1) * 2
            try:
                neededCogs.append(cogs[x])
            except IndexError:
                pass

        for cog in neededCogs:
            commandList = ""
            for command in self.bot.get_cog(cog).walk_commands():
                if command.hidden:
                    continue
                elif command.parent != None:
                    continue

                commandList += f'**{command.name}** - {command.__doc__}'

            commandList += '\n'

            helpEmbed.add_field(name=cog, value=commandList, inline=False)

        await ctx.send(embed=helpEmbed)'''

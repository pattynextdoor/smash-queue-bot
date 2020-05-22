import discord
from discord.ext import commands
from .helpers.queue_helper import Queue

class QueueManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queues = set() 

    # Listeners

    @commands.Cog.listener()
    async def on_ready(self):
        uname = self.client.user.name
        uid = self.client.user.id
        print(f'Initialized {uname} with id {uid}')

    # Commands
    @commands.command()
    async def open(self, ctx, *args):
        author_uname = ctx.message.author.name
        new_queue = None

        if (args):
            new_queue = Queue(args[0], author_uname)
        else:
            new_queue = Queue(author_uname, author_uname)

        self.queues.add(new_queue)

        await ctx.send(f'New queue created with name `{new_queue.name}`')

    @commands.command()
    async def list(self, ctx, *args):
        def generate_queue_list_string(self):
            list_str = ''

            for queue in self.queues:
                list_str += f'\n{queue.name}\n'
            return list_str

        full_str = ("```Current active queues:"
                    "---------------"
                     f"{generate_queue_list_string(self)}\n"
                     "Need a list of players in a queue instead? Try \"q!list <queue_name>\"```")

        await ctx.send(full_str)



def setup(client):
    client.add_cog(QueueManager(client))
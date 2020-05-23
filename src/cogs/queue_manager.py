import discord
from discord.ext import commands
from .helpers.queue_helper import Queue

class QueueManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queues = {} 

    # Listeners

    @commands.Cog.listener()
    async def on_ready(self):
        uname = self.client.user.name
        uid = self.client.user.id
        print(f'Initialized {uname} with id {uid}')

    # Commands

    @commands.command()
    async def open(self, ctx, *args):
        """ Opens a new queue"""
        def is_queue_open(author):
            for queue in self.queues.values():
                if queue.owner == author:
                    return True
            return False

        author_uname = ctx.message.author.name

        if is_queue_open(author_uname):
            await ctx.send(f'Player `{author_uname}` already has an active queue open.')
            return

        name = args[0] if args else author_uname # If no queue_name argument is specified, then we can default it to the owner's username
        new_queue = Queue(name, author_uname)

        self.queues.update({new_queue.name: new_queue})

        await ctx.send(f'New queue created with name `{new_queue.name}`')

    @commands.command()
    async def list_queues(self, ctx):
        """ Lists all active queues """
        if len(self.queues) == 0:
            await ctx.send('There are no active queues.')
            return

        else: 
            full_str = (', '.join(list(self.queues.keys())))
            await ctx.send(f'Active queues: {full_str}')

    @commands.command()
    async def list(self, ctx, *args):
        """ List all players in a given queue """
        if (len(args) == 0):
            await ctx.send('To list the players in a queue, please specify a queue_name. Example: `!list myQueue`')
            return

        q_name = args[0]
        uname = ctx.message.author.name

        try:
            spec_queue = self.queues[q_name]
        except KeyError:
            await ctx.send(f'Could not find the given queue `{q_name}`.')

        if len(spec_queue.list) == 0:
            await ctx.send(f'Queue `{q_name}` is currently empty!')
            return
        else:
            full_str = (', '.join(spec_queue.list))
            await ctx.send(f'Players in queue {q_name}: {full_str}')


    @commands.command()
    async def join(self, ctx, *args):
        """ Join a given queue """
        if len(args) == 0:
            await ctx.send('No queue name specified! Example: `q!join myqueue`')
            return
        else:
            q_name = args[0]
            uname = ctx.message.author.name

            if not self.__queue_exists(q_name, self.queues):
                await ctx.send(f'Could not find the given queue `{q_name}`.')
                return

            spec_queue = self.queues[q_name]

            try:
                spec_queue.add(uname)
                await ctx.send(f'`{uname}` has been added to the queue `{spec_queue.name}`.')
            except RuntimeError:
                if (len(spec_queue.list) == spec_queue.cap):
                    await ctx.send(f'Could not add new player `{uname}` to the queue `{spec_queue.name}` due to a full capacity of `{spec.queue.cap}`')
                else:
                    await ctx.send(f'Player `{uname}` is already in the queue `{spec_queue.name}`.')
    
    @commands.command()
    async def leave(self, ctx, *args):
        """ Leave a given queue """
        if len(args) == 0:
            await ctx.send('No queue name specified! Example: `q!leave myqueue`')        
            return
        else:
            q_name = args[0]
            uname = ctx.message.author.name

            if not self.__queue_exists(q_name, self.queues):
                await ctx.send(f'Could not find the given queue `{q_name}`.')
                return
            
            spec_queue = self.queues[args[0]]

            try:
                spec_queue.remove(uname)
                await ctx.send(f'`{uname}` has been removed from the queue `{spec_queue.name}`')
            except RuntimeError:
                await ctx.send(f'`{uname}` is not in the queue.')

    @commands.command()
    async def next(self, ctx, *args):
        """Cycle the queue to the next challenger"""
        if len(args) == 0:
            await ctx.send('No queue name specified! Example: `q!next myqueue`')
            return
        else:
            q_name = args[0]
            uname = ctx.message.author.name

            if not self.__queue_exists(q_name, self.queues):
                await ctx.send(f'Could not find the given queue `{q_name}`.')
                return
            elif self.queues[q_name].owner != uname:
                await ctx.send(f'Only the owner `{self.queues[q_name].owner}` can make changes to this queue.')
                return
            else:
                spec_queue = self.queues[q_name]
                most_recent_player = spec_queue.list[0]
                spec_queue.remove(most_recent_player)
                spec_queue.add(most_recent_player)
                await ctx.send(f'Queue `{q_name}` has been rotated.')


    def __queue_exists(self, q_name, q_map):
        return q_name in q_map.keys()

def setup(client):
    client.add_cog(QueueManager(client))
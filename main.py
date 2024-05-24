from guilded.ext import commands
from db import *
from loguru import logger
import guilded as nextcord
import os
import dotenv

dotenv.load_dotenv()

logger.add("tasky.log")

bot = commands.Bot(command_prefix="!")

@bot.command(name="list")
async def list(ctx: commands.Context):
    tasks = Task.select().where(Task.user == ctx.author.id)
    desc = ""

    for task in tasks:
        if task.done:
            desc += "✅ "
        else:
            desc += "❌ "

        desc += f"{task.task} ({task.id})\n"

    embed = nextcord.Embed(
        title=f"{ctx.author.display_name}'s tasks",
        description=desc,
        color=nextcord.Color.green()
    )

    embed.set_thumbnail(url=ctx.author.display_avatar)

    await ctx.send(embed=embed)

@bot.command(name="add")
async def add(ctx: commands.Context, *, task: str):
    user = ctx.author.id

    task = Task.create(task=task, user=user)

    embed = nextcord.Embed(
        title="Task created!",
        description=task.task,
        color=nextcord.Color.green()
    )

    logger.info(f"{ctx.author.display_name} added a task: {task.task}")

    embed.set_footer(text=f"Task ID: {task.id}")
    embed.set_thumbnail(url=ctx.author.display_avatar)

    await ctx.send(embed=embed)

@bot.command(name="delete", description="Delete a task")
async def delete(ctx: commands.Context, id: int):
    task = Task.select().where(Task.user == ctx.author.id, Task.id == id)

    if task:
        task = task[0]
    else:
        await ctx.send(content="Task not found!")
        return

    embed = nextcord.Embed(
        title="Task deleted!",
        description=task.task,
        color=nextcord.Color.red()
    )

    logger.info(f"{ctx.author.display_name} deleted a task: {task.task}")

    embed.set_footer(text=f"Task ID: {task.id}")
    embed.set_thumbnail(url=ctx.author.display_avatar)
    task.delete_instance()

    await ctx.send(embed=embed)

@bot.command(name="mark", description="Mark or unmark a task")
async def mark(ctx: commands.Context, id: int):
    task = Task.select().where(Task.id == id, Task.user == ctx.author.id)

    if task:
        task = task[0]
    else:
        await ctx.send(content="Task not found!")
        return

    task.done = not task.done
    task.save()

    if task.done:
        embed = nextcord.Embed(
            title="Task marked!",
            description=task.task,
            color=nextcord.Color.green()
        )
        logger.info(f"{ctx.author.display_name} marked a task: {task.task}")
    else:
        embed = nextcord.Embed(
            title="Task unmarked!",
            description=task.task,
            color=nextcord.Color.red()
        )
        logger.info(f"{ctx.author.display_name} unmarked a task: {task.task}")

    embed.set_footer(text=f"Task ID: {task.id}")
    embed.set_thumbnail(url=ctx.author.display_avatar)

    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    logger.info(f"{bot.user.display_name} up!")

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
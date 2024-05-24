from nextcord.ext import commands
from db import *
from loguru import logger
import nextcord
import os
import dotenv

dotenv.load_dotenv()

logger.add("tasky.log")

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.slash_command(name="list", description="List your tasks")
async def list(ctx: nextcord.Interaction):
    tasks = Task.select().where(Task.user == ctx.user.id)
    desc = ""

    for task in tasks:
        if task.done:
            desc += "✅ "
        else:
            desc += "❌ "

        desc += f"{task.task} ({task.id})\n"

    embed = nextcord.Embed(
        title=f"{ctx.user.display_name}'s tasks",
        description=desc,
        color=nextcord.Color.green()
    )

    embed.set_thumbnail(url=ctx.user.display_avatar)

    await ctx.send(embed=embed)

@bot.slash_command(name="add", description="Add a task")
async def add(ctx: nextcord.Interaction, task: str):
    user = ctx.user.id

    task = Task.create(task=task, user=user)

    embed = nextcord.Embed(
        title="Task created!",
        description=task.task,
        color=nextcord.Color.green()
    )

    logger.info(f"{ctx.user.display_name} added a task: {task.task}")

    embed.set_footer(text=f"Task ID: {task.id}")
    embed.set_thumbnail(url=ctx.user.display_avatar)

    await ctx.send(embed=embed)

@bot.slash_command(name="delete", description="Delete a task")
async def add(ctx: nextcord.Interaction, id: int):
    task = Task.select().where(Task.user == ctx.user.id, Task.id == id)

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

    logger.info(f"{ctx.user.display_name} deleted a task: {task.task}")
    
    embed.set_footer(text=f"Task ID: {task.id}")
    embed.set_thumbnail(url=ctx.user.display_avatar)
    task.delete_instance()

    await ctx.send(embed=embed)

@bot.slash_command(name="mark", description="Mark or unmark a task")
async def mark(ctx: nextcord.Interaction, id: int):
    task = Task.select().where(Task.id == id, Task.user == ctx.user.id)

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
        logger.info(f"{ctx.user.display_name} marked a task: {task.task}")
    else:
        embed = nextcord.Embed(
            title="Task unmarked!",
            description=task.task,
            color=nextcord.Color.red()
        )
        logger.info(f"{ctx.user.display_name} unmarked a task: {task.task}")

    embed.set_footer(text=f"Task ID: {task.id}")
    embed.set_thumbnail(url=ctx.user.display_avatar)

    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    logger.info(f"{bot.user.display_avatar} up!")

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
import discord,os,platform,sys,requests,json;
from discord import app_commands;
from discord.ext import commands;
from discord.ext.commands import MemberConverter;
from datetime import datetime, timedelta;

#Bot User agent
user_agent=f"SuperDuperBot/5.0 ({platform.system()}) (compatible: SuperDuperBot [{platform.machine()}]))";
#Bot owner
owner_user="YOUR_USERNAAME";
# Event Webservice URL
webservice_url="URL_HERE";
# Intents
intents = discord.Intents.default();
intents.message_content = True;

# Bot setup
bot = commands.Bot(command_prefix='!', intents=intents);
def print_err(e):
    print(f"\033[1;31m{e}\033[0m");
##end
def sendRequest(url,auth):
    heads={
        "User-Agent":user_agent,
        "Authorization":f"Bearer {auth}",
        "Content-Type":"application/json",
        "Accepts":"application/json",
    };
    try:
        response = requests.get(url,headers=heads);
        response.raise_for_status();  # Raise an HTTPError for bad responses
    except requests.exceptions.HTTPError as http_err:
        print_err(f"[ ERROR ]: Request to {url} failed with response code {response.status_code} (HTTP: {http_err})");
        return None;
    except Exception as err:
        print_err(f"[ ERROR ]: {err}");
        return None;
    else:
        print(f"[ INFO ]: Request to {url} succeeded with response code {response.status_code}")
        return response.json();  # Assuming the response is in JSON format
    ##endtry
##end
def sendPostRequest(url,auth,content):
    heads={
        "User-Agent":user_agent,
        "Authorization":f"Bearer {auth}",
        "Content-Type":"application/json",
        "Accepts":"application/json",
    };
    try:
        response=requests.post(url,headers=heads,json=content);
        response.raise_for_status();  # Raise an HTTPError for bad responses
    except requests.exceptions.HTTPError as http_err:
        print_err(f"[ ERROR ]: Request to {url} failed with response code {response.status_code} (HTTP: {http_err})");
        return None;
    except Exception as err:
        print_err(f"[ ERROR ]: {err}");
        return None;
    else:
        print(f"[ INFO ]: Request to {url} succeeded with response code {response.status_code}")
        return response.json();  # Assuming the response is in JSON format
    ##endtry
##end
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})');
    print(f'Connected to {len(bot.guilds)} guild(s)');
    print('------');
    try:
        synced = await bot.tree.sync();
        print(f"Synced {len(synced)} commands");
    except Exception as e:
        print(f"Failed to sync commands: {e}");
    ##endtry
##end
@bot.tree.command(name="hello", description="Says hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message('Hello!');
##end
@bot.tree.command(name="restart", description="Restarts the bot")
async def restart(interaction: discord.Interaction):
    if str(interaction.user)==owner_user:
        await interaction.response.send_message("Restarting bot...");
        os.execv(sys.executable, ['python'] + sys.argv);
    else:
        await interaction.response.send_message("Only the bot owner can restart the bot");
    ##endif
##end
@bot.tree.command(name="test", description="Recoding? Seriously?")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message('RECODING? SERIOUSLY?');
##end
@bot.tree.command(name="help", description="Shows all commands and their parameters")
async def test(interaction: discord.Interaction):
    embed = discord.Embed(title="Commands", description="Here are the available commands:", color=0x00ff00);
    for command in bot.tree.walk_commands():
        embed.add_field(name=command.name, value=command.description, inline=False)
    ##end
    await interaction.response.send_message(embed=embed);
##end
@bot.tree.command(name="echo", description="Says whatever you give it as an argument")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message);
##end
@bot.tree.command(name="van", description="bruh why did u van?")
async def van(interaction: discord.Interaction, username:discord.User):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(f"You tried to van {username.mention}, but vanning is only for servers. Nice try! <:trollgod:1330974448911913072>");
    else:
        await interaction.response.send_message(f"{username.mention} has been vanned <:trollgod:1330974448911913072>")
    ##endif
##end
@commands.has_permissions(manage_guild=True)
@bot.tree.command(name="trigger", description="triggers an event (requires manage-server permission)")
async def trigger(interaction: discord.Interaction, event: str, delay: int=0):
    try:
        if not isinstance(interaction.channel, discord.DMChannel):
            #dev_role = discord.utils.get(interaction.user.roles,name="Developer");
            if interaction.user.guild_permissions.manage_guild:
                json_content=sendRequest(webservice_url+f"/trigger_event?name={event}&delay={delay}",token);
                if json_content is None:
                    await interaction.response.send_message(f"Failed to trigger event {event} :x:");
                else:
                    await interaction.response.send_message(f"Triggered event {event} :white_check_mark:");
                ##endif
            else:
                await interaction.response.send_message(f"You do not have permission to use that command (Developer Only) `--trigger 001--`");
            ##endif
        else:
            await interaction.response.send_message(f"Command cannot be run outside of a server `--trigger 002--`");
        ##endif
    except Exception as e:
        print_err(e);
        await interaction.response.send_message(f"An error occured while running the command `--trigger 003--`");
    ##endtry
##end
@commands.has_permissions(manage_guild=True)
@bot.tree.command(name="event_add", description="adds an event to schedule (requires manage-server permission)")
async def trigger(interaction: discord.Interaction, event: str, delay: int=0):
    try:
        if not isinstance(interaction.channel, discord.DMChannel):
            #dev_role = discord.utils.get(interaction.user.roles,name="Developer");
            if interaction.user.guild_permissions.manage_guild:
                json_={
                    "name":event,
                    "start_time":delay,
                };
                json_content=sendPostRequest(webservice_url+f"/schedule/write?action=add",token,json_);
                if json_content is None:
                    await interaction.response.send_message(f"Failed to add event {event} to schedule :x:");
                else:
                    await interaction.response.send_message(f"Added event {event} to schedule :white_check_mark:");
                ##endif
            else:
                await interaction.response.send_message(f"You do not have permission to use that command (Developer Only) `--event add 001--`");
            ##endif
        else:
            await interaction.response.send_message(f"Command cannot be run outside of a server `--event add 002--`");
        ##endif
    except Exception as e:
        print_err(e);
        await interaction.response.send_message(f"An error occured while running the command `--event add 003--`");
    ##endtry
##end
@commands.has_permissions(manage_guild=True)
@bot.tree.command(name="event_remove", description="removes an event from schedule (requires manage-server permission)")
async def trigger(interaction: discord.Interaction, event: str):
    try:
        if not isinstance(interaction.channel, discord.DMChannel):
            #dev_role = discord.utils.get(interaction.user.roles,name="Developer");
            if interaction.user.guild_permissions.manage_guild:
                json_={
                    "name":event,
                };
                json_content=sendPostRequest(webservice_url+f"/schedule/write?action=remove",token,json_);
                if json_content is None:
                    await interaction.response.send_message(f"Failed to add event {event} to schedule :x:");
                else:
                    await interaction.response.send_message(f"Removed event {event} from schedule :white_check_mark:");
                ##endif
            else:
                await interaction.response.send_message(f"You do not have permission to use that command (Developer Only) `--event remove 001--`");
            ##endif
        else:
            await interaction.response.send_message(f"Command cannot be run outside of a server `--event remove 002--`");
        ##endif
    except Exception as e:
        print_err(e);
        await interaction.response.send_message(f"An error occured while running the command `--event remove 003--`");
    ##endtry
##end
@commands.has_permissions(manage_guild=True)
@bot.tree.command(name="schedule", description="shows a list of events to be triggered")
async def schedule(interaction: discord.Interaction):
    try:
        if not isinstance(interaction.channel, discord.DMChannel):
            #dev_role = discord.utils.get(interaction.user.roles,name="Developer");
            if interaction.user.guild_permissions.manage_guild:
                json_content=sendRequest(webservice_url+f"/schedule",token);
                if json_content is None:
                    await interaction.response.send_message(f"Failed to get schedule :x:");
                else:
                    events=json_content['events'];
                    embed = discord.Embed(title="Schedule",description="Scheduled Events");
                    for event in events:
                        embed.add_field(name="Event Name", value=event["name"]);
                        embed.add_field(name="Start Time", value=event["start_time"]);
                    ##end
                    await interaction.response.send_message(embed=embed);
                ##endif
            else:
                await interaction.response.send_message(f"You do not have permission to use that command (Developer Only) `--schedule 001--`");
            ##endif
        else:
            await interaction.response.send_message(f"Command cannot be run outside of a server `--schedule 002--`");
        ##endif
    except Exception as e:
        print_err(e);
        await interaction.response.send_message(f"An error occured while running the command `--schedule 003--`");
    ##endtry
##end
@commands.has_permissions(moderate_members=True)
@bot.tree.command(name="mute", description="Times out a member for a specified duration with reason (requires moderate-members permission)")
async def mute(interaction: discord.Interaction, member: discord.Member, duration: int, unit: str, reason: str="No Reason provided"):
    try:
        if not isinstance(interaction.channel, discord.DMChannel):
            if not interaction.user.guild_permissions.moderate_members:
                await interaction.response.send_message("You do not have permission to use that command`--mute 001--`", ephemeral=True);
                return;
            ##endif
            if not interaction.guild.me.guild_permissions.moderate_members:
                await interaction.response.send_message("I do not have permission to mute members `--mute 004--`", ephemeral=True);
                return;
            ##endif
            if unit not in ['s', 'm', 'h', 'd']:
                await interaction.response.send_message("Invalid time unit! Use 's' (seconds), 'm' (minutes), 'h' (hours), or 'd' (days).", ephemeral=True)
                return;
            ##endif
            # Calculate the timeout duration
            if unit == 's':
                delta = timedelta(seconds=duration);
            elif unit == 'm':
                delta = timedelta(minutes=duration);
            elif unit == 'h':
                delta = timedelta(hours=duration);
            elif unit == 'd':
                delta = timedelta(days=duration);
            ##endif

            # Apply the timeout
            timeout_end = discord.utils.utcnow() + delta;
            await member.timeout(timeout_end,reason=reason);
            await interaction.response.send_message(f'{member.mention} has been muted for {duration} {unit}. Reason: {reason}');
        else:
            await interaction.response.send_message(f"Command cannot be run outside of a server `--mute 002--`");
        ##endif
    except Exception as e:
        print_err(e);
        await interaction.response.send_message('An error occured while running the command `--mute 003--`');
    ##endtry
##end
@commands.has_permissions(ban_members=True)
@bot.tree.command(name="ban", description="Bans a member for a specified duration with reason (requires ban-members permission)")
async def ban(interaction: discord.Interaction, member: discord.User, duration: int, unit: str, reason: str="No Reason provided"):
    try:
        if not isinstance(interaction.channel, discord.DMChannel):
            if not interaction.user.guild_permissions.ban_members:
                await interaction.response.send_message("You do not have permission to use that command`--ban 001--`", ephemeral=True);
                return;
            ##endif
            if not interaction.guild.me.guild_permissions.ban_members:
                await interaction.response.send_message("I do not have permission to ban members `--ban 004--`", ephemeral=True);
                return;
            ##endif
            if unit not in ['s', 'm', 'h', 'd']:
                await interaction.response.send_message("Invalid time unit! Use 's' (seconds), 'm' (minutes), 'h' (hours), or 'd' (days). `--ban 005--`", ephemeral=True)
                return;
            ##endif
            # Calculate the ban duration
            if unit == 's':
                delta = timedelta(seconds=duration);
            elif unit == 'm':
                delta = timedelta(minutes=duration);
            elif unit == 'h':
                delta = timedelta(hours=duration);
            elif unit == 'd':
                delta = timedelta(days=duration);
            ##endif

            # Apply the ban
            timeout_end = discord.utils.utcnow() + delta;
            await member.ban(reason=reason);
            await interaction.response.send_message(f'{member.mention} has been banned for {duration}{unit}. Reason: {reason}');
        else:
            await interaction.response.send_message(f"Command cannot be run outside of a server `--ban 002--`");
        ##endif
    except Exception as e:
        print_err(e);
        await interaction.response.send_message('An error occured while running the command `--ban 003--`');
    ##endtry
##end
@commands.has_permissions(ban_members=True)
@bot.tree.command(name="unban", description="Removes ban from member (requires ban-members permission)")
async def unban(interaction: discord.Interaction, user_id:int, reason:str="No Reason Provided"):
    try:
        if not isinstance(interaction.channel, discord.DMChannel):
            if not interaction.user.guild_permissions.moderate_members:
                await interaction.response.send_message("You do not have permission to use that command`--unban 001--`", ephemeral=True);
                return;
            ##end
            if not interaction.guild.me.guild_permissions.moderate_members:
                await interaction.response.send_message("I do not have permission to mute members `--unban 004--`", ephemeral=True);
                return;
            ##endif
            user = await interaction.client.fetch_user(user_id);
            await interaction.guild.unban(user, reason=reason);
            await interaction.response.send_message(f'{user.mention} has been unmuted. Reason: {reason}');
        else:
            await interaction.response.send_message(f"Command cannot be run outside of a server `--unban 002--`");
        ##endif
    except Exception as e:
        print_err(e);
        await interaction.response.send_message('An error occured while running the command `--unban 003--`');
    ##endtry
##end
@commands.has_permissions(moderate_members=True)
@bot.tree.command(name="unmute", description="Removes timeout from member (requires moderate-members permission)")
async def unmute(interaction: discord.Interaction, member: discord.Member, reason:str="No Reason Provided"):
    try:
        if not isinstance(interaction.channel, discord.DMChannel):
            if not interaction.user.guild_permissions.moderate_members:
                await interaction.response.send_message("You do not have permission to use that command`--unmute 001--`", ephemeral=True);
                return;
            ##end
            if not interaction.guild.me.guild_permissions.moderate_members:
                await interaction.response.send_message("I do not have permission to mute members `--unmute 004--`", ephemeral=True);
                return;
            ##endif
            # Apply the timeout
            await member.timeout(None);
            await interaction.response.send_message(f'{member.mention} has been unmuted. Reason: {reason}');
        else:
            await interaction.response.send_message(f"Command cannot be run outside of a server `--unmute 002--`");
        ##endif
    except Exception as e:
        print_err(e);
        await interaction.response.send_message('An error occured while running the command `--unmute 003--`');
    ##endtry
##end
bot.run('your token here');
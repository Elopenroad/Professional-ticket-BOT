import discord 
from discord.ext import commands
import asyncio
import json
from discord import app_commands
from discord.ext.commands import MissingPermissions

with open('config.json') as f:
    config = json.load(f)

token = config['token']

bot = commands.Bot(command_prefix='/' , intents= discord.Intents.all())

@bot.event
async def on_ready():
    global command_called
    global command_called_section
    command_called = False
    command_called_section = False
    synced = await bot.tree.sync()
    print(f"synced {len(synced)} command(s))")
    print('Bot is running')
 
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if isinstance(message.channel, discord.TextChannel) and message.channel.name == 'ticketmaster':
        if not message.author.guild_permissions.administrator:
            try:
                await message.delete()
            except discord.errors.NotFound:
                pass

    await bot.process_commands(message)




def only_admin(interaction: discord.Integration):
    if interaction.user == interaction.user.guild_permissions.administrator:
        return True
    else:
        return False




command_called_section = False

@bot.tree.command(name="section", description="create a section")
@app_commands.checks.has_permissions(administrator=True)
async def section(interaction: discord.Integration):
    global command_called_section
    if command_called_section:
        text = discord.Embed(color=discord.Color.gold() , description="""**Sorry, this command can only be called once**
        
        
        **In the eventuality of security concerns,
         we have developed an alternative command that grants you the ability to reset all settings of the bot,
          encompassing roles and channels**
          **```/reload```**

""")
        await interaction.response.send_message(embed=text)
    else:
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
           }
        category = await guild.create_category('support', overwrites=overwrites)
        await guild.create_voice_channel('ticket',  category=category, user_limit=10,overwrites=overwrites)
        channel = await guild.create_text_channel(name='ticketmaster' , overwrites=overwrites ,category=category)
        embed = discord.Embed(color=discord.Color.gold() , title="***GET START***" , description="""```python\n/support\n```
        
        
        **Upon invoking this command, the bot will generate a designated section consisting of a text channel and a voice channel. Subsequently, I will diligently rectify any remaining steps required to successfully initiate the bot**""")
        await channel.send(embed=embed)
        textembed = discord.Embed(title=f"**The TicketMaster section has been created**")
        await interaction.response.send_message(embed=textembed)

        command_called_section = True





command_called = False


@bot.tree.command(name="support", description="create a support role")
@app_commands.checks.has_permissions(administrator=True)
async def support(interaction: discord.Integration):
    if interaction.channel.name != 'ticketmaster':
        return
    global command_called
    if command_called:
        text = discord.Embed(color=discord.Color.gold() , description="""**Sorry, this command can only be called once**
        
        
        **In the eventuality of security concerns,
         we have developed an alternative command that grants you the ability to reset all settings of the bot,
          encompassing roles and channels**

          **```/reload```**

""")
        await interaction.response.send_message(embed=text)

    else:

        guild = interaction.guild
        role = await guild.create_role(name="MasterSupportTeam")
        embed = discord.Embed(color=discord.Color.gold() , description=f"""***```\nCommand: /section
Description: To get started, use this command to create a dedicated section for sending tickets. It will create a special channel where users can submit their support requests.

Command: /support
Description: After setting up the section, utilize this command to configure your support team. It will create a special role for your dedicated supporters, enabling them to handle incoming tickets.

Command: /role
Description: Once the support team is set, assign the support role to specific users by using this command. Those who have this role will receive ticket messages directly in their DMs for quick and efficient support.

Command: /team
Description: Support list.

Command: /remove
Description: In case you need to make changes to your support team, use this command to remove the support role from certain users.

Command: /done
Description: Once all the setup steps are completed, simply use this command, and the bot will begin its work. Remember, the commands will only work within the support section for seamless operation.

Important Note: If you encounter any issues or if roles and channels are accidentally deleted, never attempt to recreate them manually. Instead, use the -reload command, which fixes the bot and restarts everything, ensuring the smooth functioning of your support system.

Command: /connect
Description: By using this command, the bot will join the voice channel section, allowing for voice-based support and interactions.

Command: /disconnect
Description: When you no longer require the bot's presence in the voice channel, simply issue this command, and the bot will gracefully leave.

Ticket System:
The ticket system enables users to submit support requests to the support team. When a ticket is sent, the bot automatically sends the ticket message to all supporters. Supporters can then respond by pressing a reaction to indicate they have taken up the ticket. Once they have addressed the issue, the supporters can provide a detailed report on the resolution.

Member Limitation:
To prevent abuse and maintain fairness, members can only send a ticket once every 6 hours. This limitation ensures that everyone gets a chance to receive timely support.

Unanswered Tickets:
If a supporter fails to respond to a member's ticket within a reasonable timeframe, the bot will send a message to both the member's DM and the supporter, apologizing for the delay in response. This ensures that no ticket goes unanswered, and members are aware that their concerns are being addressed.

Get ready to witness the power of the Amazing Discord Support Bot as it revolutionizes your support system, making it more organized, efficient, and responsive than ever before!
\n```***


**Command list**

      **```/help```**
      
      **```/section```**
      
      **```/support```**
      
      **```/done```**
      
      **```/role```**

      **```/team```**
      
      **```/remove```**
      
      **```/connect```**
      
      **```/disconnect```**
""")
        embed.set_image(url='https://cdn.discordapp.com/attachments/1055178772363612170/1118590706303377439/Baleen_make_a_picture_for_a_discord_bot_ticket__golden_animated_4cce965c-7853-4541-a23e-79d492264c84.png')
        await interaction.response.send_message(embed=embed)
        catgory = discord.utils.get(interaction.guild.categories, name='support')
        channel = discord.utils.get(interaction.guild.channels, name='ticketmaster')
        voiceChannel = discord.utils.get(interaction.guild.voice_channels, name='ticket')

        await catgory.set_permissions(interaction.guild.default_role, read_messages=True)
        await channel.set_permissions(interaction.guild.default_role, read_messages=True , send_messages=False)
        await voiceChannel.set_permissions(interaction.guild.default_role, read_messages=True)
        command_called = True
  

@bot.tree.command(name="reload", description="delete section and role")
@app_commands.checks.has_permissions(administrator=True)
async def reload(interaction: discord.Integration):
    global command_called
    global command_called_section
    command_called = False
    command_called_section = False


    guild = interaction.guild
    catgory = discord.utils.get(interaction.guild.categories, name='support')
    channel = discord.utils.get(interaction.guild.channels, name='ticketmaster')
    voiceChannel = discord.utils.get(interaction.guild.voice_channels, name='ticket')
    role = discord.utils.get(guild.roles, name='MasterSupportTeam')

    if voiceChannel or channel or catgory or role:
        try:
            await catgory.delete()
            await channel.delete()
            await voiceChannel.delete()
            await role.delete()
            embedif = discord.Embed(color=discord.Color.gold() ,title="""**Bot reloaded. Now you can use:**
        
        ```/section```
        ```/support```""")
        except discord.errors.NotFound:
            pass
   
        try:
            await interaction.response.send_message(embed=embedif)
        except discord.errors.NotFound:
            print('reload')
  
    
    else:
        embedelse = discord.Embed(color=discord.Color.gold() ,title="""**Bot reloaded. Now you can use:**
        
        **```/section```**
        **```/support```**""")
        await interaction.response.send_message(embed=embedelse)


@bot.tree.command(name="role", description="give the role")
@app_commands.checks.has_permissions(administrator=True)
async def role(interaction: discord.Integration,  member :  discord.Member):
    if interaction.channel.name != 'ticketmaster':
        return
    guild = interaction.guild
    role = discord.utils.get(guild.roles, name='MasterSupportTeam')
    await member.add_roles(role)
    embed = discord.Embed(color=discord.Color.gold(), title=f"__***{member.mention} added to the support team***__")
    
    bot_message = await interaction.response.send_message(embed=embed)
    try:
        await asyncio.sleep(20)
        await interaction.delete_original_response()
        if bot_message:
            await bot_message.delete()
    except discord.errors.NotFound:
        print('Not found')


@bot.tree.command(name="remove", description="remove the role")
@app_commands.checks.has_permissions(administrator=True)
async def remove(interaction: discord.Integration,  member: discord.Member):
    if interaction.channel.name != 'ticketmaster':
        return
    guild = interaction.guild
    role = discord.utils.get(guild.roles, name='MasterSupportTeam')
    await member.remove_roles(role)
    embed = discord.Embed(color=discord.Color.gold(),description=f"__***{member.mention} deleted from support team\n***__")
    bot_message = await interaction.response.send_message(embed=embed)
    try:
        await asyncio.sleep(20)
        if bot_message:
            await bot_message.delete()

        await interaction.delete_original_response()
    except discord.errors.NotFound:
        print("Not found")

@bot.tree.command(name="team", description="support team")
@app_commands.checks.has_permissions(administrator=True)
async def team(interaction: discord.Integration):
    if interaction.channel.name != 'ticketmaster':
        return
    role = discord.utils.get(interaction.guild.roles, name='MasterSupportTeam')     
    members_with_role = role.members 
    
    member_list = "\n".join([member.name for member in members_with_role])  # Create a list of members
    messageE = discord.Embed(color=discord.Color.gold() , description= f"**The following members have the {role.name} role:\n{member_list}**")
    messagel =await interaction.response.send_message(embed=messageE)
    try:
        await asyncio.sleep(20)
        if messagel:
            await messagel.delete()

        await interaction.delete_original_response()
    except discord.errors.NotFound:
        print("Not found")


@bot.tree.command(name="done", description="save settings")
@app_commands.checks.has_permissions(administrator=True)
async def done(interaction: discord.Integration ):

    if interaction.channel.name != 'ticketmaster':
        return
    catgory = discord.utils.get(interaction.guild.categories, name='support')
    channel = discord.utils.get(interaction.guild.channels, name='ticketmaster')
    voiceChannel = discord.utils.get(interaction.guild.voice_channels, name='ticket')
    embed = discord.Embed(title="**Boom**")
    await interaction.response.send_message(embed=embed)

    await channel.purge()

    await catgory.set_permissions(interaction.guild.default_role, read_messages=True)
    await channel.set_permissions(interaction.guild.default_role, read_messages=True , send_messages=True)
    await voiceChannel.set_permissions(interaction.guild.default_role, read_messages=True)
    embed = discord.Embed(color=discord.Color.gold(), title="**TICKETS**", description="""**Welcome to our support ticket system!
    We have created a dedicated text channel called 'ticket' where you can send your support tickets.
    This channel is specifically designed for you to receive assistance and guidance from our support team.**

    **We kindly ask for your patience while waiting for a response from our support team.
    They are working diligently to address all tickets in a timely manner.
    Rest assured, your inquiry is important to us, and we will make every effort to provide a helpful and prompt resolution.**

    **__To send a ticket, type:__**
    ```/ticket```
    **and write your report**""")
    embed.set_image(url='https://media.discordapp.net/attachments/1055178772363612170/1118593471981297714/Baleen_make_a_picture_for_a_discord_bot_ticket__golden_animated_080d7a41-adb3-4bfc-8430-4adbab87c536.png?width=427&height=427')
    await interaction.channel.edit(name='ticketmaster')

    await channel.send(embed=embed)
    await interaction.channel.edit(slowmode_delay=3600)
   



connected_channel = None

@bot.tree.command(name="connect", description="join a voice")
@app_commands.checks.has_permissions(administrator=True)
async def connect(interaction: discord.Integration, *, channel: str = 'ticket'):
    global connected_channel
    voice_cliento = interaction.guild.voice_client

    guild = interaction.guild
    voice_channels = guild.voice_channels
    try:

        if not voice_cliento:
            target_channel = None
            for voice_channel in voice_channels:
                if voice_channel.name == channel:
                    target_channel = voice_channel
                    break

            if target_channel:
                voice_client = await target_channel.connect()
                connected_channel = target_channel
                embedx = discord.Embed(color=discord.Color.gold(), title=f"***Bot has joined the voice channel: {target_channel.name}***")
                await interaction.response.send_message(embed=embedx)
            else:
                embedf = discord.Embed(color=discord.Color.gold(), title="***The specified voice channel was not found. Joining default channel.***")
                target_channel = discord.utils.get(interaction.guild.voice_channels, name='ticket')
                await interaction.response.send_message(embed=embedf)
                voice_client = await target_channel.connect()
                connected_channel = target_channel
                embedc = discord.Embed(color=discord.Color.gold(), title=f"***Bot has joined the default voice channel: {target_channel.name}***")
                await interaction.response.send_message(embed=embedc)
        else:
            print("Bot is already connected to a voice channel.")
    except discord.errors.NotFound:
        print("Unknown interaction error occurred.")


@bot.tree.command(name="disconnect", description="disconnect")
@app_commands.checks.has_permissions(administrator=True)
async def disconnect(interaction: discord.Integration):
    global connected_channel
    voice_client = interaction.guild.voice_client

    if voice_client:
        await voice_client.disconnect()
        embed = discord.Embed(color=discord.Color.gold(), title="***Disconnected from the voice channel.***")
        await interaction.response.send_message(embed=embed)
        connected_channel = None
        print("Disconnected from the voice channel.")
    else:
        embed = discord.Embed(color=discord.Color.gold(), title="***Not currently connected to a voice channel.***")
        await interaction.response.send_message(embed=embed)
        print("Not currently connected to a voice channel.")


@bot.tree.command(name="ticket", description="send a ticket")
@commands.guild_only()
async def ticket(interaction: discord.Integration, *, message:str):
    if interaction.channel.name != 'ticketmaster':
        return
    guild = interaction.guild
    role = discord.utils.get(guild.roles, name='MasterSupportTeam')
    if role in interaction.user.roles:
        authorembed = discord.Embed(color=discord.Color.gold(), title=f"ERROR" , description=f"**You're not allow to send ticket because you are a supporter**")
        authormode = await interaction.response.send_message(embed=authorembed)
        await asyncio.sleep(10)
        try:
            await interaction.delete_original_response()
            if authormode:
                await authormode.delete()    
        except discord.errors.NotFound:
            pass

    author_name = interaction.user.name
    embed = discord.Embed(color=discord.Color.gold(), description="**We have received your ticket. Please be patient. We will reply to your message soon**")
    embed.set_image(url='https://cdn.discordapp.com/attachments/1055178772363612170/1117783960764825680/Baleen_some_animated_are_in_a_golden_with_a_headphone_and_a_tab_b6a99666-51bf-4ee8-9430-35dbbbde71b2.png')
    bot_message = await interaction.response.send_message(embed=embed)
    await asyncio.sleep(5)
    try:
        await interaction.delete_original_response()
        if bot_message:
            await bot_message.delete()
    except discord.errors.NotFound:
        pass

    supporters = [member for member in guild.members if role in member.roles]
    support_messages = {}

    for supporter in supporters:
        mes = discord.Embed(color=discord.Color.gold(), title=f"**Ticket message**", description=f"""**{message}**
        
        {author_name}""")
        sent_message = await supporter.send(embed=mes)
        support_messages[sent_message.id] = supporter
        await sent_message.add_reaction('✅')

    def check(reaction, user):
        return user in supporters and str(reaction.emoji) == '✅'

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=172800.0, check=check)
    except asyncio.TimeoutError:
        supporterembed = discord.Embed(color=discord.Color.gold() , title="**Your response was not received within the given time. Please try again later**")
        await supporter.send(embed=supporterembed)
    else:
        for message_id, supporter in support_messages.items():
            if reaction.message.id == message_id:
                del support_messages[message_id]
                
                supportResponse = discord.Embed(color=discord.Color.gold(), title=f"**Response**", description="Please write your response for the reporter")
                wrting = await supporter.send(embed=supportResponse)

                def message_check(m):
                    return m.author == supporter

                try:
                    response = await bot.wait_for('message', timeout=172800.0, check=message_check)
                except asyncio.TimeoutError:
                    responseEmbed = discord.Embed(color=discord.Color.gold() , description="""**
                    We regret to inform you that our support team was unable to respond to your ticket.
                      This may have occurred due to various reasons,
                        including the presence of irrelevant content,
                          the use of vulgar language,
                            or the nature of technical and bot support inquiries.
                              If you believe your initial message was clear and did not violate any guidelines,
                                we kindly request you to submit another ticket or reach out to our support team for further assistance **""")
                    await interaction.user.send(embed = responseEmbed)
                else:
                    answer = discord.Embed(color=discord.Color.gold(), title=f"***Support team response from {supporter.display_name}***", description=f"""
__**YOUR TICKET**__:
                    **``` \n{message}:\n```**
                    
__**SUPPORT RESPONSE**__:
                    **```\n{response.content}\n```**""")
                    await interaction.user.send(embed=answer)
                    await wrting.delete()
                    report = discord.Embed(color=discord.Color.gold(), title="**REPORT**", description=f"""**The ticket**
                    
                    **```{message}```**
                    
                    __from:__ 
                    **```{author_name}```**
                    
                    __answer__:
                    **```{response.content}```**""")

                    await sent_message.delete()
                    await supporter.send(embed=report)
                    try:
                        await reaction.message.delete()
                    except discord.errors.NotFound:
                        print("message not fund")
                break




bot.remove_command("help")



@bot.tree.command()
@only_admin()
async def help(interaction: discord.Integration):
    embed = discord.Embed(color=discord.Color.gold(), title="Bot Commands", description="Here are the available commands:")
    embed.add_field(name="/section", value="**```\nCreates a support section with a text channel and a voice channel.\n```**")
    embed.add_field(name="/support", value="**```\nProvides information about the support ticket system.\n```**")
    embed.add_field(name="/reload", value="**```\nResets all settings of the bot, including roles and channels.\n```**")
    embed.add_field(name="/role mention", value="**```\nGives the support role to a member mentioned.\n```**")
    embed.add_field(name="/remove mention", value="**```\nRemoves the support role from a member mentioned.\n```**")
    embed.add_field(name="/done", value="**```\nMarks the support section setup as done and allows users to send tickets.\n```**")
    embed.add_field(name="/connect [channel]", value="**```\nConnects the bot to a voice channel. If no channel is specified, it joins the 'ticket' voice channel.\n```**")
    embed.add_field(name="/disconnect", value="**```\nDisconnects the bot from the current voice channel.\n```**")
    embed.add_field(name="/ticket [message]", value="**```\nSends a support ticket with the specified message.\n```**")
    
    await interaction.response.send_message(embed=embed)
    




bot.run(token)
# Discord-Bot
A work-in-progress Discord Bot built using discord.py.

By Henry Gu (legman1) and Byron Sun (Cherithe). (2021-2022)

Current Functionality:
- In-built music/video player. (For personal use only)
- Fun miscellaneous commands. (Gif commands, Image commands, Chat commands)
- Moderation commands to improve upon existing moderation capabilities.
- Locally persistent datastore.
- Can be deployed onto platforms such as Heroku to offer a full Discord Bot experience.

To Run:
- Fork this repository onto a local machine.
- Install all required modules listed in requirements.txt - Ideally, their latest versions.
- Install ffmpeg if you want to run the bot on a local device, and run from the root directory: src/bot.py.
- If running on Heroku, read relevant documentation - The necessary files should be present already however.
- More importantly, the bot requires 2 files: A .env and a BannedWords.txt in the src folder. After forking,
  create a Discord App application on the Developer Portal and include:
  DISCORD_TOKEN=<yourdiscordbottoken>
  TENOR_KEY=<yourtenorkeytoenablegifstowork> 
  POGWALL=<someemoteidhere>
  
  as formatted in your .env file. BannedWords.txt can be blank, but is used for the purposes of the filter command.
  The filter command when turned on, will filter any messages containing words in the BannedWords.txt which can be
  useful for policing general language used in the server.

What to Improve:
- The economy feature is currently bare-bones - Heroku does not support persistence as its servers restart
  regularly and use only the original fiels provided, so any files such as persistence are not saved.
  This can be resolved through means such as the Heroku-suggested AWS S3 which can be accessed using the Boto3 Python
  library - though new accounts only have free trials for 12 months.
- This can be improved upon by adding jobs, a shop, as well as time-limited actions and events to encourage
  users to use the bot.
- More general commands can be added as neccessary.
- Some more moderation commands could be added, such as a ban/kick command, though this seems redundant.


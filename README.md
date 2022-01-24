# outsmart_uploadfilter_tgbot
Telegram bot that receives media files and sends back slightly modified versions to get a version that circumvents hashcode-based upload-filters.

in early development.

To deploy this, create a telegram bot (by messaging @BotFather on tg), download the dependencies (from pip: skimage, telegram-bot and moviepy) set the access-token you receive as TELEGRAM_BOT_TOKEN in the environment and run bot.py with python (I am using python 3.7.9, but any 3.x.x should probably work).
But I will take care of the hosting myself once the code is ready.

roadmap:

* logging
* add basic safety features like rate limiting
* asynchronicity and parallelism for scaling
* add a way for users to give feedback
* more sophisticated filters
* user control over what filters to use
* add languages that arent English
* caching maybe? but I dont think it can be done while staying true to the principle of not saving the users files except temporarily

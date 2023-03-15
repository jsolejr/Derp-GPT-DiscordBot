// Import required modules
const Eris = require("eris");
const { Configuration, OpenAIApi } = require("openai");
// Load environment variables from .env file
require('dotenv').config()

// Set up OpenAI API client
const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

// Instantiate the Eris Discord bot with the bot token and required intents
const bot = new Eris(process.env.DISCORD_BOT_TOKEN, {
    intents: [
        "guildMessages"
    ]
});

// Define a helper function to perform completions using the OpenAI API
async function runCompletion(message) {
    const completion = await openai.createCompletion({
        model: "text-davinci-003",
        prompt: message,
        max_tokens: 200,
    });
    // Return the text of the first choice in the generated completions
    return completion.data.choices[0].text;
}

// Event handler: log when the bot is connected and ready
bot.on("ready", () => {
    console.log("Bot is connected and ready!");
});

// Event handler: log errors
bot.on("error", (err) => {
    console.error(err);
});

// Event handler: when a new message is created in a guild
bot.on("messageCreate", (msg) => {
    // Check if the message starts with the '#' character
    if (msg.content.startsWith("#")) {
        // Run the completion function and send the result as a reply
        runCompletion(msg.content.substring(1))
            .then(result => bot.createMessage(msg.channel.id, result));
    }
});

// Connect the bot to Discord
bot.connect();

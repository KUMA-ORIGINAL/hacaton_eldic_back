import { Telegraf } from 'telegraf';
import dotenv from "dotenv";
dotenv.config();

const bot = new Telegraf(process.env.BOT_TOKEN);

// Команда /start
bot.start((ctx) => {
  ctx.reply(
    "Добро пожаловать в Eldik Kassa!\nВыберите действие:",
    {
      reply_markup: {
        inline_keyboard: [
          [
            {
              text: "📲 Открыть Eldik Kassa",
              web_app: { url: "https://eldikkassa.ustaz.tech/" }
            }
          ],
          [
            { text: "ℹ️ О проекте", callback_data: "about" }
          ]
        ]
      }
    }
  );
});
bot.telegram.setMyCommands([
  { command: 'start', description: 'Главное меню Eldik Kassa' },
  { command: 'help', description: 'Список команд' },
  { command: 'about', description: 'Информация о проекте' },
  { command: 'app', description: 'Открыть веб-приложение' },
]);

// Команда /help
bot.command("help", (ctx) => {
  ctx.reply(
    "🆘 *Команды Eldik POS*\n\n" +
    "/start — открыть главное меню\n" +
    "/help — список команд\n" +
    "/about — информация о проекте\n" +
    "/app — открыть WebApp\n",
    { parse_mode: "Markdown" }
  );
});

// Команда /about
bot.command("about", (ctx) => {
  ctx.reply(
    "ℹ️ *Eldik Kassa*\nМини-касса для малого бизнеса.\n" +
    "Позволяет пробивать чеки, фиксировать оплату и смотреть отчёты — прямо внутри Telegram.",
    { parse_mode: "Markdown" }
  );
});

// Команда /app — открыть WebApp отдельно
bot.command("app", (ctx) => {
  ctx.reply(
    "Откройте приложение:",
    {
      reply_markup: {
        inline_keyboard: [
          [
            {
              text: "📲 Открыть Eldik Kassa",
              web_app: { url: "https://eldikkassa.ustaz.tech/" }
            }
          ]
        ]
      }
    }
  );
});


// Обработка ошибок
bot.catch((err, ctx) => {
  console.error(`❗ Ошибка у пользователя ${ctx.from.id}`, err);
  ctx.reply("Произошла ошибка. Попробуйте позже.");
});

bot.launch();
console.log("Telegram bot started");
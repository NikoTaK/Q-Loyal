import asyncio
import logging
import uvicorn

from aiogram import Bot, Dispatcher, F

from config import CUSTOMER_BOT_TOKEN
from config import BUSINESS_BOT_TOKEN

from app.handlers_customer import router as customer_router
from app.handlers_bussines import router as business_router
from app.database.models import async_main
from app.api import api_app 


customer_bot = Bot(token=CUSTOMER_BOT_TOKEN)
business_bot = Bot(token=BUSINESS_BOT_TOKEN)
dp = Dispatcher()

api_app.state.customer_bot = customer_bot
api_app.state.business_bot = business_bot

async def run_api():
    # Настраиваем сервер uvicorn
    config = uvicorn.Config(api_app, host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await async_main()
    
    customer_info = await customer_bot.get_me()
    business_info = await business_bot.get_me()

    customer_router.message.filter(F.bot.id == customer_info.id)
    business_router.message.filter(F.bot.id == business_info.id)

    dp.include_router(customer_router)
    dp.include_router(business_router)

    print(f"Customer Bot: @{customer_info.username}")
    print(f"Business Bot: @{business_info.username}")
    print("API Server running on http://0.0.0.0:8000")
    
    await asyncio.gather(
        dp.start_polling(customer_bot, business_bot),
        run_api()
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:  
        print("Starting customer and business bots...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Customer and business bots stopped by user")
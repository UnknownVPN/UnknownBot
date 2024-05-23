from enums.menu_keyboards import * 
from utilities.config_handler import ConfigHandler


cohandler = ConfigHandler()

async def new_service_log(
        app,
        info,
        user_id,
        payment_id,
        license,
        service_name,
        service_time,
        user_count,
        size,
        amount,
        card_number=None
    ):

    text = NEW_SERVICE_LOG.format(
        info,
        user_id,
        payment_id,
        license,
        service_name,
        service_time,
        user_count,
        size,
        amount,
        card_number,
        user_id,
        payment_id
    )

    await app.send_message(int(cohandler.getconfig["bot"]["log_channel"]),text)

async def new_card(app,topic,card,amount,tid,user_id):
    text = PAYEMNT_SUCCESS_LOGGER.format(topic,card,amount,tid,user_id)
    await app.send_message(int(cohandler.getconfig["bot"]["log_channel"]),text)
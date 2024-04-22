from services.crud.user_service import User
from services.crud.payments_service import Payment
from services.crud.vpn_services import vpnServices
from services.crud.cardPayment_service import CardPayment


class dbService(User, Payment, vpnServices, CardPayment):
    def __init__(self):
        User.__init__(self)
        Payment.__init__(self)
        vpnServices.__init__(self)
        CardPayment.__init__(self)

    async def MakeBuyTransection(self, userId: int, servicePrice: int):
        # handling all database query of buying services
        async with await self.client.start_session() as session:
            async with session.start_transaction():
                Buyer = await self.get_user(userId)
                if Buyer:
                    if Buyer["balance"] < servicePrice:
                        session.abort_transaction()
                        print("session abort")
                        return False
                    else:
                        await self.sub_user_amount(Buyer["_id"], servicePrice)
                        await session.commit_transaction()
                        return True

                else:
                    session.abort_transaction()
                    print("session abort")
                    return False

    async def TransferBalance(self, fromUser: int, To: int, Amount: int):
        async with await self.client.start_session() as session:
            async with session.start_transaction():
                fromUser = await self.get_user(fromUser)
                toUser = await self.get_user(To)
                if fromUser and toUser:
                    if fromUser["balance"] < Amount:
                        session.abort_transaction()
                        print("session abort")
                        return False
                    else:
                        detail = f'{fromUser["_id"]} to {toUser["_id"]} amount {Amount}'
                        await self.sub_user_amount(fromUser["_id"], Amount)
                        await self.inc_user_amount(toUser["_id"], Amount)
                        await self.insertPayments(
                            fromUser["_id"], Amount, "Done", detail
                        )
                        await session.commit_transaction()
                        print("session comited")
                        return True

                else:
                    session.abort_transaction()
                    print("session abort")
                    return False

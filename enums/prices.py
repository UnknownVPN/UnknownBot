class prices:
    service_1 = 38_000
    service_2 = 47_000
    service_3 = 48_000
    service_4 = 79_000
    service_5 = 74_000
    service_6 = 128_000
    service_7 = 97_000
    service_8 = 165_000
    
    giftAmount = 10_000
    userCount = 10_000
    data = 1_000
    
    size = {
        1: {
            25: service_1,
            50: service_2
        },
        2: {
            50 : service_3,
            100 : service_4
        },
        3: {
            75: service_5,
            150: service_6
        },
        4: {
            100: service_7,
            200: service_8
        }
    }  

    cs1 = 98_000
    cs2 = 146_000
    cs3 = 154_000
    cs4 = 263_000
    cs5 = 218_000
    cs6 = 382_000
    cs7 = 281_000
    cs8 = 499_000

    service_dict = {
        cs1: service_1,
        cs2: service_2,
        cs3: service_3,
        cs4: service_4,
        cs5: service_5,
        cs6: service_6,
        cs7: service_7,
        cs8: service_8
    }

    str_conf = [
        [
            {"size": 25, "price": f"{cs1:,}"},
            {"size": 50, "price": f"{cs2:,}"},
            "تک",
        ],
        [
            {"size": 50, "price": f"{cs3:,}"},
            {"size": 100, "price": f"{cs4:,}"},
            "دو",
        ],
        [
            {"size": 75, "price": f"{cs5:,}"},
            {"size": 150, "price": f"{cs6:,}"},
            "سه",
        ],
        [
            {"size": 100, "price": f"{cs7:,}"},
            {"size": 200, "price": f"{cs8:,}"},
            "چهار",
        ],
    ]

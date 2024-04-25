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

    service_dict = {
        98_000: service_1,
        146_000: service_2,
        154_000: service_3,
        263_000: service_4,
        218_000: service_5,
        382_000: service_6,
        281_000: service_7,
        499_000: service_8
    }

    str_conf = [
        [
            {"size": 25, "price": f"{service_dict[98_000]:,}"},
            {"size": 50, "price": f"{service_dict[146_000]:,}"},
            "تک",
        ],
        [
            {"size": 50, "price": f"{service_dict[154_000]:,}"},
            {"size": 100, "price": f"{service_dict[263_000]:,}"},
            "دو",
        ],
        [
            {"size": 75, "price": f"{service_dict[218_000]:,}"},
            {"size": 150, "price": f"{service_dict[382_000]:,}"},
            "سه",
        ],
        [
            {"size": 100, "price": f"{service_dict[281_000]:,}"},
            {"size": 200, "price": f"{service_dict[499_000]:,}"},
            "چهار",
        ],
    ]

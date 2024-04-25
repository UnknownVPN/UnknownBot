class prices:
    giftAmount = 10_000
    service_1 = 99_000
    service_2 = 129_000
    service_3 = 130_000
    service_4 = 197_000
    service_5 = 186_000
    service_6 = 297_000
    service_7 = 269_000
    service_8 = 385_000
    userCount = 10_000
    data = 3_000

    size = {
        1: {25: service_1, 50: service_2},
        2: {50: service_3, 100: service_4},
        3: {75: service_5, 150: service_6},
        4: {100: service_7, 200: service_8},
    }

    service_dict = {
        70_000: 99_000,
        104_000: 129_000,
        110_000: 130_000,
        188_000: 197_000,
        156_000: 186_000,
        273_000: 297_000,
        201_000: 269_000,
        357_000: 385_000,
    }

    str_conf = [
        [
            {"size": 25, "price": f"{service_1:,}"},
            {"size": 50, "price": f"{service_2:,}"},
            "تک",
        ],
        [
            {"size": 50, "price": f"{service_3:,}"},
            {"size": 100, "price": f"{service_4:,}"},
            "دو",
        ],
        [
            {"size": 75, "price": f"{service_5:,}"},
            {"size": 150, "price": f"{service_6:,}"},
            "سه",
        ],
        [
            {"size": 100, "price": f"{service_7:,}"},
            {"size": 200, "price": f"{service_8:,}"},
            "چهار",
        ],
    ]

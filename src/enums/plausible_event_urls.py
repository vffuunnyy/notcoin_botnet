import enum


class PlausibleEventUrls(str, enum.Enum):
    """Plausible event URLs."""

    WEBAPP_RELOAD = "https://clicker.joincommunity.xyz/clicker#tgWebAppData=query_id%3DAAEmj9sVAAAAACaP2xVltUK_%26user%3D%257B%2522id%2522%253A366710566%252C%2522first_name%2522%253A%2522%25E6%259C%2589%25E6%25AF%2592%25E3%2581%25AA%25E3%2581%259F%25E3%2582%258F%25E3%2581%2594%25E3%2581%25A8%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522vffuunnyy%2522%252C%2522language_code%2522%253A%2522ru%2522%252C%2522is_premium%2522%253Atrue%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1705501647%26hash%3D9843553e63398a4d6cc395c2fa0f398801ef0e2355a98615bcea5dd07a97cd55&tgWebAppVersion=7.0&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23212d3b%22%2C%22section_bg_color%22%3A%22%231d2733%22%2C%22secondary_bg_color%22%3A%22%23151e27%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d8b99%22%2C%22link_color%22%3A%22%235eabe1%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23242d39%22%2C%22accent_text_color%22%3A%22%2364b5ef%22%2C%22section_header_text_color%22%3A%22%2379c4fc%22%2C%22subtitle_text_color%22%3A%22%237b8790%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%7D"
    BOOSTS_PAGE = "https://clicker.joincommunity.xyz/clicker/boosts"
    HOME_PAGE = "https://clicker.joincommunity.xyz/clicker"
    TASKS_PAGE = "https://clicker.joincommunity.xyz/clicker/earn"

def get_restaurants(urls):
    return [
        {
            "id": i + 1,
            "name": f"Вкусно и точка - {i + 1}",
            "url": url
        }
        for i, url in enumerate(urls)
    ]

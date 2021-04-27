hash_tags = [
    # "آجیل",
    "برنج",
    # "mi8sejogja",
]


def convert_to_hash_tag():
    data = []
    for hash_tag in hash_tags:
        data.append(hash_tag.replace(' ', '_'))
    return data


def get_hashtags():
    return convert_to_hash_tag()

import re


def get_text_data(text: str) -> dict:
    words = re.findall(r"\w+", text)
    sentences = re.split(r"[.?!]", text)
    paragraphs = re.split("\n\n", text)
    return {
        "words": words,
        "sentences": sentences,
        "paragraphs": paragraphs,
    }


if __name__ == '__main__':
    text = """В глубине густого леса, где лучи солнца едва проникают сквозь листву, расцветает загадочное царство природы. Здесь, среди высоких деревьев и мягкого покрывала мха, цветут редкие и невероятно красочные цветы. Их лепестки словно пленительные краски на холсте природы, создавая неповторимую симфонию цветов и оттенков. В этом уединенном уголке земли время кажется замедленным, словно природа таинственно играет своей собственной мелодией.

    Среди этого природного изобилия выделяется старинный замок, стоящий на возвышенности, словно страж бескрайних лесов. Замок, поглощенный временем и завесой легенд, словно хранит в себе тайны веков. Его стены кажутся пронизанными духом прошлого, а каждый проход и комната словно запечатаны воспоминаниями. Шаги по изношенным полам замедляются, будто приглашая гостей на увлекательное путешествие в историю и загадки этого загадочного места.

    Вечерний свет проникает сквозь стекла замка, освещая старинные портреты и пыльные мебельные детали. В тишине слышны лишь шорохи лесных созданий за окнами. Здесь, в этом волшебном уголке природы и истории, словно соединяются два мира – сказочный лес и загадочный замок, создавая атмосферу, полную магии и таинственности.
    """

    text_data = get_text_data(text)

    # 1. количество символов
    print(len(text))

    # 2. количество слов
    print(len(text_data["words"]))

    # 3. количество предложений
    print(len(text_data["sentences"]))

    # 4. количество абзацев (считаем два переноса строки за абзац)
    print(len(text_data["paragraphs"]))

    # 5. самое длинное слово
    print(max(text_data["words"], key=len))

    # 6. самое короткое слово
    print(min(text_data["words"], key=len))
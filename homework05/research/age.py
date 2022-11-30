import datetime
import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def translate_date(b_date: str) -> tp.Optional[dt.date]:
    try:
        b_date_comps = list(map(int, b_date.split(".")))
        return dt.date(*b_date_comps[::-1])
    except Exception:
        return None


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    f_response = get_friends(
        user_id=user_id,
        fields=["bdate"],
    )
    count = 0
    friends_list = f_response.items
    age = 0
    for f in friends_list:
        dob = f.get("bdate", None)  # type: ignore
        t_dob = translate_date(dob)
        if t_dob:
            count += 1
            age += (dt.datetime.now().date() - t_dob).days / 365  # type: ignore
    return age / count


if __name__ == "__main__":
    # id_ = 120652471
    id_ = 168643808
    res = age_predict(id_)
    a = 0

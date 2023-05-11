from pytest import mark, raises

from slash3 import S3Key


@mark.parametrize(
    "base, append, expect",
    [
        ("private/", "/clowns.jpg", "private/clowns.jpg"),
    ],
)
def test_add(base: str, append: str, expect: str) -> None:
    assert S3Key(base) + append == S3Key(expect)


@mark.parametrize(
    "base, append, expect",
    [
        ("", "clowns.jpg", "clowns.jpg"),
        ("private/", "/clowns.jpg", "private/clowns.jpg"),
        ("private/", "clowns.jpg", "private/clowns.jpg"),
        ("private", "/clowns.jpg", "private/clowns.jpg"),
        ("private-", "clowns.jpg", "private-clowns.jpg"),
    ],
)
def test_append(base: str, append: str, expect: str) -> None:
    assert S3Key(base).append(append) == S3Key(expect)


@mark.parametrize(
    "key, expect",
    [
        (
            "/clowns.jpg",
            'S3 keys cannot start with the delimiter "/" ("/clowns.jpg")',
        ),
        (
            "private//clowns.jpg",
            (
                'S3 keys cannot contain consecutive "/" delimiters '
                '("private//clowns.jpg")'
            ),
        ),
        (
            "x" * 1025,
            (
                f"S3 keys cannot be longer than 1024 characters "
                f'("{"x" * 1025}" has 1025 characters)'
            ),
        ),
    ],
)
def test_init__invalid(key: str, expect: str) -> None:
    with raises(ValueError) as ex:
        S3Key(key)
    assert str(ex.value) == expect


@mark.parametrize(
    "base, append, expect",
    [
        ("", "clowns.jpg", "clowns.jpg"),
        ("private/", "/clowns.jpg", "private/clowns.jpg"),
        ("private", "clowns.jpg", "private/clowns.jpg"),
    ],
)
def test_join(base: str, append: str, expect: str) -> None:
    assert S3Key(base).join(append) == S3Key(expect)


def test_key() -> None:
    assert S3Key("clowns.jpg").key == "clowns.jpg"


@mark.parametrize(
    "key, expect",
    [
        ("", ""),
        ("clowns.jpg", "clowns.jpg"),
        ("private/clowns.jpg", "clowns.jpg"),
        ("staff/photos/clowns.jpg", "clowns.jpg"),
    ],
)
def test_leaf(key: str, expect: str) -> None:
    assert S3Key(key).leaf == expect


@mark.parametrize(
    "key, parent, expect",
    [
        (
            "private/clowns.jpg",
            "private",
            "clowns.jpg",
        ),
        (
            "private/clowns.jpg",
            "private/",
            "clowns.jpg",
        ),
        (
            "staff/photos/clowns.jpg",
            "staff",
            "photos/clowns.jpg",
        ),
    ],
)
def test_relative_to(key: str, parent: str, expect: str) -> None:
    assert S3Key(key).relative_to(parent) == expect


def test_relative_to__not_parent() -> None:
    with raises(ValueError) as ex:
        S3Key("clowns.jpg").relative_to("private")

    assert str(ex.value) == '"private" is not a parent of "clowns.jpg"'


@mark.parametrize(
    "base, append, expect",
    [
        ("private", "clowns.jpg", "private/clowns.jpg"),
    ],
)
def test_truediv(base: str, append: str, expect: str) -> None:
    assert S3Key(base) / append == S3Key(expect)

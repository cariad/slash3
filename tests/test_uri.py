from typing import Any, Optional

from pytest import mark, raises

from slash3 import S3Key, S3Uri


@mark.parametrize(
    "base, suffix, expect",
    [
        ("s3://circus/image-", "clowns.jpg", "s3://circus/image-clowns.jpg"),
    ],
)
def test_add(base: str, suffix: str, expect: str) -> None:
    assert S3Uri(base) + suffix == S3Uri(expect)


@mark.parametrize(
    "base, suffix, expect",
    [
        ("s3://circus/image-", "clowns.jpg", "s3://circus/image-clowns.jpg"),
    ],
)
def test_append(base: str, suffix: str, expect: str) -> None:
    assert S3Uri(base).append(suffix) == S3Uri(expect)


@mark.parametrize(
    "uri, expect",
    [
        ("s3://circus", "circus"),
        ("s3://circus/", "circus"),
        ("s3://circus/clowns.jpg", "circus"),
    ],
)
def test_bucket(uri: str, expect: str) -> None:
    assert S3Uri(uri).bucket == expect


@mark.parametrize(
    "compare_to, expect",
    [
        (S3Uri("s3://circus/clowns.jpg"), True),
        ("s3://circus/clowns.jpg", True),
        (S3Uri("s3://circus/jugglers.jpg"), False),
        ("s3://circus/jugglers.jpg", False),
    ],
)
def test_eq(compare_to: Any, expect: bool) -> None:
    assert (S3Uri("s3://circus/clowns.jpg") == compare_to) is expect


def test_init__invalid() -> None:
    with raises(ValueError) as ex:
        S3Uri("clowns.jpg")

    assert str(ex.value) == '"clowns.jpg" is not an S3 URI'


@mark.parametrize(
    "base, suffix, expect",
    [
        ("s3://circus", "clowns.jpg", "s3://circus/clowns.jpg"),
        ("s3://circus/", "clowns.jpg", "s3://circus/clowns.jpg"),
    ],
)
def test_join(base: str, suffix: str, expect: str) -> None:
    assert S3Uri(base).join(suffix) == S3Uri(expect)


@mark.parametrize(
    "uri, expect",
    [
        ("s3://circus/clowns.jpg", S3Key("clowns.jpg")),
        ("s3://circus/private/jugglers.jpg", S3Key("private/jugglers.jpg")),
    ],
)
def test_key(uri: str, expect: S3Key) -> None:
    assert S3Uri(uri).key == expect


@mark.parametrize(
    "uri, expect",
    [
        ("s3://circus/private/jugglers.jpg", "s3://circus/private/"),
        ("s3://circus/private/", "s3://circus/"),
        ("s3://circus/private", "s3://circus/"),
        ("s3://circus/", "s3://circus/"),
    ],
)
def test_parent(uri: str, expect: S3Key) -> None:
    assert S3Uri(uri).parent == expect


@mark.parametrize(
    "uri, parent, expect",
    [
        (
            "s3://circus/private/clowns.jpg",
            "s3://circus/private/",
            "clowns.jpg",
        ),
        (
            "s3://circus/private/clowns.jpg",
            "s3://circus/",
            "private/clowns.jpg",
        ),
    ],
)
def test_relative_to(uri: str, parent: str, expect: str) -> None:
    assert S3Uri(uri).relative_to(parent) == expect


def test_relative_to__different_bucket() -> None:
    with raises(ValueError) as ex:
        S3Uri("s3://circus/clowns.jpg").relative_to("s3://burgers/clowns.jpg")

    assert str(ex.value) == (
        'There is no relative path from "s3://burgers/clowns.jpg" to '
        '"s3://circus/clowns.jpg" because these URIs describe different '
        "buckets"
    )


def test_relative_to__not_parent() -> None:
    with raises(ValueError) as ex:
        S3Uri("s3://circus/clowns.jpg").relative_to("s3://circus/private/")

    assert str(ex.value) == (
        '"s3://circus/private/" is not a parent of "s3://circus/clowns.jpg"'
    )


@mark.parametrize(
    "uri",
    [
        "s3://circus/",
        "s3://circus/clowns.jpg",
        "s3://circus/private/",
    ],
)
def test_repr(uri: str) -> None:
    assert repr(S3Uri(uri)) == uri


@mark.parametrize(
    "base, append, expect",
    [
        ("s3://circus", "clowns.jpg", "s3://circus/clowns.jpg"),
        ("s3://circus/", "clowns.jpg", "s3://circus/clowns.jpg"),
    ],
)
def test_truediv(base: str, append: str, expect: str) -> None:
    joined = S3Uri(base) / append
    assert joined == S3Uri(expect)


@mark.parametrize(
    "bucket, key, expect",
    [
        ("circus", None, "s3://circus/"),
        ("circus", "clowns.jpg", "s3://circus/clowns.jpg"),
    ],
)
def test_to_uri(bucket: str, key: Optional[str], expect: str) -> None:
    assert S3Uri.to_uri(bucket, key=key).uri == expect

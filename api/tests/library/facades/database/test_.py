from library.facades.database import models


def test_(_clean_package_store_table):
    package_storage = models.PackageStorage(
        sub="sub 1",
        spec_id="spec id 1",
        version="version 1",
        updated_at="11",
        model_count=12,
        updated_at_spec_id="11#spec id 1",
    )
    package_storage.save()

    print(list(models.PackageStorage.scan()))

    assert False

import io
from datetime import datetime, timedelta, timezone
from unittest import mock  # python3
#from unittest.mock import MagicMock

import mock  # python2, after pip install mock
import pytest
from flask import Flask, json, jsonify, session, url_for
from flask_babelex import get_locale, to_user_timezone, to_utc
from flask_login import current_user
from flask_security import login_user
from flask_security.utils import login_user
from invenio_accounts.models import Role, User
from invenio_accounts.testutils import create_test_user, login_user_via_session
from mock import patch

from weko_records_ui.models import (
    InstitutionName
    ,FileSecretDownload
    ,FilePermission
    ,FileOnetimeDownload
)
    

institution_name = InstitutionName(
    name="test"
)


# InstitutionName
def test_InstitutionName_set_institution_name(app,):
    # Exception coverage
    institution_name.set_institution_name("test")


# FilePermission
def test_FilePermission_set_institution_name(app, db, db_FilePermission):
    db_FilePermission.find(
        user_id=db_FilePermission.id,
        record_id=db_FilePermission.record_id,
        file_name=db_FilePermission.file_name
    )


# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_FilePermission_init_file_permission -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_FilePermission_init_file_permission(app, db, db_FilePermission):
    db_FilePermission.init_file_permission(
        user_id=db_FilePermission.id,
        record_id=db_FilePermission.record_id,
        file_name=db_FilePermission.file_name,
        activity_id=db_FilePermission.usage_application_activity_id
    )


# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_FilePermission_update_status -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_FilePermission_update_status(app, db, db_FilePermission):
    f = db.session.query(FilePermission).first()
    assert f.status == -1
    db_FilePermission.update_status(
        permission=f,
        status=1
    )
    db.session.commit()
    f = db.session.query(FilePermission).first()
    assert f.status == 1


# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_FilePermission_update_open_date -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_FilePermission_update_open_date(app, db, db_FilePermission):
    f = db.session.query(FilePermission).first()
    db_FilePermission.update_open_date(
        permission=f,
        open_date=datetime(2022, 12, 31)
    )
    db.session.commit()
    f = db.session.query(FilePermission).first()
    assert f.open_date == datetime(2022, 12, 31)


# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_FilePermission_find_by_activity -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_FilePermission_find_by_activity(app, db, db_FilePermission):
    db_FilePermission.find_by_activity(
        activity_id=db_FilePermission.usage_application_activity_id
    )


# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_FilePermission_update_usage_report_activity_id -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_FilePermission_update_usage_report_activity_id(app, db, db_FilePermission):
    f = db.session.query(FilePermission).first()
    assert f.usage_application_activity_id == "test"
    db_FilePermission.update_usage_report_activity_id(
        permission=f,
        activity_id='test2'
    )
    db.session.commit()
    f = db.session.query(FilePermission).first()
    assert f.usage_report_activity_id == "test2"


# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_FilePermission_delete_object -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_FilePermission_delete_object(app, db, db_FilePermission):
    assert db.session.query(FilePermission).count() == 1
    db_FilePermission.delete_object(
        permission=db_FilePermission
    )
    assert db.session.query(FilePermission).count() == 0


def test_FileOnetimeDownload_update_download(app, db, db_FileOneTimeDownload):
    data1 = {
        "file_name": db_FileOneTimeDownload.file_name,
        "user_mail": db_FileOneTimeDownload.user_mail,
        "record_id": db_FileOneTimeDownload.record_id,
    }

    db_FileOneTimeDownload.update_download(
        data=data1
    )

# def find_list_permission_approved(record_id, file_name):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_find_list_permission_approved -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_find_list_permission_approved(app, records_restricted, users,db_file_permission):
    #32
    indexer, results = records_restricted
    recid = results[len(results)-1]["recid"]
    filename =results[len(results)-1]["filename"]
    assert len(FilePermission.find_list_permission_approved(users[0]["id"],recid.pid_value, filename)) == 0

# def find_by_activity:
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_find_by_activity -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_find_by_activity(db_file_permission):
    #34
    listpermission:list = FilePermission.find_by_activity("usage_application_activity_id_dummy1")

    sorted_list = sorted(listpermission, key= lambda x: x.id ,reverse=True)
    assert listpermission == sorted_list

# def find_downloadable_only(cls, **obj) -> list:
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_find_downloadable_only -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
@pytest.mark.skip(reason="'from sqlalchemy.dialects.postgresql import INTERVAL' can't tests on SQLite.")
def test_find_downloadable_only(app,db):
    # 35
    user_mail ='aaa@example.org' 
    record_id=1
    file_name="text.txt"
    created=datetime.now() - timedelta(2)
    with app.test_request_context():
        # with db.session.begin_nested():
        FileOnetimeDownload.create(**{"user_mail":user_mail,"record_id":record_id,"file_name":file_name,"download_count":0 ,"expiration_date":2})
        FileOnetimeDownload.create(**{"user_mail":user_mail,"record_id":record_id,"file_name":file_name,"download_count":1 ,"expiration_date":1})
        FileOnetimeDownload.create(**{"user_mail":user_mail,"record_id":record_id,"file_name":file_name,"download_count":1 ,"expiration_date":2})
        FileOnetimeDownload.create(**{"user_mail":user_mail,"record_id":record_id,"file_name":file_name,"download_count":1 ,"expiration_date":2})

        recs = FileOnetimeDownload.find_downloadable_only(user_mail=user_mail,record_id=record_id,file_name=file_name)
        assert len(recs) == 2


# def find_by_activity:
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_find_by_activity -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_init():
    # 36
    dl = FileSecretDownload("a","b","c",1,2)
    assert dl.file_name == "a"
    assert dl.user_mail == "b"
    assert dl.record_id == "c"
    assert dl.download_count == 1
    assert dl.expiration_date == 2

# def create(cls, **data):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_create -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_create(app,db):
    # 37 42
    with app.test_request_context():
        dl = FileSecretDownload.create(
                    file_name = "a"
                    ,user_mail ="b"
                    ,record_id = "c"
                    ,download_count = 1
                    ,expiration_date= 2
            )
        assert dl.id
        assert dl.created
        rec = FileSecretDownload.find(
                    id = dl.id
                    ,file_name = "a"
                    ,record_id = "c"
                    ,created = dl.created
            )
        assert len(rec) == 1
        rec = rec[0]
        assert rec.file_name == "a"
        assert rec.user_mail == "b"
        assert rec.record_id == "c"
        assert rec.download_count == 1
        assert rec.expiration_date == 2

    # 38
    with app.test_request_context():
        with patch("weko_records_ui.models.db.session.add", side_effect=Exception("test_error")):
            defaultlength = len(FileSecretDownload.query.filter_by().all())
            with pytest.raises(Exception):
                dl = FileSecretDownload.create(
                    file_name = "a"
                    ,user_mail ="b"
                    ,record_id = "c"
                )
                assert defaultlength == len(FileSecretDownload.query.filter_by().all())

# def update_download(cls, **data):
# .tox/c1/bin/pytest --cov=weko_records_ui tests/test_models.py::test_update_download -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-records-ui/.tox/c1/tmp
def test_update_download(app,db):
    with app.test_request_context():
        # 39
        dl = FileSecretDownload.create(
            file_name = "a"
            ,user_mail ="b"
            ,record_id = "c"
            ,download_count = 1
            ,expiration_date= 2
        )
        result = FileSecretDownload.update_download(
            id = dl.id
            ,file_name = "a"
            ,record_id = "c"
            ,created = dl.created
            ,download_count = 100
        )
        if result:
            assert result[0].download_count == 100
        else:
            assert False

        # 40
        assert FileSecretDownload.update_download(
            id = dl.id + 1
            ,file_name = "a"
            ,record_id = "c"
            ,created = dl.created
        ) == None
        assert FileSecretDownload.update_download(
            id = dl.id
            ,file_name = "a"
            ,record_id = "c"
            ,created = dl.created
        )
def test_update_download2(app,db):
    with app.test_request_context():
        # 41
        dl = FileSecretDownload.create(
            file_name = "a"
            ,user_mail ="b"
            ,record_id = "c"
            ,download_count = 1
            ,expiration_date= 2
        )
        with patch("weko_records_ui.models.db.session.merge", side_effect=Exception("test_error")):
            before = FileSecretDownload.query.filter_by().one_or_none().download_count
            try:
                dl = FileSecretDownload.update_download(
                    id = dl.id
                    ,file_name = "a"
                    ,record_id = "c"
                    ,created = dl.created
                    ,download_count = 200
                )
                assert False
            except:
                assert before == FileSecretDownload.query.filter_by().one_or_none().download_count

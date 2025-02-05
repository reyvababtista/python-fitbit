#!/usr/bin/env python

from datetime import datetime, timedelta

import firebase_admin
from firebase_admin import credentials

from fitbit.fitbit_client import Fitbit
from repository.csv import Csv
from repository.firestore import Firestore
from repository.fitbit_repository import Repository
from repository.gcloud import GoogleCloud
from repository.gcloud_repository import GoogleCloudRepository
from repository.realtime_database import Realtime


def init_firebase(certificate_path, database_url):
    cred = credentials.Certificate(certificate_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': database_url
    })

gc_repository: GoogleCloudRepository = None

def refresh(token):
    print("Refreshing token..")
    secrets = gc_repository.get_users_secrets()
    user_secret = [d for d in secrets if d["user_id"] == token["user_id"]]
    gc_repository.add_secret_version(
        secret_id=user_secret[0]["secret_id"], payload=token)


def main(request):
    today = datetime.today()
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/reyvababtista/Projects/python-fitbit/secrets/tigerawaredev-6692e3e245ac.json"

    gc = GoogleCloud("tigerawaredev")
    gc_repository = GoogleCloudRepository(gc=gc)
    firebase_credentials = gc_repository.get_firebase_credential()
    firebase_realtime_db_url = gc_repository.get_realtime_db_url()

    init_firebase(certificate_path=firebase_credentials,
                  database_url=firebase_realtime_db_url)

    root = 'fitbit'
    fs = Firestore(collect_name=root)
    rdb = Realtime(root=root)
    csv = Csv()
    repository = Repository(fs, csv, rdb)

    secrets = gc_repository.get_users_secrets()
    for secret in secrets:
        start_date = datetime.strptime(secret["start_date"], '%Y-%m-%d')
        end_date = datetime.strptime(secret["end_date"], '%Y-%m-%d') + timedelta(days=1)
        fitbit = Fitbit(
                client_id=secret["client_id"],
                client_secret=secret["client_secret"],
                access_token=secret["access_token"],
                refresh_token=secret["refresh_token"],
                refresh_cb=refresh
            )
        repository.set_config(fitbit=fitbit, date=today)
        repository.get_profile()
        repository.get_intraday()
        repository.get_time_series()

from fitbit.exceptions import HTTPBadRequest
from fitbit.fitbit_client import Fitbit
from repository.csv import Csv
from repository.firestore import Firestore
from repository.realtime_database import Realtime


class Repository():
    def __init__(self, firestore: Firestore, csv: Csv, rdb: Realtime):
        self.firestore = firestore
        self.csv = csv
        self.rdb = rdb
        self.set_data_source()

    def set_data_source(self, firestore: bool = False, csv: bool = False, rdb: bool = True):
        self.firestore_enabled = firestore
        self.csv_enabled = csv
        self.rdb_enabled = rdb

    def _log_err(self, err):
        print("  x", err)

    def set_config(self, fitbit: Fitbit, date):
        self.fitbit = fitbit
        self.date = date

    def get_profile(self):
        profile = self.fitbit.user_profile_get()['user']
        print("\n--------------------------------------------------")
        print(
            'You are authorized to access data for the user: {}'.format(
                profile['fullName']))
        print("--------------------------------------------------\n")

        if (self.rdb_enabled): self.rdb.store_profile(profile)
        if (self.firestore_enabled): self.firestore.store_profile(profile)
        if (self.csv_enabled): self.csv.store_profile(profile)
        return profile['encodedId']

    def get_intraday(self):
        steps = self.fitbit.intraday_time_series(
            resource="steps")
        if (self.rdb_enabled): self.rdb.store_intraday(data=steps, date=self.date, doc_name="steps")
        if (self.firestore_enabled): self.firestore.store_intraday(data=steps, date=self.date, doc_name="steps")
        if (self.csv_enabled): self.csv.store_intraday(data=steps, date=self.date, doc_name="steps")

        calories = self.fitbit.intraday_time_series(
            resource="calories")
        if (self.rdb_enabled): self.rdb.store_intraday(data=calories, date=self.date, doc_name="calories")
        if (self.firestore_enabled): self.firestore.store_intraday(data=calories, date=self.date, doc_name="calories")
        if (self.csv_enabled): self.csv.store_intraday(data=calories, date=self.date, doc_name="calories")

        distance = self.fitbit.intraday_time_series(
            resource="distance")
        if (self.rdb_enabled): self.rdb.store_intraday(data=distance, date=self.date, doc_name="distance")
        if (self.firestore_enabled): self.firestore.store_intraday(data=distance, date=self.date, doc_name="distance")
        if (self.csv_enabled): self.csv.store_intraday(data=calories, date=self.date, doc_name="calories")

        heart = self.fitbit.intraday_time_series(
            resource="heart")
        if (self.rdb_enabled): self.rdb.store_intraday(data=heart, date=self.date, doc_name="heart")
        if (self.firestore_enabled): self.firestore.store_intraday(data=heart, date=self.date, doc_name="heart")
        if (self.csv_enabled): self.csv.store_intraday(data=heart, date=self.date, doc_name="heart")
        try:
            elevation = self.fitbit.intraday_time_series(
                resource="elevation",
                start_date=self.date,
                end_date=self.date)

            if (self.rdb_enabled): self.rdb.store_intraday(data=elevation, date=self.date, doc_name="elevation")
            if (self.firestore_enabled): self.firestore.store_intraday(data=elevation, date=self.date,
                                                                       doc_name="elevation")
            if (self.csv_enabled): self.csv.store_intraday(data=elevation, date=self.date, doc_name="elevation")
        except HTTPBadRequest as e:
            self._log_err(e)

        try:
            floors = self.fitbit.intraday_time_series(
                resource="floors",
                start_date=self.date,
                end_date=self.date)

            if (self.rdb_enabled): self.rdb.store_intraday(data=floors, date=self.date, doc_name="floors")
            if (self.firestore_enabled): self.firestore.store_intraday(data=floors, date=self.date, doc_name="floors")
            if (self.csv_enabled): self.csv.store_intraday(data=floors, date=self.date, doc_name="floors")

        except HTTPBadRequest as e:
            self._log_err(e)

    def get_time_series(self):
        sleeps = self.fitbit.time_series(
            resource='sleep',
            base_date=self.date,
            end_date=self.date,
            api_version=1.2)
        if (self.rdb_enabled): self.rdb.store_time_series(data=sleeps, doc_name="sleeps")
        if (self.firestore_enabled): self.firestore.store_time_series(data=sleeps, doc_name="sleeps")
        if (self.csv_enabled): self.csv.store_time_series(data=sleeps, doc_name="sleeps")

        heart_rates = self.fitbit.time_series(
            resource='activities/heart',
            base_date=self.date,
            end_date=self.date, )
        if (self.rdb_enabled): self.rdb.store_time_series(data=heart_rates, doc_name="heart_rates")
        if (self.firestore_enabled): self.firestore.store_time_series(data=heart_rates, doc_name="heart_rates")
        if (self.csv_enabled): self.csv.store_time_series(data=heart_rates, doc_name="heart_rates")

        activity_calories = self.fitbit.time_series(
            resource='activities/activityCalories',
            base_date=self.date,
            end_date=self.date, )
        if (self.rdb_enabled): self.rdb.store_time_series(data=activity_calories, doc_name="activity_calories")
        if (self.firestore_enabled): self.firestore.store_time_series(data=activity_calories, doc_name="activity_calories")
        if (self.csv_enabled): self.csv.store_time_series(data=activity_calories, doc_name="activity_calories")

        calories = self.fitbit.time_series(
            resource='activities/calories',
            base_date=self.date,
            end_date=self.date)
        if (self.rdb_enabled): self.rdb.store_time_series(data=calories, doc_name="calories")
        if (self.firestore_enabled): self.firestore.store_time_series(data=calories, doc_name="calories")
        if (self.csv_enabled): self.csv.store_time_series(data=calories, doc_name="calories")

        calories_bmr = self.fitbit.time_series(
            resource='activities/caloriesBMR',
            base_date=self.date,
            end_date=self.date)
        if (self.rdb_enabled): self.rdb.store_time_series(data=calories_bmr, doc_name="calories_bmr")
        if (self.firestore_enabled): self.firestore.store_time_series(data=calories_bmr, doc_name="calories_bmr")
        if (self.csv_enabled): self.csv.store_time_series(data=calories_bmr, doc_name="calories_bmr")

        distance = self.fitbit.time_series(
            resource='activities/distance',
            base_date=self.date,
            end_date=self.date)
        if (self.rdb_enabled): self.rdb.store_time_series(data=distance, doc_name="distance")
        if (self.firestore_enabled): self.firestore.store_time_series(data=distance, doc_name="distance")
        if (self.csv_enabled): self.csv.store_time_series(data=distance, doc_name="distance")

        try:
            elevation = self.fitbit.time_series(
                resource='activities/elevation',
                base_date=self.date,
                end_date=self.date)
            if (self.rdb_enabled): self.rdb.store_time_series(data=elevation, doc_name="elevation")
            if (self.firestore_enabled): self.firestore.store_time_series(data=elevation, doc_name="elevation")
            if (self.csv_enabled): self.csv.store_time_series(data=elevation, doc_name="elevation")
        except HTTPBadRequest as e:
            self._log_err(e)

        try:
            floors = self.fitbit.time_series(
                resource='activities/floors',
                base_date=self.date,
                end_date=self.date)
            if (self.rdb_enabled): self.rdb.store_time_series(data=floors, doc_name="floors")
            if (self.firestore_enabled): self.firestore.store_time_series(data=floors, doc_name="floors")
            if (self.csv_enabled): self.csv.store_time_series(data=floors, doc_name="floors")

        except HTTPBadRequest as e:
            self._log_err(e)

        minutes_sedentary = self.fitbit.time_series(
            resource='activities/minutesSedentary',
            base_date=self.date,
            end_date=self.date)
        if (self.rdb_enabled): self.rdb.store_time_series(data=minutes_sedentary, doc_name="minutes_sedentary")
        if (self.firestore_enabled): self.firestore.store_time_series(data=minutes_sedentary, doc_name="minutes_sedentary")
        if (self.csv_enabled): self.csv.store_time_series(data=minutes_sedentary, doc_name="minutes_sedentary")

        minutes_lightly_active = self.fitbit.time_series(
            resource='activities/minutesLightlyActive',
            base_date=self.date,
            end_date=self.date)
        if (self.rdb_enabled): self.rdb.store_time_series(data=minutes_lightly_active, doc_name="minutes_lightly_active")
        if (self.firestore_enabled): self.firestore.store_time_series(data=minutes_lightly_active, doc_name="minutes_lightly_active")
        if (self.csv_enabled): self.csv.store_time_series(data=minutes_lightly_active, doc_name="minutes_lightly_active")

        minutes_fairly_active = self.fitbit.time_series(
            resource='activities/minutesFairlyActive',
            base_date=self.date,
            end_date=self.date)
        if (self.rdb_enabled): self.rdb.store_time_series(data=minutes_fairly_active, doc_name="minutes_fairly_active")
        if (self.firestore_enabled): self.firestore.store_time_series(data=minutes_fairly_active, doc_name="minutes_fairly_active")
        if (self.csv_enabled): self.csv.store_time_series(data=minutes_fairly_active, doc_name="minutes_fairly_active")

        minutes_very_active = self.fitbit.time_series(
            resource='activities/minutesVeryActive',
            base_date=self.date,
            end_date=self.date)
        if (self.rdb_enabled): self.rdb.store_time_series(data=minutes_very_active, doc_name="minutes_very_active")
        if (self.firestore_enabled): self.firestore.store_time_series(data=minutes_very_active, doc_name="minutes_very_active")
        if (self.csv_enabled): self.csv.store_time_series(data=minutes_very_active, doc_name="minutes_very_active")

        steps = self.fitbit.time_series(
            resource='activities/steps',
            base_date=self.date,
            end_date=self.date)
        if (self.rdb_enabled): self.rdb.store_time_series(data=steps, doc_name="steps")
        if (self.firestore_enabled): self.firestore.store_time_series(data=steps, doc_name="steps")
        if (self.csv_enabled): self.csv.store_time_series(data=steps, doc_name="steps")

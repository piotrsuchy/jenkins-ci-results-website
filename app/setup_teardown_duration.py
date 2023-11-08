from flask import current_app


class SetupDuration:
    def __init__(self):
        self._durations_state = {}

    def update_setup_start_time(self, setup_id, start_time):
        current_app.logger.error(f'UPDATE SETUP START TIME {start_time}')
        zero_indexed_setup_id = str(int(setup_id) - 1)
        self._durations_state[zero_indexed_setup_id] = start_time

    def get_setup_start_time(self, setup_id):
        zero_indexed_setup_id = str(int(setup_id) - 1)
        return self._durations_state.get(zero_indexed_setup_id, None)


class TeardownDuration:
    def __init__(self):
        self._durations_state = {}

    def update_teardown_start_time(self, setup_id, start_time):
        current_app.logger.error(f'UPDATE TEARDOWN START TIME {start_time}')
        zero_indexed_setup_id = str(int(setup_id) - 1)
        self._durations_state[zero_indexed_setup_id] = start_time

    def get_teardown_start_time(self, setup_id):
        zero_indexed_setup_id = str(int(setup_id) - 1)
        return self._durations_state.get(zero_indexed_setup_id, None)

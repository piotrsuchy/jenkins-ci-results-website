class ProgressManager:
    def __init__(self):
        self._progress_state = {}
        
    def update_progress(self, setup_id, data):
        if setup_id not in self._progress_state:
            self._progress_state[setup_id] = {'completed_tests': 0, 'total_tests': 0}
        
        # Logic to update the progress state based on the provided data
        # ...
        
    def get_progress(self, setup_id):
        return self._progress_state.get(setup_id, {'completed_tests': 0, 'total_tests': 0})

import csv
from datetime import datetime as dt
from pathlib import Path

from pep_parse.settings import FILE_FORMAT

BASE_DIR = Path(__file__).parent.parent
RESULT_DIR = 'results'
DATETIME = dt.now().strftime('%Y_%m_%d_%H_%M_%S')
PEP_STATUS_COUNTER = {
    'Active': 0,
    'Accepted': 0,
    'Deferred': 0,
    'Final': 0,
    'Provisional': 0,
    'Rejected': 0,
    'Superseded': 0,
    'Withdrawn': 0,
    'Draft': 0,
    'Other': 0,
    'Total': 0
}


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_counter = PEP_STATUS_COUNTER

    def process_item(self, item, spider):
        self.status_counter[item['status']] += 1
        self.status_counter['Total'] += 1

        return item

    def close_spider(self, spider):
        status_summary_filename = f'status_summary_{DATETIME}.{FILE_FORMAT}'
        results_path = BASE_DIR / RESULT_DIR
        results_path.mkdir(parents=True, exist_ok=True)
        status_summary_file_path = results_path / status_summary_filename

        with open(status_summary_file_path, 'w', newline='') as file:
            fieldnames = ['Статус', 'Количество']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for status, count in self.PEP_STATUS_COUNTER.items():
                writer.writerow(
                    {
                        'Статус': status,
                        'Количество': count
                    }
                )

BOT_NAME = 'pep_parse'
NEWSPIDER_MODULE = f'{BOT_NAME}.spiders'
SPIDER_MODULES = [NEWSPIDER_MODULE]
CSV_FILE_FORMAT = 'csv'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

FEEDS = {
    f'results/pep_%(time)s.{CSV_FILE_FORMAT}': {
        'format': CSV_FILE_FORMAT,
        'encoding': 'utf8',
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    }
}

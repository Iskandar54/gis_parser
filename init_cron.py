from crontab import CronTab

cron = CronTab(user='root')
job = cron.new(
    command='. /app/env.sh && cd /app && /usr/local/bin/python3 /app/main.py >> /app/logs/cron.log 2>&1',
    comment='2gis_parser'
)
job.setall('0 10 * * * ')
cron.write()

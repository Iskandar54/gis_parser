printenv | sed 's/^\(.*\)$/export \1/' > /app/env.sh
chmod +x /app/env.sh

python3 /app/init_cron.py

cron && tail -f /app/logs/cron.log
FROM python:3.10

WORKDIR /HarryPotterStatsBot

COPY requirements.txt /HarryPotterStatsBot/
RUN pip install -r /HarryPotterStatsBot/requirements.txt
COPY . /HarryPotterStatsBot/

CMD python3 /HarryPotterStatsBot/bot.py
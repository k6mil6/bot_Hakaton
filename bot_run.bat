@echo off

call venv\Scripts\activate

set TOKEN=6193825963:AAFVpKEbQ8veAygTrdBP8ECNfsBCZCrx1Kw
set CHAT_ID=-873191361
set DB_LINK=postgres://k6mil6:tfZ8PxAH6JSK@ep-round-sky-222264.us-east-2.aws.neon.tech/neondb

python main.py

pause
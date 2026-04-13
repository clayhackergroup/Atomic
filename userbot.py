import asyncio
import logging
import json
import os
import random
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.messages import ReportRequest, ReportSpamRequest

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CONFIG_FILE = "config.json"
ACCOUNTS_FILE = "accounts.json"
PROXIES_FILE = "proxies.json"
REPORTS_FILE = "reports.json"

REPORT_REASONS = {
    "spam": "spam",
    "violence": "violence", 
    "illegal": "illegal",
    "fake": "fake",
    "adult": "adult",
    "abuse": "harassment",
    "scam": "fraud",
    "drugs": "pornography",
    "pedo": "violence",
    "copyright": "copyright"
}

user_sessions = {}
active_clients = {}

def load_json(filepath, default=None):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return default if default is not None else {}

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def init_files():
    files = {
        CONFIG_FILE: {
            "admin_id": 8754040441,
            "max_reports": 100,
            "interval": 3,
            "image_path": "/home/clay/Desktop/6065510171_bb00e7222b_z.jpg",
            "rate_limit_wait": 60,
            "concurrent_reports": 1,
            "auto_retry": True,
            "retry_count": 3
        },
        ACCOUNTS_FILE: [],
        PROXIES_FILE: []
    }
    
    for filename, default_data in files.items():
        if not os.path.exists(filename):
            save_json(filename, default_data)

init_files()
config = load_json(CONFIG_FILE)
accounts = load_json(ACCOUNTS_FILE)
proxies = load_json(PROXIES_FILE, [])

logger.info(f"Loaded {len(accounts)} accounts, {len(proxies)} proxies")

def load_reports():
    return load_json(REPORTS_FILE, [])

def save_report(data):
    reports = load_reports()
    reports.append({**data, "timestamp": datetime.now().isoformat()})
    save_json(REPORTS_FILE, reports)

def get_proxy():
    if not proxies:
        return None
    p = random.choice(proxies)
    return f"http://{p.get('user')}:{p.get('pass')}@{p.get('host')}:{p.get('port')}" if p.get('user') else None

def get_entity_type(entity):
    if hasattr(entity, 'broadcast'):
        return "channel"
    elif hasattr(entity, 'megagroup'):
        return "supergroup"
    elif hasattr(entity, 'chat'):
        return "group"
    return "user"

async def report_single(client, entity, reason, event, reporter_id):
    entity_type = get_entity_type(entity)
    
    try:
        if entity_type in ["group", "supergroup", "channel"]:
            await client(ReportSpamRequest(
                channel=entity,
                participants=[reporter_id],
                reason=REPORT_REASONS.get(reason, "spam"),
                message=f"Report"
            ))
        else:
            await client(ReportRequest(
                peer=entity,
                reason=REPORT_REASONS.get(reason, "spam"),
                message=f"Report"
            ))
        return True
    except Exception as e:
        return False

async def report_with_account(client, event, entity, reason, count, interval, image_path, reporter_id):
    success = 0
    failed = 0
    rate_limited = False
    
    for i in range(1, count + 1):
        try:
            entity_type = get_entity_type(entity)
            
            if entity_type in ["group", "supergroup", "channel"]:
                await client(ReportSpamRequest(
                    channel=entity,
                    participants=[reporter_id],
                    reason=REPORT_REASONS.get(reason, "spam"),
                    message=f"Report #{i}"
                ))
            else:
                await client(ReportRequest(
                    peer=entity,
                    reason=REPORT_REASONS.get(reason, "spam"),
                    message=f"Report #{i}"
                ))
            
            success += 1
            
            save_report({
                "entity_id": str(entity.id),
                "entity_type": entity_type,
                "reason": reason,
                "reporter": reporter_id,
                "report_num": i
            })
            
            if i == 10 and image_path:
                try:
                    await event.respond(file=image_path, message=f"maga ladle meowwww gop gop gop")
                except: pass
            
            if i == 20:
                await event.respond(
                    f"⚠️ @mrdarkhorizon @spideyze\n"
                    f"⛔️ bjai tera time waste ho gaya me thanks\n"
                    f"👤 Reported: {entity.title or entity.id}"
                )
            
            if i % 10 == 0:
                await event.respond(f"✅ Progress: {i}/{count}")
            
            await asyncio.sleep(interval)
            
        except Exception as e:
            error_str = str(e).lower()
            if "rate" in error_str or "flood" in error_str:
                rate_limited = True
                wait_time = config.get("rate_limit_wait", 60)
                await event.respond(f"⚠️ Rate limited! Waiting {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                failed += 1
    
    return success, failed

async def report_multi_account(event, entity, reason, count):
    accs = load_json(ACCOUNTS_FILE, [])
    if not accs:
        await event.respond("❌ No accounts available!")
        return
    
    interval = config.get("interval", 3)
    image_path = config.get("image_path", "")
    reporter_id = event.sender_id
    reports_per_account = count // len(accs)
    remainder = count % len(accs)
    
    await event.respond(
        f"🚀 **Multi-Account Report Started!**\n\n"
        f"📱 Accounts: {len(accs)}\n"
        f"📊 Total Reports: {count}\n"
        f"📊 Per Account: ~{reports_per_account}\n"
        f"⚠️ Reason: {reason}"
    )
    
    tasks = []
    account_names = []
    
    for i, acc in enumerate(accs):
        session = acc.get("session", f"acc{i}")
        api_id = acc.get("api_id", 0)
        api_hash = acc.get("api_hash", "")
        
        if not api_id or not api_hash:
            continue
        
        acc_count = reports_per_account + (1 if i < remainder else 0)
        
        async def report_task(session_name, api_id, api_hash, acc_count):
            try:
                proxy = get_proxy()
                client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)
                async with client:
                    return await report_with_account(
                        client, event, entity, reason, acc_count,
                        interval, image_path, reporter_id
                    )
            except Exception as e:
                logger.error(f"Account error: {e}")
                return 0, acc_count
        
        tasks.append(report_task(session, api_id, api_hash, acc_count))
        account_names.append(session)
    
    results = await asyncio.gather(*tasks)
    
    total_success = sum(r[0] for r in results)
    total_failed = sum(r[1] for r in results)
    
    await event.respond(
        f"🎉 **Multi-Account Complete!**\n\n"
        f"✅ Total Successful: {total_success}\n"
        f"❌ Total Failed: {total_failed}\n"
        f"📱 Accounts Used: {len(tasks)}"
    )

async def report_group(client, event, group_input, reason, max_reports):
    try:
        if group_input.lstrip('-').isdigit() or group_input.startswith('-100'):
            entity = await client.get_entity(int(group_input))
        elif group_input.startswith('@'):
            entity = await client.get_entity(group_input)
        else:
            entity = await client.get_entity('@' + group_input)
    except Exception as e:
        await event.respond(f"❌ Error: Could not find {group_input}\n{str(e)[:200]}")
        return
    
    entity_type = get_entity_type(entity)
    entity_name = getattr(entity, 'title', None) or getattr(entity, 'username', None) or str(entity.id)
    interval = config.get("interval", 3)
    image_path = config.get("image_path", "")
    
    await event.respond(
        f"📋 **Target Found!**\n\n"
        f"🏷️ Name: {entity_name}\n"
        f"📌 Type: {entity_type}\n"
        f"🆔 ID: `{entity.id}`\n"
        f"⚠️ Reason: {reason}\n"
        f"📊 Reports: {max_reports}\n"
        f"⏱️ Interval: {interval}s\n\n"
        f"🚀 Starting..."
    )
    
    success, failed = await report_with_account(
        client, event, entity, reason, max_reports,
        interval, image_path, event.sender_id
    )
    
    await event.respond(
        f"🎉 **Completed!**\n\n"
        f"✅ Successful: {success}\n"
        f"❌ Failed: {failed}\n"
        f"👤 Target: {entity_name}"
    )

def main_menu():
    return (
        f"🔰 **REPORT MASTER PRO**\n\n"
        f"**Commands:**\n"
        f"/start - Start bot\n"
        f"/report <target> <reason> [count] - Single account\n"
        f"/multi <target> <reason> [count] - Multi account 🔥\n"
        f"/accounts - List accounts\n"
        f"/proxies - List proxies\n"
        f"/addacc - Add account\n"
        f"/addproxy - Add proxy\n"
        f"/status - Status\n"
        f"/stats - Statistics\n"
        f"/broadcast <msg> - Broadcast\n"
        f"/help - Help"
    )

@events.register(events.NewMessage(pattern='/start'))
async def start_handler(event):
    user = await event.get_sender()
    
    user_info = (
        f"👤 **New User**\n\n"
        f"👤 Username: @{user.username or 'None'}\n"
        f"📝 Name: {user.first_name}\n"
        f"🆔 ID: `{user.id}`\n"
        f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}"
    )
    
    try:
        await event.client.send_message(config["admin_id"], user_info)
    except: pass
    
    accs = load_json(ACCOUNTS_FILE, [])
    await event.respond(
        f"Welcome {user.first_name}! 👋\n\n"
        f"🆔 Your ID: `{user.id}`\n"
        f"📱 Accounts: {len(accs)}\n\n"
        f"{main_menu()}"
    )

@events.register(events.NewMessage(pattern='/help'))
async def help_handler(event):
    await event.respond(main_menu())

@events.register(events.NewMessage(pattern='/accounts'))
async def accounts_handler(event):
    accs = load_json(ACCOUNTS_FILE, [])
    prxs = load_json(PROXIES_FILE, [])
    await event.respond(
        f"📱 **Accounts:** {len(accs)}\n"
        f"🌐 **Proxies:** {len(prxs)}\n\n"
        f"Use /addacc to add accounts"
    )

@events.register(events.NewMessage(pattern='/proxies'))
async def proxies_handler(event):
    prxs = load_json(PROXIES_FILE, [])
    await event.respond(f"🌐 **Proxies:** {len(prxs)}\n\nUse /addproxy to add")

@events.register(events.NewMessage(pattern='/addacc'))
async def addacc_handler(event):
    await event.respond(
        f"📝 **Add Account**\n\n"
        f"Edit `accounts.json`:\n\n"
        f"```json\n"
        f"[\n"
        f"  {{\n"
        f"    \"api_id\": 12345678,\n"
        f"    \"api_hash\": \"hash\",\n"
        f"    \"session\": \"acc1\"\n"
        f"  }}\n"
        f"]\n"
        f"```"
    )

@events.register(events.NewMessage(pattern='/addproxy'))
async def addproxy_handler(event):
    await event.respond(
        f"🌐 **Add Proxy**\n\n"
        f"Edit `proxies.json`:\n\n"
        f"```json\n"
        f"[\n"
        f"  {{\n"
        f"    \"host\": \"ip\",\n"
        f"    \"port\": 8080,\n"
        f"    \"user\": \"user\",\n"
        f"    \"pass\": \"pass\"\n"
        f"  }}\n"
        f"]\n"
        f"```"
    )

@events.register(events.NewMessage(pattern='/report'))
async def report_handler(event):
    user_id = event.sender_id
    
    if user_id in user_sessions:
        await event.respond("⏳ Use /cancel")
        return
    
    parts = event.text.split()
    if len(parts) < 3:
        await event.respond(
            f"❌ **Usage:** `/report <target> <reason> [count]`\n\n"
            f"**Examples:**\n"
            f"`/report @group spam 100`\n"
            f"`/report @group violence`\n"
            f"`/report -100123 spam`\n\n"
            f"**Reasons:** {', '.join(REPORT_REASONS.keys())}"
        )
        return
    
    group_input = parts[1]
    reason = parts[2].lower()
    max_reports = int(parts[3]) if len(parts) > 3 else config.get("max_reports", 100)
    
    if reason not in REPORT_REASONS:
        await event.respond(f"❌ Invalid reason!")
        return
    
    user_sessions[user_id] = True
    
    accs = load_json(ACCOUNTS_FILE, [])
    if not accs:
        await event.respond("❌ No accounts!")
        del user_sessions[user_id]
        return
    
    first_acc = accs[0]
    proxy = get_proxy()
    
    async with TelegramClient(first_acc["session"], first_acc["api_id"], first_acc["api_hash"], proxy=proxy) as client:
        await report_group(client, event, group_input, reason, max_reports)
    
    del user_sessions[user_id]

@events.register(events.NewMessage(pattern='/multi'))
async def multi_handler(event):
    user_id = event.sender_id
    
    if user_id in user_sessions:
        await event.respond("⏳ Use /cancel")
        return
    
    parts = event.text.split()
    if len(parts) < 3:
        await event.respond(
            f"❌ **Usage:** `/multi <target> <reason> [count]`\n\n"
            f"Uses ALL accounts to report!\n\n"
            f"Example: `/multi @group spam 200`"
        )
        return
    
    group_input = parts[1]
    reason = parts[2].lower()
    count = int(parts[3]) if len(parts) > 3 else config.get("max_reports", 100)
    
    if reason not in REPORT_REASONS:
        await event.respond(f"❌ Invalid reason!")
        return
    
    user_sessions[user_id] = True
    
    try:
        if group_input.lstrip('-').isdigit() or group_input.startswith('-100'):
            entity = await event.client.get_entity(int(group_input))
        elif group_input.startswith('@'):
            entity = await event.client.get_entity(group_input)
        else:
            entity = await event.client.get_entity('@' + group_input)
    except Exception as e:
        await event.respond(f"❌ Error: {str(e)[:200]}")
        del user_sessions[user_id]
        return
    
    await report_multi_account(event, entity, reason, count)
    del user_sessions[user_id]

@events.register(events.NewMessage(pattern='/cancel'))
async def cancel_handler(event):
    user_id = event.sender_id
    if user_id in user_sessions:
        del user_sessions[user_id]
        await event.respond("✅ Cancelled!")
    else:
        await event.respond("❌ No operation")

@events.register(events.NewMessage(pattern='/status'))
async def status_handler(event):
    accs = load_json(ACCOUNTS_FILE, [])
    prxs = load_json(PROXIES_FILE, [])
    await event.respond(
        f"📊 **Status**\n\n"
        f"📱 Accounts: {len(accs)}\n"
        f"🌐 Proxies: {len(prxs)}\n"
        f"👥 Active: {len(user_sessions)}"
    )

@events.register(events.NewMessage(pattern='/stats'))
async def stats_handler(event):
    reports = load_reports()
    await event.respond(f"📈 **Total Reports:** {len(reports)}")

@events.register(events.NewMessage(pattern='/broadcast (.+)'))
async def broadcast_handler(event):
    if event.sender_id != config["admin_id"]:
        await event.respond("❌ Admin only!")
        return
    
    msg = event.text[11:]
    accs = load_json(ACCOUNTS_FILE, [])
    
    for acc in accs:
        try:
            async with TelegramClient(acc["session"], acc["api_id"], acc["api_hash"]) as client:
                await client.send_message(acc.get("broadcast_to", config["admin_id"]), msg)
        except Exception as e:
            logger.error(f"Broadcast error: {e}")
    
    await event.respond("✅ Broadcast sent!")

@events.register(events.NewMessage(incoming=True))
async def message_handler(event):
    if event.is_private and not event.message.text.startswith('/'):
        await event.respond(f"👋 Welcome!\n\n{main_menu()}")

async def main():
    accs = load_json(ACCOUNTS_FILE, [])
    if not accs:
        print("⚠️ No accounts! Edit accounts.json first")
        return
    
    first_acc = accs[0]
    logger.info(f"Starting with account: {first_acc.get('session')}")
    
    proxy = get_proxy()
    async with TelegramClient(first_acc["session"], first_acc["api_id"], first_acc["api_hash"], proxy=proxy) as client:
        for handler in [start_handler, report_handler, multi_handler, cancel_handler, status_handler, 
                       stats_handler, accounts_handler, proxies_handler, addacc_handler, addproxy_handler,
                       help_handler, broadcast_handler, message_handler]:
            client.add_event_handler(handler)
        
        logger.info("✅ Bot running!")
        await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())

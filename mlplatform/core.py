import asyncio,json,sqlite3,time,math
from pathlib import Path

def validate(event):
    if not isinstance(event,dict): raise ValueError('event must be object')
    for key in ('id','asset','timestamp','cpu'):
        if key not in event: raise ValueError(f'missing {key}')
    if not all(isinstance(event[k],str) and event[k].strip() for k in ('id','asset','timestamp')):
        raise ValueError('invalid identifiers')
    value=event['cpu']
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not 0<=value<=100:
        raise ValueError('cpu must be finite in [0,100]')
    from datetime import datetime
    stamp=datetime.fromisoformat(event['timestamp'].replace('Z','+00:00'))
    if stamp.tzinfo is None: raise ValueError('timestamp requires timezone')
    return event

async def ingest(events,path,workers=4):
    if workers<1: raise ValueError('workers must be positive')
    db=sqlite3.connect(path)
    db.execute('CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, asset TEXT, cpu REAL, body TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS deadletter (body TEXT, error TEXT)'); db.commit()
    q=asyncio.Queue(maxsize=32); counts={'accepted':0,'duplicate':0,'rejected':0}; latency=[]
    start=time.perf_counter()
    async def worker():
        while True:
            item=await q.get()
            try:
                if item is None: return
                event,t0=item
                try:
                    e=validate(event)
                    with db:
                        cursor=db.execute('INSERT OR IGNORE INTO events VALUES (?,?,?,?)',
                                          (e['id'],e['asset'],e['cpu'],json.dumps(e)))
                    counts['accepted' if cursor.rowcount else 'duplicate']+=1
                except (ValueError,TypeError) as exc:
                    with db: db.execute('INSERT INTO deadletter VALUES (?,?)',(json.dumps(event),str(exc)))
                    counts['rejected']+=1
                latency.append(time.perf_counter()-t0)
                await asyncio.sleep(0)
            finally: q.task_done()
    tasks=[asyncio.create_task(worker()) for _ in range(workers)]
    try:
        for event in events: await q.put((event,time.perf_counter()))
        for _ in tasks: await q.put(None)
        await asyncio.gather(*tasks)
        total=db.execute('SELECT COUNT(*) FROM events').fetchone()[0]
        summary=[{'asset':a,'events':n,'mean_cpu':v} for a,n,v in
                 db.execute('SELECT asset,COUNT(*),AVG(cpu) FROM events GROUP BY asset')]
        elapsed=time.perf_counter()-start
        return {**counts,'stored_total':total,'elapsed_seconds':elapsed,
                'events_per_second':len(events)/max(elapsed,1e-9),
                'latency_p95_ms':sorted(latency)[min(len(latency)-1,int(len(latency)*.95))]*1000 if latency else 0,
                'assets':summary,'execution':'local asyncio, synchronous transactional SQLite sink'}
    finally:
        for task in tasks:
            if not task.done(): task.cancel()
        await asyncio.gather(*tasks,return_exceptions=True)
        db.close()

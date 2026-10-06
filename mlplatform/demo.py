import argparse,asyncio,json,random
from pathlib import Path
from .core import ingest
def main():
    p=argparse.ArgumentParser(); p.add_argument('--events',type=int,default=200); p.add_argument('--workers',type=int,default=4)
    a=p.parse_args()
    if a.events<1 or a.workers<1: p.error('events/workers must be positive')
    rng=random.Random(7)
    events=[{'id':f'e-{i}','asset':f'asset-{i%4}','timestamp':'2026-01-01T00:00:00Z','cpu':rng.uniform(0,100)} for i in range(a.events)]
    events+=events[:5]+[{'id':'invalid','cpu':120}]
    Path('artifacts').mkdir(exist_ok=True)
    report=asyncio.run(ingest(events,'artifacts/events.sqlite',a.workers)); report['synthetic']=True
    Path('artifacts/report.json').write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))
if __name__=='__main__': main()

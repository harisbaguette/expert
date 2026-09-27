"""사건별 기록을 읽을 수 있는 보고서와 대조 CSV로 만든다."""
import csv
import gzip
import json
from collections import Counter
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
OUT = HERE.parent


def main():
    sources = json.loads((HERE / 'selected_cases.json').read_text())
    assessments = json.loads((HERE / 'case_assessments.json').read_text())
    by_id = {r['review_id']: r for r in sources}
    lines = ['# 실제 판례 24건 대입 결과', '',
             '검토일: 2026-09-17. 이 문서는 **판결문을 읽은 검토자가 현재 정의에 대입한 기록**이다. 실제 에이전트에 사실만 입력한 블라인드 실행 결과가 아니며, 아래 법리 재구성을 정답률·승소율로 환산하지 않는다.', '',
             '공통 흐름: 접수(M27·M31) → 사건·쟁점·완료 범위(M25·M34·M36) → 자료·반대 근거(M07·M12·M14·M18·M19) → 판단·계획(M21·M34·M35) → 필요한 실무(M09·M52·M53 등) → 반증·검증(M42·M43) → 쟁점별 결과·미완료·후속(M36·M40·M41). 다음 기록은 사건마다 이 공통 연결에 채워야 할 구체적인 내용을 적는다.', '',
             '모든 사건에서 기존 재료에 책임을 배정할 수 있었다. 그러나 **직무별 법적 요건·예외·증거·절차 계약과 해당 기능의 실증은 별도**다. 판결문에 없는 소송기록을 확보했다거나 자율 해결했다고 표시하지 않는다.', '',
             '| ID | 사건번호 | 사건의 어려운 부분 |', '|---|---|---|']
    for item in assessments:
        source = by_id[item['review_id']]
        lines.append(f'| {item["review_id"]} | {source["case"]} | {item["label"]} |')
    rows = []
    for item in assessments:
        source = by_id[item['review_id']]
        rid = item['review_id']
        text_file = f'재현/원문/{rid}_{source["id"]}.txt'
        raw_file = f'재현/원본/{source["id"]}.json.gz'
        lines += ['', f'## {rid} · {item["label"]}', '',
                  f'**{source["court"]} {source["date"]} · {source["case"]}**  ',
                  f'[로컬 원문 발췌·정리본]({quote(text_file)}) · [원본 JSON 압축본]({quote(raw_file)}) · [공식 원문 주소]({source["official_url"]})', '',
                  f'**선정 이유:** {item["complexity"]}', '',
                  f'**대입 질문:** {item["task"]}', '',
                  f'**판결문에 따른 답:** {item["reconstructed_answer"]}', '',
                  f'**실제 주문:** {source["order"]}', '',
                  f'**현재 재료에 대입:** {item["application"]}', '',
                  f'사용 재료: {" · ".join(item["materials"])}.', '',
                  f'**해결 가능성 판정:** 판결문에 기재된 핵심 법리는 위와 같이 재구성할 수 있다. {item["remaining_gap"]} 자율 실행은 미실시이며 사건 해결 능력은 미입증이다.', '',
                  f'**재시험용 변형 입력:** {item["mutation"]}', '',
                  f'**그때 요구할 반응:** {item["mutation_expected"]}', '',
                  '변형은 실제 판례의 추가 사실이 아니라 이번 검토에서 만든 시험 입력이다. 예상 반응을 기록했으며 실행 통과로 세지 않았다.']
        rows.append({'ID': rid, '사건번호': source['case'], '선고일': source['date'],
                     '사건명': item['label'], '필수분기': item['task'],
                     '재구성한답': item['reconstructed_answer'], '재료': ' '.join(item['materials']),
                     '미해결조건': item['remaining_gap'], '변형입력': item['mutation'],
                     '기대반응': item['mutation_expected'], '자율실행': '미실시',
                     '원본SHA256': source['sha256'], '원본경로': source['file']})
    (OUT / '02_24건_대입결과.md').write_text('\n'.join(lines) + '\n')
    with (OUT / '02_24건_대입결과.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with gzip.open(HERE / 'corpus_inventory.csv.gz', 'rt', encoding='utf-8') as f:
        inventory = list(csv.DictReader(f))
    groups = Counter((r['court'], r['date'], r['case']) for r in inventory if all(r[k] for k in ('court', 'date', 'case')))
    stats = {'selected': len(sources), 'unique_case_keys': len({(r['court'], r['date'], r['case']) for r in sources}),
             'categories': dict(Counter(r['category'] for r in sources)),
             'body_chars_total': sum(int(r['chars']) for r in sources),
             'en_banc': sum(int(r['en_banc']) for r in sources),
             'dissent_signal': sum(int(r['dissent_signal']) for r in sources),
             'corpus_duplicate_key_groups': sum(v > 1 for v in groups.values()),
             'corpus_duplicate_key_extra_records': sum(v - 1 for v in groups.values() if v > 1),
             'autonomous_run_count': 0, 'autonomous_success_rate': None}
    (HERE / 'review_statistics.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

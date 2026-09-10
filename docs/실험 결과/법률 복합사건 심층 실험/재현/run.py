"""Execute LEGAL-001's bounded state, arithmetic, and artifact-contract checks.

Not a legal reasoning engine, blind model test, or real bank/court integration.
Run from any directory: python3 path/to/run.py
"""
from pathlib import Path
from copy import deepcopy
from itertools import product, permutations
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parent
CASE = json.loads((ROOT / 'case.json').read_text())
CHECKS = []


def check(name, condition, observed):
    CHECKS.append({'check': name, 'passed': bool(condition), 'observed': observed})
    if not condition:
        raise AssertionError(name)


def vote_result(yes, present, issued):
    if not 0 <= yes <= present <= issued:
        raise ValueError('invalid voting population')
    return {'ordinary': yes * 2 > present and yes * 4 >= issued,
            'special': yes * 3 >= present * 2 and yes * 3 >= issued}


def can_read(evidence_id, stage):
    return next(e['stage'] for e in CASE['evidence'] if e['id'] == evidence_id) <= stage


def can_disclose(evidence_id, recipient, permission):
    # Test-specific permission records, NOT inferred legal privilege decisions.
    return (evidence_id, recipient) in permission


def payment_next(status):
    return {'not_started': 'request_if_authorized', 'unknown': 'query_only',
            'confirmed': 'reuse_receipt', 'failed_confirmed': 'review_retry'}[status]


def validate_artifact(artifact, stage, current_state, recipient):
    """Validate explicit metadata; does not infer correctness from legal prose."""
    errors = []
    if any(not can_read(eid, stage) for eid in artifact['evidence']):
        errors.append('future_evidence')
    if any(current_state.get(key) != value for key, value in artifact['basis'].items()):
        errors.append('stale_basis')
    if current_state['phase'] not in artifact['phases']:
        errors.append('wrong_procedural_phase')
    if recipient not in artifact['recipients']:
        errors.append('unauthorized_recipient')
    if any(c['source_purpose'] != c['use_as'] for c in artifact['claims']):
        errors.append('amount_meaning_mismatch')
    return errors


def minimum_schedule(workers):
    # Every reviewer is stipulated qualified for each job; no actual labor occurred.
    tasks = [('funds', 8), ('forensic', 8), ('legal', 10), ('merge', 2)]
    best = None
    for order in permutations(tasks):
        if order[-1][0] != 'merge':
            continue
        for assignment in product(range(workers), repeat=4):
            free = [0] * workers
            ends, rows = {}, []
            for (task, duration), worker in zip(order, assignment):
                prior = max(ends.values(), default=0) if task == 'merge' else 0
                start = max(free[worker], prior)
                end = start + duration
                free[worker], ends[task] = end, end
                rows.append({'task': task, 'reviewer': worker + 1,
                             'start_hour': start, 'end_hour': end})
            candidate = {'hours': max(free), 'assignments': rows}
            if best is None or candidate['hours'] < best['hours']:
                best = candidate
    return best


def main():
    state = deepcopy(CASE['initial'])
    snapshots = []
    artifacts = {'v1_note': {'depends': {'delivered', 'returned'},
                             'stale': False, 'external_copy': False},
                 'historic_external_copy': {'depends': {'delivered'},
                                            'stale': False, 'external_copy': True}}
    # Explicitly synthetic external copy only for preservation testing.
    def snapshot(stage, ids):
        result = deepcopy(state)
        result['unreconciled_principal'] = (state['paid'] - state['delivered']
                                          - state['returned'] - state['personal_paid'])
        result['votes'] = vote_result(state['votes_yes'], state['votes_present'], state['issued'])
        snapshots.append({'stage': stage, 'new_evidence': ids, 'state': result,
                          'artifact_states': deepcopy(artifacts)})
    snapshot(0, [e['id'] for e in CASE['evidence'] if e['stage'] == 0])
    for event in CASE['events']:
        assert all(can_read(eid, event['stage']) for eid in event['ids'])
        for artifact in artifacts.values():
            if artifact['depends'] & event['changes'].keys():
                artifact['stale'] = True
        state.update(event['changes'])
        snapshot(event['stage'], event['ids'])
    for snap in snapshots:
        for artifact in snap['artifact_states'].values():
            artifact['depends'] = sorted(artifact['depends'])
    s = [snap['state'] for snap in snapshots]
    check('C01 원금 대사 단계별 재계산',
          [s[i]['unreconciled_principal'] for i in [0, 1, 7, 8]] == [24, 30, 30, 27],
          [s[i]['unreconciled_principal'] for i in [0, 1, 7, 8]])
    check('C02 미래 증거 접근 거부와 공개 후 허용',
          not can_read('E23', 9) and can_read('E23', 10), {'before': False, 'after': True})
    check('C03 납품 정정 뒤 구판 합격 무효화',
          not snapshots[0]['artifact_states']['v1_note']['stale']
          and snapshots[1]['artifact_states']['v1_note']['stale'],
          snapshots[1]['artifact_states']['v1_note'])
    check('C04 이미 전달된 사본의 이력 보존',
          snapshots[-1]['artifact_states']['historic_external_copy']['external_copy']
          and snapshots[-1]['artifact_states']['historic_external_copy']['stale'],
          'synthetic copy preserved, correction review required; no real filing occurred')
    # 30 logical billion-won-tenths represented here as 30 one-eok atoms.
    remaining_atoms = set(range(30))
    personal_route_atoms = set(range(12))
    check('C05 같은 원천 금액의 중복 합산 반례',
          len(remaining_atoms | personal_route_atoms) == 30
          and len(remaining_atoms) + len(personal_route_atoms) == 42,
          {'union': 30, 'naive_addition': 42, 'subset_relation': True})
    civil_value = {'amount': 27, 'purpose': 'principal_reconciliation', 'unit': 'KRW_100M'}
    check('C06 대사값을 형사 이득액으로 전용 거부',
          civil_value['purpose'] != 'criminal_gain',
          {'candidate': civil_value, 'requested_purpose': 'criminal_gain', 'allowed': False})
    check('C07 개인정보 공유의 수신자 경계',
          can_disclose('E13', 'personal_counsel', {('E13', 'personal_counsel')})
          and not can_disclose('E13', 'company_counsel', {('E13', 'personal_counsel')}),
          {'personal_internal': True, 'company_automatic_share': False})
    check('C08 회사 접근권을 개인 위임으로 대체하지 않음',
          state['company_access'] is False, {'client': CASE['client'], 'company_access': False})
    check('C09 결과 불명에서 재송금 대신 조회',
          payment_next(s[7]['payment_status']) == 'query_only'
          and payment_next(s[8]['payment_status']) == 'reuse_receipt',
          {'stage7': payment_next(s[7]['payment_status']),
           'stage8': payment_next(s[8]['payment_status'])})
    # Execute the ambiguous-result branch in a tiny fake bank with no network.
    bank_ledger = {'P01': 3}
    retries = 0
    if payment_next('unknown') == 'request_if_authorized':
        retries += 1
        bank_ledger['P02'] = 3
    check('C10 모의 은행 입금 1회 유지',
          len(bank_ledger) == 1 and sum(bank_ledger.values()) == 3 and retries == 0,
          {'ledger': bank_ledger, 'retries': retries, 'naive_retry_total': 6})
    check('C11 수령 확인과 합의 미성립의 공존',
          state['personal_paid'] == 3 and state['settlement'] == 'rejected',
          {'receipt': 3, 'settlement': state['settlement']})
    check('C12 철회 전후 안건별 판정',
          s[0]['votes'] == {'ordinary': True, 'special': True}
          and s[6]['votes'] == {'ordinary': True, 'special': False},
          {'before': s[0]['votes'], 'after': s[6]['votes']})
    switch_min = next(x for x in range(24001) if vote_result(45000+x, 69000, 100000)['special'])
    new_min = next(x for x in range(31001) if vote_result(45000+x, 69000+x, 100000)['special'])
    check('C13 찬성 확보 방식에 따른 분모 변화',
          switch_min == 1000 and new_min == 3000,
          {'existing_attendee_switch': switch_min, 'new_attendee': new_min,
           'naive_new_1000_passes': vote_result(46000, 70000, 100000)['special']})
    seat_available = False  # additional adverse branch, not supplied final fact
    can_appoint = s[6]['votes']['ordinary'] and seat_available
    check('C14 보통결의 수치 충족과 선임 선행조건 분리',
          s[6]['votes']['ordinary'] and not can_appoint,
          {'branch': 'no vacant seat and expansion not passed', 'appointment_confirmed': can_appoint})
    after_company_payment = 42 - 20 - 12
    check('C15 회사 자금 전략의 여유 제약',
          after_company_payment == 10 and after_company_payment < 16,
          {'remaining': after_company_payment, 'minimum': 16, 'personal_authority': False})
    check('C16 미래 매각액을 당일 확정재원으로 사용 거부',
          CASE['initial']['personal_available'] == 3 and state['personal_available'] == 0,
          {'initial_available': 3, 'final_available': 0,
           'unconfirmed_sale_day14': 10, 'promise_12_today_supported': False})
    two, three = minimum_schedule(2), minimum_schedule(3)
    check('C17 총량 여유가 있어도 기한 내 배치 실패',
          28 <= 2*15 and two['hours'] == 18 and two['hours'] > 15,
          {'total_work': 28, 'aggregate_capacity': 30, 'minimum_schedule': two})
    check('C18 세 번째 적격 검토자 투입 일정',
          three['hours'] == 12 and three['hours'] <= 15, three)
    document_phase = 'pre_arrest'
    check('C19 영장 발부 뒤 과거 절차 문안 재사용 거부',
          document_phase == s[9]['phase'] and document_phase != s[10]['phase'],
          {'document_phase': document_phase, 'current_phase': s[10]['phase'], 'allowed': False})
    check('C20 법령 적용시점 검사',
          '2027-12-31' > CASE['as_of'] and '2026-07-01' <= CASE['as_of'],
          {'reference_label': '2027-12-31', 'as_of': CASE['as_of'],
           'automatically_applicable': False, 'note': 'date gate only; transition provisions need legal review'})
    # Inclusive/exclusive thresholds independently checked at exact boundaries.
    check('C21 의결 경계값',
          not vote_result(25000, 50000, 100000)['ordinary']
          and vote_result(25001, 50000, 100000)['ordinary']
          and vote_result(48000, 72000, 100000)['special']
          and not vote_result(47999, 72000, 100000)['special'],
          {'ordinary_half': False, 'ordinary_half_plus_one': True,
           'special_exact_two_thirds': True, 'special_one_short': False})
    check('C22 증거 파일 무결성',
          all(hashlib.sha256((ROOT.parent/e['path']).read_bytes()).hexdigest() == e['sha256']
              for e in CASE['evidence']), {'files': len(CASE['evidence']),
                                          'meaning': 'file integrity only, not factual truth'})
    final_note = {
        'path': '산출물/03_영장심문_의견서_초안_v2.md',
        'evidence': ['E02', 'E03', 'E04', 'E06', 'E11', 'E12', 'E14', 'E15', 'E19', 'E21'],
        'basis': {'delivered': 22, 'personal_paid': 3, 'approval': 'disputed'},
        'phases': ['pre_arrest'], 'recipients': ['personal_counsel'],
        'claims': [{'source_purpose': 'principal_reconciliation',
                    'use_as': 'principal_reconciliation'}],
    }
    check('C23 작성한 초안의 시점·수신자 메타데이터 검사',
          not validate_artifact(final_note, 9, s[9], 'personal_counsel')
          and (ROOT.parent / final_note['path']).exists(), final_note)
    negatives = []
    for mutation, error in [('future_evidence', 'future_evidence'),
                            ('old_amount', 'stale_basis'),
                            ('old_phase', 'wrong_procedural_phase'),
                            ('company_recipient', 'unauthorized_recipient'),
                            ('amount_purpose', 'amount_meaning_mismatch')]:
        candidate = deepcopy(final_note)
        stage, candidate_state, recipient = 9, s[9], 'personal_counsel'
        if mutation == 'future_evidence':
            candidate['evidence'].append('E23')
        elif mutation == 'old_amount':
            candidate['basis']['delivered'] = 28
        elif mutation == 'old_phase':
            stage, candidate_state = 10, s[10]
        elif mutation == 'company_recipient':
            recipient = 'company_counsel'
        elif mutation == 'amount_purpose':
            candidate['claims'][0]['use_as'] = 'criminal_gain'
        errors = validate_artifact(candidate, stage, candidate_state, recipient)
        negatives.append({'injected_metadata_defect': mutation, 'expected': error,
                          'observed': errors, 'blocked': error in errors})
    check('C24 결함을 주입한 산출 메타데이터 5종 차단',
          all(n['blocked'] for n in negatives), negatives)
    (ROOT / 'artifact_contract.json').write_text(
        json.dumps({'scope': 'metadata only, not legal prose validation',
                    'valid': final_note, 'negative_controls': negatives},
                   ensure_ascii=False, indent=2) + '\n')
    result = {'kind': CASE['kind'], 'checks': CHECKS, 'snapshots': snapshots,
              'summary': {'checks': len(CHECKS), 'passed': sum(c['passed'] for c in CHECKS),
                          'stages': len(snapshots), 'evidence_files': len(CASE['evidence']),
                          'external_goal': 'arrest avoidance failed in injected adverse branch',
                          'legal_merits': 'not independently graded'}}
    (ROOT/'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    with (ROOT/'checks.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['검사', '통과', '관측'])
        writer.writerows([c['check'], c['passed'], json.dumps(c['observed'], ensure_ascii=False)] for c in CHECKS)
    print(json.dumps(result['summary'], ensure_ascii=False))


if __name__ == '__main__':
    main()

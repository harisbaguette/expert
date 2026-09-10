"""Bounded contract simulations, not an implementation or benchmark of 166 agents.

Run: python3 "docs/실험 결과/재현/occupation-dynamic-models.py"
All world states, figures, rules, and tool responses here are synthetic.
The comparison omits one contract; it is not a measured previous product.
"""

import itertools
import json
from pathlib import Path


RESULTS = []


def record(name, roles, assumptions, worlds, omitted_contract, failures):
    RESULTS.append({
        "model": name,
        "role_ids": roles,
        "assumptions": assumptions,
        "worlds": worlds,
        "omitted_contract": omitted_contract,
        "omission_counterexamples": failures,
        "contract_checks": "passed in enumerated synthetic worlds",
    })


def lost_bank_reply():
    worlds, failures = [], 0
    for committed, query_available in itertools.product([False, True], repeat=2):
        paid = int(committed)
        if not query_available:
            action, state = "query pending; do not resend", "unresolved"
        elif committed:
            action, state = "reuse confirmed receipt", "confirmed"
        else:
            paid += 1
            action, state = "execute after confirmed nonexecution", "confirmed"
        assert paid <= 1
        assert state != "confirmed" or paid == 1
        naive_paid = int(committed) + 1
        failures += naive_paid > 1
        worlds.append({"initially_committed": committed, "query_available": query_available,
                       "action": action, "state": state, "payments": paid})
    record("은행 응답 유실", ["067", "074", "104", "164"],
           "조회가 성공하면 외부 실행 여부를 확정한다. 조회 불가를 실패 확정으로 간주하지 않는다.",
           worlds, "결과 불명과 확정 실패를 합쳐 재전송", failures)


def dependency_invalidation():
    graph = {"fact": ["calc", "model"], "calc": ["brief"], "brief": ["pdf"],
             "model": ["drawing"]}
    expected = {"fact": {"fact", "calc", "brief", "pdf", "model", "drawing"},
                "calc": {"calc", "brief", "pdf"}, "model": {"model", "drawing"},
                "none": set()}
    worlds, failures = [], 0
    for changed, oracle in expected.items():
        stale, pending = set(), [] if changed == "none" else [changed]
        while pending:
            item = pending.pop()
            if item not in stale:
                stale.add(item)
                pending.extend(graph.get(item, []))
        assert stale == oracle
        assert "unrelated_work" not in stale
        submitted_pdf = {"version": 1, "external_copy_preserved": True,
                         "correction_required": "pdf" in stale}
        assert submitted_pdf["external_copy_preserved"]
        naive = set() if changed == "none" else {changed}
        failures += naive != oracle
        worlds.append({"changed": changed, "invalidated": sorted(stale),
                       "submitted_artifact": submitted_pdf})
    record("새 증거·설계 변경의 전파", ["002", "031", "065", "122", "138"],
           "의존 그래프는 명시된 여섯 객체이며 제출된 외부 사본은 소급 삭제할 수 없다.",
           worlds, "바뀐 원본만 수정하고 파생 판단·파일의 합격을 유지", failures)


def shared_schedule():
    durations = [8, 8, 10]
    worlds, failures = [], 0
    for capacity in [8, 13, 16]:
        valid = []
        for assignment in itertools.product([0, 1], repeat=3):
            loads = [sum(d for d, worker in zip(durations, assignment) if worker == w)
                     for w in [0, 1]]
            if max(loads) <= capacity:
                valid.append({"assignment": assignment, "loads": loads})
        feasible = bool(valid)
        assert feasible == (capacity == 16)
        naive_feasible = sum(durations) <= 2 * capacity
        failures += naive_feasible and not feasible
        worlds.append({"capacity_per_person": capacity, "total_work": sum(durations),
                       "feasible": feasible, "witness": valid[:1],
                       "aggregate_only_says_feasible": naive_feasible})
    record("공동 전문가·설비 일정", ["032", "059", "096", "128"],
           "두 작업자, 각 8·8·10시간의 분할 불가 작업 세 개. 중단·분할·외주 불허.",
           worlds, "전체 시간 합계만 비교하고 작업별 배치를 생략", failures)


def composite_strategy():
    # No actual tax rates, legal conclusions, or predicted litigation outcomes.
    options = [
        {"name": "A", "tax_base": 1, "tax_adverse": 6, "other_cash": 5, "facts_consistent": True},
        {"name": "B", "tax_base": 3, "tax_adverse": 3, "other_cash": 2, "facts_consistent": True},
        {"name": "C", "tax_base": 2, "tax_adverse": 4, "other_cash": 3, "facts_consistent": True},
        {"name": "D", "tax_base": 1, "tax_adverse": 1, "other_cash": 1, "facts_consistent": False},
    ]
    feasible, worlds = [], []
    for option in options:
        remaining = [10 - option[tax] - option["other_cash"]
                     for tax in ["tax_base", "tax_adverse"]]
        valid = min(remaining) >= 4 and option["facts_consistent"]
        if valid:
            feasible.append(option["name"])
        worlds.append({**option, "cash_under_two_interpretations": remaining,
                       "all_constraints_met": valid})
    assert feasible == ["B"]
    naive = min(options, key=lambda x: x["tax_base"])["name"]
    assert naive == "A" and naive not in feasible
    record("법무·세무·현금 통합 전략", ["002", "006", "017", "066", "069"],
           "임의 금액 단위. 현금 10·최소 운영 여유 4. 두 해석은 가정이며 D는 동일 사실의 양립 불가 단정으로 정의했다. 적법한 예비적 주장은 오류로 세지 않는다.",
           worlds, "기준 해석의 세액 하나만 최소화", 1)


def joint_loss():
    worlds, failures = [], 0
    for shock in ["none", "one_position", "shared_collateral"]:
        direct = {"none": 0, "one_position": 3, "shared_collateral": 6}[shock]
        liquidity = 4 if shock == "shared_collateral" else 0
        total = direct + liquidity
        acceptable = total <= 8
        assert acceptable == (shock != "shared_collateral")
        failures += direct <= 8 and not acceptable
        worlds.append({"shock": shock, "direct_loss": direct,
                       "linked_liquidity_need": liquidity, "total_need": total,
                       "limit": 8, "within_limit": acceptable})
    record("공통 담보·유동성 손실", ["070", "072", "077", "153", "166"],
           "공동 충격에서는 직접 손실 6에 추가 현금 필요 4가 동시에 발생한다. 확률은 부여하지 않는다.",
           worlds, "직접 손실만 더하고 연쇄 현금 필요를 생략", failures)


def deletion_replay():
    worlds, failures = [], 0
    for order in itertools.permutations(["event_1", "delete_A", "late_replay"]):
        stored, naive, deleted = {"B": ["unrelated"]}, {"B": ["unrelated"]}, False
        for event in order:
            if event == "delete_A":
                deleted = True
                stored.pop("A", None)
                naive.pop("A", None)
            else:
                # Both records belong to A before the deletion; no renewed consent.
                if not deleted:
                    stored.setdefault("A", []).append(event)
                naive.setdefault("A", []).append(event)
        assert "A" not in stored and stored["B"] == ["unrelated"]
        failures += "A" in naive
        worlds.append({"arrival_order": order, "final_customers": sorted(stored),
                       "naive_resurrected_deleted_customer": "A" in naive})
    record("삭제 후 지연 이벤트·재처리", ["086", "109", "112", "114"],
           "삭제 범위는 고객 A의 이 두 과거 기록이며 재수집 동의·보존 예외가 없다. B는 삭제 대상 밖이다.",
           worlds, "삭제 시점 데이터만 지우고 후속 재처리를 통제하지 않음", failures)


def operation_capabilities():
    available = {("pptx", "create", "v1"), ("pdf", "export", "v1"),
                 ("cad", "render", "v1")}
    requested = [("pptx", "create", "v1"), ("pdf", "export", "v1"),
                 ("pptx", "edit_notes", "v1"), ("ppt", "preserve_edit", "v1"),
                 ("cad", "edit_assembly", "v1"), ("pptx", "create", "v2")]
    worlds, failures = [], 0
    for request in requested:
        supported = request in available
        naive = request[0] in {item[0] for item in available}
        failures += naive and not supported
        worlds.append({"request": request, "supported": supported,
                       "next": "execute" if supported else "configure and verify missing capability"})
    assert [w["supported"] for w in worlds] == [True, True, False, False, False, False]
    record("형식·작업·판본별 도구 지원", ["050", "058", "090", "123", "157"],
           "가상 도구 대장이다. 어떤 상용 프로그램이나 API의 실제 지원을 주장하지 않는다.",
           worlds, "같은 형식이 한 번 됐으면 모든 작업·판본도 된다고 가정", failures)


def diagnostic_bootstrap():
    worlds, failures = [], 0
    for observation, observation_allowed, execution_allowed in itertools.product(
            [True, False, None], [False, True], [False, True]):
        state, trace = "unknown", ["condition unknown"]
        # Diagnostic dependencies can be scheduled before the target is activated.
        if observation_allowed:
            trace.append("authorized diagnostic observation")
            state = {True: "active", False: "inactive", None: "unknown"}[observation]
        execute = state == "active" and execution_allowed
        if execute:
            trace.append("target execution allowed")
        else:
            trace.append("no target execution")
        assert not execute or (observation is True and observation_allowed and execution_allowed)
        assert observation_allowed or state == "unknown"
        # A plausible incomplete reading waits at the gate, never scheduling diagnosis.
        naive_state = "unknown"
        failures += state != naive_state
        worlds.append({"observation": observation, "observation_allowed": observation_allowed,
                       "execution_allowed": execution_allowed, "final_condition": state,
                       "execute": execute, "trace": trace})
    record("조건 판정과 진단의 순환 대기", ["034", "097", "112", "129", "135"],
           "진단 관측과 본 실행의 권한은 독립. 허용한 관측도 불명 결과를 낼 수 있다. 대상 조건은 처음에 미확인이다.",
           worlds, "불명 조건을 무조건 대기시켜 그 조건을 판별할 진단도 시작하지 않음", failures)


def main():
    for model in [lost_bank_reply, dependency_invalidation, shared_schedule,
                  composite_strategy, joint_loss, deletion_replay,
                  operation_capabilities, diagnostic_bootstrap]:
        model()
    result = {
        "kind": "bounded synthetic contract simulation; not agent performance",
        "models": RESULTS,
        "summary": {"model_count": len(RESULTS),
                    "enumerated_configurations": sum(len(m["worlds"]) for m in RESULTS),
                    "omission_counterexamples": sum(m["omission_counterexamples"] for m in RESULTS)},
    }
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()

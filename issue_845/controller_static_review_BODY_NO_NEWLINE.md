## Controller 复核：#845 authenticated formal intake 同宿主静态接线候选

延续 #845 评论 5903330714 的完整接续 HOLD。Management 干净 HEAD/远端 main 为 `a84ded6f08ef8f65c69c7bad6522250f8f15dc73`，tree `284bbb3b2b2d578b260e8a771b649477bce9c076`；Todo2 为 `aebf99d3f76ab98aec5820ec28c38f3e42ab9020`，tree `0ec35271869001d5c2fc4707d8d5c2fec475500e`。前序 K1 静态候选保持不变。

新独立锁定副本 `/Users/youmingding/.local/state/close_loop_management/issue845-post039-host-r1-formal-intake-locked-candidate` 在外部宿主增加六个非终止阶段：冻结 ReviewIntent／Controller payload、认证 Controller 评论、生成八个 Owner 槽位挑战、逐槽认证、finalize、调用现有 `produce_authenticated_current_facts` 一次并保全候选片段。它沿用当前源码的 `current_native_inputs`、`issue_845_authenticated_review_intake_v0_1` 和正式 producer，不改仓库模块；`REAL_RUN_ENABLED=False`。该接线只涉及外部 `host.py` 与 `k1_handoff.py`，其余四个运行文件与父候选逐字相同。

code-relay 在完成初步接线后因工作区额度耗尽中断，没有交回完整生命周期测试。Controller 独立复算候选 manifest SHA-256 `6a23b16e381ea22b80f71f0882c9dd67311d83639e793771208ee7d07b5a9dd5`、runtime diff `ecdd0f92f87372831b67cbdff1c1818e0f94754f5c75c26df7c975ec30548cf7`、4,588 项绑定哈希零差异和精确差异内容。Python 3.11 `-I -S -B` 隔离导入 PASS，输出 `occurrence_created=false`、`workload_runs=0`；原生认证 intake 的离线 mocked suite 为 105 passed。候选 manifest 的 `offline_import=PENDING` 是 relay 中断时状态；本段独立导入结果单独记录，不回写其原始 manifest。没有 token、host-stop、采集、K1 session 或 formal 输出文件。

**裁定：仅保留该精确源码形状的静态接线候选。** 六阶段宿主命令未作完整合成生命周期验证，真实 urllib／审计事件序列、Owner 槽位时序和 producer 原始回执均未现场验证；原生模块测试不替代宿主测试。`created_at` 必须预先冻结，并满足 occurrence→Controller→session→Owner→`created_at`→生产时间的顺序且早于宿主 24 小时截止。后续先在隔离合成环境证明同宿主正路径、缺失/错误槽位和一次性失败顺序，再独立审查 produced bytes、bridge、零写入完整包及 K3 currentness。新包不能自动替换 #806 R1 绑定的保留包 `sha256:1cea87fc91e069f7c2fafc3e03f14214ed18684c6fdd725cecebf254e2f2109b`。本记录没有授权新 occurrence、GitHub 现场读取、K1/K3、T0 或真实 A1；完整接续继续 HOLD。

CONTROL_RECORD=v1
KIND=ISSUE_845_AUTHENTICATED_FORMAL_INTAKE_STATIC_SEAM_REVIEW
SUBJECT=#845
PREDECESSOR=#845_5903330714
BINDS_SHA=a84ded6f08ef8f65c69c7bad6522250f8f15dc73
BINDS_TREE=284bbb3b2b2d578b260e8a771b649477bce9c076
HOST_MANIFEST_SHA256=sha256:6a23b16e381ea22b80f71f0882c9dd67311d83639e793771208ee7d07b5a9dd5
HOST_RUNTIME_DIFF_SHA256=sha256:ecdd0f92f87372831b67cbdff1c1818e0f94754f5c75c26df7c975ec30548cf7
FULL_SAME_HOST_CONTINUATION_READY=false
FRESH_OCCURRENCE_AUTHORIZED=false
K1_AUTHORIZED=false
T0_CONNECTIONS=0
REAL_A1=false
AUTHORITY_EFFECT=static_seam_candidate_only
NEXT_GATE=ISOLATED_SYNTHETIC_HOST_LIFECYCLE_AND_FORMAL_PRODUCTION_WITNESS
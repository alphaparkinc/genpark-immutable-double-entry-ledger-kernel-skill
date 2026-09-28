import sys, json
from client import ImmutableDoubleEntryLedger

def main():
    ledger = ImmutableDoubleEntryLedger()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(ledger.run_benchmark_ledger_kernel(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "post_journal_entry", "description": "Post balanced double-entry transaction block."},
                        {"name": "compute_trial_balance", "description": "Verify net-zero trial balance across all accounts."},
                        {"name": "verify_ledger_integrity", "description": "Verify cryptographic hash chain of ledger."},
                        {"name": "run_benchmark_ledger_kernel", "description": "Run general ledger test suite."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "post_journal_entry":
                    out = ledger.post_journal_entry(args.get("entry_id", ""), args.get("legs", []), args.get("currency", "USD"), args.get("description", ""))
                elif tname == "compute_trial_balance":
                    out = ledger.compute_trial_balance()
                elif tname == "verify_ledger_integrity":
                    out = ledger.verify_ledger_integrity()
                elif tname == "run_benchmark_ledger_kernel":
                    out = ledger.run_benchmark_ledger_kernel()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()

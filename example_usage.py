import sys, json
from client import ImmutableDoubleEntryLedger

def main():
    print("Testing ImmutableDoubleEntryLedger...")
    ledger = ImmutableDoubleEntryLedger()
    res = ledger.run_benchmark_ledger_kernel()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["unbalanced_rejected"] is True
    assert res["trial_balance_is_zero"] is True
    assert res["hash_chain_valid"] is True
    print("All Immutable Double Entry Ledger tests passed successfully!")

if __name__ == "__main__":
    main()

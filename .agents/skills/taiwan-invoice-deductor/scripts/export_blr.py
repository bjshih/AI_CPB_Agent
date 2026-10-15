#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper script to export Taiwan VAT 81-byte BLR TXT and review Excel report.
"""
import sys
import json
from pathlib import Path

def format_line(item: dict, seq: int, buyer_tax_id: str, tax_reg_no: str, period: str) -> str:
    fmt_code = str(item.get("format_code", "21"))[:2].ljust(2)
    reg_no = str(item.get("tax_register_no", tax_reg_no))[:9].ljust(9)
    seq_str = f"{seq:07d}"
    rec_period = str(item.get("period", period))[:5].ljust(5)
    buyer_id = str(item.get("buyer_tax_id", buyer_tax_id))[:8].ljust(8)
    seller_id = str(item.get("seller_tax_id", "00000000"))[:8].ljust(8)
    inv_no = str(item.get("invoice_number", ""))[:10].ljust(10)
    
    sales_amt = int(item.get("sales_amount", 0))
    tax_amt = int(item.get("tax_amount", 0))
    
    sales_str = f"{sales_amt:012d}"
    tax_type = str(item.get("tax_type", "1"))[:1]
    tax_str = f"{tax_amt:010d}"
    deduct_code = str(item.get("deduct_code", "1"))[:1]
    
    space_carrier = " " * 7
    space_reserved = " " * 1
    
    line = (
        f"{fmt_code}{reg_no}{seq_str}{rec_period}{buyer_id}{seller_id}"
        f"{inv_no}{sales_str}{tax_type}{tax_str}{deduct_code}{space_carrier}{space_reserved}"
    )
    
    encoded = line.encode("cp950")
    if len(encoded) != 81:
        raise ValueError(f"Line byte length must be 81, got {len(encoded)}: [{line}]")
    return line

def export_data(invoices_json_path: str, output_dir: str, buyer_tax_id: str, tax_reg_no: str, period: str):
    with open(invoices_json_path, "r", encoding="utf-8") as f:
        invoices = json.load(f)
    
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. 產生 81-byte TXT
    lines = []
    seq = 1
    for inv in invoices:
        inv_no = inv.get("invoice_number", "").strip()
        if not inv_no:
            continue
        line = format_line(inv, seq, buyer_tax_id, tax_reg_no, period)
        lines.append(line)
        seq += 1
        
    txt_path = out_dir / f"{buyer_tax_id}.TXT"
    txt_content = "\r\n".join(lines) + ("\r\n" if lines else "")
    with open(txt_path, "wb") as f:
        f.write(txt_content.encode("cp950"))
        
    # 2. 產出 Excel 或 CSV
    try:
        import pandas as pd
        rows = []
        for idx, inv in enumerate(invoices, start=1):
            rows.append({
                "序號": idx,
                "發票字軌號碼": inv.get("invoice_number", ""),
                "開立日期": inv.get("invoice_date", ""),
                "賣方統一編號": inv.get("seller_tax_id", ""),
                "買方統一編號": inv.get("buyer_tax_id", buyer_tax_id),
                "未稅銷售額": inv.get("sales_amount", 0),
                "營業稅額": inv.get("tax_amount", 0),
                "總金額": inv.get("total_amount", 0),
                "格式代號": inv.get("format_code", "21"),
                "扣抵代號": inv.get("deduct_code", "1"),
                "判定結果": "得扣抵" if str(inv.get("format_code", "21")) == "21" else "不得扣抵",
                "品名/備註": inv.get("item_description", ""),
                "法令審查說明": inv.get("tax_note", "")
            })
        df = pd.DataFrame(rows)
        excel_path = out_dir / f"營業稅進項申報審核清冊_{buyer_tax_id}_{period}.xlsx"
        df.to_excel(excel_path, index=False)
        print(f"Excel report generated: {excel_path}")
    except Exception as e:
        print(f"Notice: pandas not available or failed ({e}), writing CSV instead.")
        csv_path = out_dir / f"營業稅進項申報審核清冊_{buyer_tax_id}_{period}.csv"
        import csv
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["序號", "發票字軌號碼", "開立日期", "賣方統編", "未稅銷售額", "稅額", "總金額", "格式代號", "扣抵代號", "品名", "稅法說明"])
            for idx, inv in enumerate(invoices, start=1):
                writer.writerow([
                    idx, inv.get("invoice_number", ""), inv.get("invoice_date", ""),
                    inv.get("seller_tax_id", ""), inv.get("sales_amount", 0),
                    inv.get("tax_amount", 0), inv.get("total_amount", 0),
                    inv.get("format_code", "21"), inv.get("deduct_code", "1"),
                    inv.get("item_description", ""), inv.get("tax_note", "")
                ])
        print(f"CSV report generated: {csv_path}")

    print(f"BLR TXT successfully generated: {txt_path} ({len(lines)} records, CP950 CRLF 81-bytes)")

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python export_blr.py <invoices.json> <output_dir> <buyer_tax_id> <tax_reg_no> <period>")
        sys.exit(1)
    export_data(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

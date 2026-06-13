# -*- coding: utf-8 -*-

import csv
import re
import requests


# 第一题：拿债券数据并保存成 csv
def get_bond_data():
    url = "https://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN"

    # bondType=100001 是 Treasury Bond，issueYear 是发行年份
    params = {
        "bondType": "100001",
        "issueYear": "2023",
        "pageNo": "1",
        "pageSize": "20"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    data_list = []

    try:
        # 先请求第一页，看看一共有多少页
        res = requests.post(url, data=params, headers=headers, timeout=15)
        res.raise_for_status()
        res_json = res.json()

        if "data" not in res_json:
            print("返回数据格式不对")
            return data_list

        page_total = res_json["data"].get("pageTotal", 1)
        print("一共", page_total, "页")

        for page in range(1, page_total + 1):
            params["pageNo"] = str(page)

            res = requests.post(url, data=params, headers=headers, timeout=15)
            res.raise_for_status()
            res_json = res.json()

            rows = res_json["data"].get("resultList", [])
            print("正在处理第", page, "页，数据条数：", len(rows))

            for item in rows:
                one = {
                    "ISIN": item.get("isin", ""),
                    "Bond Code": item.get("bondCode", ""),
                    "Issuer": item.get("entyFullName", ""),
                    "Bond Type": item.get("bondType", ""),
                    "Issue Date": item.get("issueStartDate", ""),
                    "Latest Rating": item.get("debtRtng", "")
                }
                data_list.append(one)

    except Exception as e:
        print("获取数据时出错：", e)

    return data_list


def save_csv(data_list, file_name):
    columns = [
        "ISIN",
        "Bond Code",
        "Issuer",
        "Bond Type",
        "Issue Date",
        "Latest Rating"
    ]

    try:
        with open(file_name, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data_list)

        print("已经保存到", file_name)

    except Exception as e:
        print("保存 csv 时出错：", e)


# 把中文日期转成 2023-06-02 这种格式
def format_date(date_text):
    m = re.search(r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日", date_text)

    if m:
        year = m.group(1)
        month = m.group(2).zfill(2)
        day = m.group(3).zfill(2)
        return year + "-" + month + "-" + day

    return date_text


# 第二题：正则匹配函数
def reg_search(text, regex_list):
    result = []

    for rule in regex_list:
        one_result = {}

        for name in rule:
            pattern = rule[name]

            # 题目里给的是“自定义”，所以这里按字段单独处理
            if pattern == "*自定义*":
                if name == "标的证券":
                    m = re.search(r"\d{6}\.(SH|SZ|BJ)", text)
                    if m:
                        one_result[name] = m.group(0)
                    else:
                        one_result[name] = ""

                elif name == "换股期限":
                    date_list = re.findall(
                        r"\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日",
                        text
                    )

                    new_list = []
                    for d in date_list:
                        new_list.append(format_date(d))

                    one_result[name] = new_list[:2]

                else:
                    one_result[name] = ""

            else:
                # 如果传进来的是普通正则，就直接匹配
                match_list = re.findall(pattern, text, re.S)

                if len(match_list) == 0:
                    one_result[name] = ""
                elif len(match_list) == 1:
                    one_result[name] = match_list[0]
                else:
                    one_result[name] = match_list

        result.append(one_result)

    return result


if __name__ == "__main__":
    # 第一题
    bond_data = get_bond_data()

    if len(bond_data) > 0:
        save_csv(bond_data, "bond_data.csv")
    else:
        print("没有拿到债券数据")

    print("-" * 40)

    # 第二题简单测试
    text = """
    标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
    有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债
    券。
    换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
    之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
    日至 2027 年 6 月 1 日止。
    """

    regex_list = [
        {
            "标的证券": "*自定义*",
            "换股期限": "*自定义*"
        }
    ]

    print(reg_search(text, regex_list))

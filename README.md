# Orbitfin 测试题

这个仓库放的是本次测试题代码，主要写了两个部分。

## 1. 债券数据获取

代码里用 `requests` 请求中国货币网的数据接口，筛选条件是：

- Bond Type：Treasury Bond
- Issue Year：2023

最后把需要的字段保存到 `bond_data.csv`。

保存的字段有：

- ISIN
- Bond Code
- Issuer
- Bond Type
- Issue Date
- Latest Rating

## 2. reg_search 函数

第二部分是自己写了一个 `reg_search` 函数。

传入文本和正则规则后，返回匹配结果。

题目里的例子主要提取两个内容：

- 标的证券：提取类似 `600900.SH` 的股票代码
- 换股期限：提取两个日期，并转成 `yyyy-mm-dd` 格式

## 怎么运行

先安装依赖：

```bash
pip install -r requirements.txt
```

然后运行：

```bash
python main.py
```

如果第一题数据获取成功，会生成：

```text
bond_data.csv
```

## 文件

- `main.py`：代码文件
- `requirements.txt`：依赖
- `README.md`：简单说明

## 备注

如果网站临时访问不了，第一题可能会拿不到数据，但第二题的正则函数可以正常运行。

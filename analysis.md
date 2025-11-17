# 预测准确性分析

本次共有 42 份 PDF 预测报告，其中文件名以 **a** 结尾视为真实成功（21 份），以 **c** 结尾视为真实失败（21 份）。

## 汇总指标
- 明确给出“成功/失败”判断的报告：42/42（100% 覆盖率）。
- 在全部 42 份报告上计算的总体准确率：45.2%（19/42）。
- 预测为“成功”的报告 32 份，其中 15 份真实成功；预测为“失败”的报告 10 份，其中 4 份真实失败。

## 混淆矩阵（行=模型预测，列=真实）
| 预测\\真实 | 成功 | 失败 |
| --- | --- | --- |
| 成功 | 15 | 17 |
| 失败 | 6 | 4 |

## Overall 评分对比
| 实际结果 | 样本数 | 平均值 | 中位数 |
| --- | --- | --- | --- |
| 成功（a） | 21 | 7.92 | 8.27 |
| 失败（c） | 21 | 7.74 | 8.19 |

> 真实成功公司的平均 Overall 评分（7.92）比真实失败公司（7.74）高 0.18, 真实成功公司评分中位数8.27也大于真实失败公司中位数8.19分.
## 单个文件预测结果与评分
| 文件 | 实际 | 预测 | Overall 评分 |
| --- | --- | --- | --- |
| 1001a.pdf | success | success | 8.50 |
| 1002c.pdf | failure | failure | 8.50 |
| 1005a.pdf | success | failure | 8.27 |
| 1112c.pdf | failure | success | 8.19 |
| 137a.pdf | success | success | 7.47 |
| 145a.pdf | success | success | 7.40 |
| 162a.pdf | success | success | 8.30 |
| 16a.pdf | success | failure | 7.50 |
| 177c.pdf | failure | failure | 8.04 |
| 195a.pdf | success | success | 8.43 |
| 204a.pdf | success | success | 8.10 |
| 235c.pdf | failure | success | 8.50 |
| 25a.pdf | success | failure | 7.63 |
| 26c.pdf | failure | success | 6.38 |
| 289c.pdf | failure | success | 8.56 |
| 355c.pdf | failure | success | 8.12 |
| 369a.pdf | success | success | 7.41 |
| 379c.pdf | failure | success | 8.50 |
| 454c.pdf | failure | success | 4.25 |
| 485c.pdf | failure | success | 8.39 |
| 503a.pdf | success | success | 8.17 |
| 510a.pdf | success | failure | 4.50 |
| 531c.pdf | failure | failure | 7.30 |
| 557c.pdf | failure | success | 8.25 |
| 562c.pdf | failure | success | 8.27 |
| 572a.pdf | success | success | 8.40 |
| 605c.pdf | failure | success | 8.22 |
| 617c.pdf | failure | failure | 8.42 |
| 619c.pdf | failure | success | 8.62 |
| 625a.pdf | success | success | 8.60 |
| 642a.pdf | success | failure | 7.20 |
| 685a.pdf | success | success | 8.46 |
| 738a.pdf | success | success | 8.60 |
| 785c.pdf | failure | success | 7.50 |
| 797a.pdf | success | success | 8.50 |
| 803c.pdf | failure | success | 5.89 |
| 835c.pdf | failure | success | 7.80 |
| 846a.pdf | success | success | 8.10 |
| 858a.pdf | success | failure | 8.43 |
| 875a.pdf | success | success | 8.30 |
| 898c.pdf | failure | success | 7.00 |
| 98c.pdf | failure | success | 7.92 |

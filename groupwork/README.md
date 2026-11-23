# Project 2 — 5020 Maths for AI

主报告：`groupwork5020.md`。Markdown 公式使用标准 `$...$` 与 `$$...$$`；请在支持 MathJax/KaTeX 的 Markdown 查看器中阅读。图片使用相对路径，移动报告时请同时保留 `figures/`。

本地已验证环境：Python 3.11.5、NumPy 1.24.3、Matplotlib 3.7.2。

```powershell
python code/experiments.py
python code/verify.py
```

脚本从自身位置解析输出目录，可以从任意工作目录运行。已有依赖即可运行；需要新环境时可执行 `python -m pip install -r requirements.txt`。

模块：`model.py` 定义模型与谱半径；`optimizers.py` 执行迭代；`experiments.py` 生成全部实验；`verify.py` 核查独立数学性质。`data/` 保存完整轨迹、汇总表、稳定性网格与环境记录。所有实验确定性，无随机种子。重新运行覆盖生成的图表与数据，不修改报告。

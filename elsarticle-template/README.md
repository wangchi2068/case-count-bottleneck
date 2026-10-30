# Elsevier elsarticle LaTeX 完整模版包 (v3.5)

本模版包为 Elsevier 期刊（包含 *Epidemics*）官方标准投稿 LaTeX 模版套件。

## 目录文件说明

| 文件名 | 类型 | 说明 |
|---|---|---|
| `elsarticle.cls` | 核心类文件 | Elsevier 官方文档类（最新 v3.5） |
| `elsarticle-num.bst` | 参考文献样式 | 顺序编号样式（*Epidemics* 推荐标准） |
| `elsarticle-num-names.bst` | 参考文献样式 | 顺序编号加作者名样式 |
| `elsarticle-harv.bst` | 参考文献样式 | Harvard 作者-年份样式 |
| `elsarticle-template-num.tex` | 模版源码 | 顺序编号范例源码（推荐作为新稿件起点） |
| `elsarticle-template-num-names.tex` | 模版源码 | 编号+作者名范例源码 |
| `elsarticle-template-harv.tex` | 模版源码 | 哈佛格式范例源码 |
| `elsdoc.pdf` | 官方使用手册 | Elsevier 官方完整用法文档（参数、双盲审、多作者机构排版规范） |
| `elsarticle-template-num.pdf` | 编译预览 | 预编译生成的 PDF 预览文件 |

## 快速编译测试

本地已配置 `tectonic` 编译器，可在本目录下直接运行：

```bash
tectonic elsarticle-template-num.tex
```

若使用标准 TeXLive / pdflatex / xelatex：

```bash
pdflatex elsarticle-template-num.tex
bibtex elsarticle-template-num
pdflatex elsarticle-template-num.tex
pdflatex elsarticle-template-num.tex
```

## Epidemics 投稿常用文档类选项

```latex
%% 初稿送审（单栏双倍行距、便于审稿人阅读）：
\documentclass[preprint,12pt]{elsarticle}

%% 双盲审格式（如期刊要求 double-blind）：
\documentclass[preprint,12pt,doubleblind]{elsarticle}

%% 最终排版预估（双栏排版）：
\documentclass[5p,twocolumn]{elsarticle}
```

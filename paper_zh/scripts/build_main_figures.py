"""Compose the five main figures and three supplement figures.

Each source PDF holds one or more panels.  Panels are placed individually at
roughly half text width so their original 7--9 pt fonts stay legible after the
composite is scaled to \\textwidth.
"""

from pathlib import Path

import fitz
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from PIL import Image

matplotlib.use("Agg")
matplotlib.rcParams.update({
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "font.size": 7,
})

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
OUT = FIG
FONT_CN = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc")

BLUE = "#0072B2"
ORANGE = "#D55E00"
GREEN = "#009E73"
GREY = "#6E6E6E"
PINK = "#CC79A7"

PAGE_W = 470.0
MARGIN = 17.0
COL_W = (PAGE_W - 2 * MARGIN - 8) / 2
GAP = 7.0


def src_rect(path):
    doc = fitz.open(path)
    rect = doc[0].rect
    doc.close()
    return rect


_TIGHT = {}


def tight_clip(path, clip):
    """Trim surrounding white space of one panel."""
    key = (str(path), tuple(clip))
    if key in _TIGHT:
        return _TIGHT[key]
    doc = fitz.open(path)
    page = doc[0]
    pix = page.get_pixmap(clip=clip, dpi=200, alpha=False)
    arr = np.frombuffer(pix.samples, dtype=np.uint8)
    arr = arr.reshape(pix.height, pix.width, pix.n)
    mask = (arr[:, :, :3] < 250).any(axis=2)
    ys, xs = np.where(mask)
    doc.close()
    if len(xs) == 0:
        _TIGHT[key] = clip
        return clip
    pad = 2.0
    x0 = clip.x0 + xs.min() / pix.width * clip.width - pad
    x1 = clip.x0 + (xs.max() + 1) / pix.width * clip.width + pad
    y0 = clip.y0 + ys.min() / pix.height * clip.height - pad
    y1 = clip.y0 + (ys.max() + 1) / pix.height * clip.height + pad
    out = fitz.Rect(max(clip.x0, x0), max(clip.y0, y0),
                    min(clip.x1, x1), min(clip.y1, y1))
    _TIGHT[key] = out
    return out


def place_pdf(page, path, rect, clip=None):
    doc = fitz.open(path)
    page.show_pdf_page(fitz.Rect(rect), doc, 0, clip=clip)
    doc.close()


def panel_rect(path, index, count):
    rect = src_rect(path)
    w = rect.width / count
    return fitz.Rect(index * w, 0, (index + 1) * w, rect.height)


def label(page, letter, x, y):
    page.insert_text(
        fitz.Point(x, y + 8),
        letter,
        fontsize=9,
        fontname="ArialBold",
        fontfile=r"C:\Windows\Fonts\arialbd.ttf",
        color=(0, 0, 0),
    )


LABEL_H = 11.0

# Fraction of the source width at which two side-by-side panels are separated.
# The value sits in the white gutter between the left panel's ink and the right
# panel's y-axis label, so neither panel loses a tick label or a bar.
SPLITS = {
    "fig_02_variance_theory.pdf": 0.502,
    "fig_04_vR_precision.pdf": 0.481,
    "fig_05_levers_budget.pdf": 0.520,
    "fig_06_renewal_scale.pdf": 0.5045,
    "fig_09_denominator_noise.pdf": 0.483,
    "fig_11_reporting_adjustment.pdf": 0.420,
    "fig_13_scale_vs_seasons.pdf": 0.528,
    "fig_14_peak_decomp.pdf": 0.5015,
    "fig_15_period_season_iqr.pdf": 0.454,
}


def split_rects(path):
    """Return the left and right panel clips with a shared clean boundary."""
    r = src_rect(path)
    s = SPLITS[Path(path).name]
    return (fitz.Rect(0, 0, r.width * s, r.height),
            fitz.Rect(r.width * s, 0, r.width, r.height))


def add_pdf_row(page, y, specs):
    """specs: list of (letter, path, clip).  Equal widths, letter above each."""
    n = len(specs)
    width = (PAGE_W - 2 * MARGIN - GAP * (n - 1)) / n
    heights = []
    for letter, path, clip in specs:
        r = src_rect(path) if clip is None else tight_clip(path, clip)
        heights.append(width * r.height / r.width)
    row_h = LABEL_H + max(heights)
    for i, (letter, path, clip) in enumerate(specs):
        x = MARGIN + i * (width + GAP)
        h = heights[i]
        top = y + LABEL_H + (max(heights) - h) / 2
        use = clip if clip is None else tight_clip(path, clip)
        place_pdf(page, path, (x, top, x + width, top + h), use)
        label(page, letter, x + 1.0, y)
    return y + row_h


def crop_schematic():
    """Crop white margins and the lower estimand boxes of the flowchart."""
    path = FIG / "fig_01_model_schematic.png"
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im)
    mask = (arr < 248).any(axis=2)
    ys, xs = np.where(mask)
    x0, x1 = xs.min(), xs.max() + 1
    y0, y1 = ys.min(), ys.max() + 1
    y1 = min(y1, int(im.height * 0.4052))
    crop = im.crop((x0, y0, x1, y1))
    out = FIG / "_schematic_top.png"
    crop.save(out, dpi=(300, 300))
    return out


def new_panel_vh(path):
    R, vR, k, rho, tau = 1.15, 0.04, 0.35, 0.25, 0.15
    vH = tau ** 2 * (R ** 2 + vR)
    AH = R + rho * (1 + tau ** 2) * (R ** 2 + vR) / k
    mx = AH / (vR + vH)
    m = np.logspace(0, 3, 500)
    v = vR + vH + AH / m

    fig, ax = plt.subplots(figsize=(2.16, 2.0))
    fig.subplots_adjust(left=0.22, right=0.97, bottom=0.18, top=0.95)
    ax.semilogx(m, v, color=BLUE, lw=1.5, label=r"$V_H(m)$")
    ax.semilogx(m, vR + AH / m, color=GREY, lw=0.9, ls="--",
                label=r"$v_R+A_H/m$")
    ax.axhline(vR + vH, color=ORANGE, lw=0.8, ls=":")
    ax.text(1.15, vR + vH + 0.011, r"$v_R+v_H$", color=ORANGE,
            fontproperties=FONT_CN, fontsize=6.4)
    ax.plot([mx], [vR + vH + AH / mx], "o", ms=3.2, color=GREEN, zorder=5)
    ax.annotate("平衡规模 30.4", xy=(mx, vR + vH + AH / mx),
                xytext=(1.6, 0.168), fontproperties=FONT_CN, fontsize=6.2,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=GREEN,
                                shrinkA=1, shrinkB=2))
    ax.set_xlim(1, 1000)
    ax.set_ylim(0.035, 0.30)
    ax.set_xlabel("预计报告规模 m", fontproperties=FONT_CN, fontsize=7)
    ax.set_ylabel("方差", fontproperties=FONT_CN, fontsize=7)
    ax.legend(frameon=False, fontsize=6.2, loc="upper right",
              handlelength=1.2, borderpad=0.1, labelspacing=0.25)
    fig.savefig(path)
    plt.close(fig)


def new_panel_reversal(path):
    k, rho = 0.35, 0.25
    m = np.logspace(0, 3, 400)
    nu = k * m / rho ** 2
    fig, ax = plt.subplots(figsize=(2.16, 2.0))
    fig.subplots_adjust(left=0.21, right=0.97, bottom=0.18, top=0.95)
    ax.loglog(m, nu, color=BLUE, lw=1.3)
    ax.fill_between(m, nu, 1e4, color=ORANGE, alpha=0.06, lw=0)
    ax.fill_between(m, 1, nu, color=GREEN, alpha=0.06, lw=0)
    ax.text(1.35, 4800, "扩大覆盖占优", fontproperties=FONT_CN, fontsize=6.4,
            color=ORANGE)
    ax.text(1.35, 1.6, "提高报告率占优", fontproperties=FONT_CN, fontsize=6.4,
            color=GREEN)
    ax.text(28, 380, r"$m=\rho^2\nu/k$", color=BLUE, fontsize=6.4)
    for mm, nn, tx, ty in ((17.9, 100, 1.55, 300), (178.6, 1000, 9.0, 3200)):
        ax.plot([mm], [nn], "o", ms=3.2, color="black", zorder=5)
        ax.annotate(f"({mm:g}, {nn:g})", xy=(mm, nn), xytext=(tx, ty),
                    fontsize=6.0, arrowprops=dict(arrowstyle="-", lw=0.5,
                                                   color="black", shrinkA=1,
                                                   shrinkB=2))
    ax.set_xlim(1, 1000)
    ax.set_ylim(1, 1e4)
    ax.set_xlabel("预计报告规模 m", fontproperties=FONT_CN, fontsize=7)
    ax.set_ylabel(r"报告率形状参数 $\nu$", fontproperties=FONT_CN, fontsize=7)
    fig.savefig(path)
    plt.close(fig)


def fig1():
    schematic = crop_schematic()
    p_vh = FIG / "_panel_vh.pdf"
    p_rev = FIG / "_panel_reversal.pdf"
    new_panel_vh(p_vh)
    new_panel_reversal(p_rev)

    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=820)
    y = 0.0

    im = Image.open(schematic)
    h = (PAGE_W - 2 * MARGIN) * im.height / im.width
    label(page, "A", 2.0, y)
    rect = fitz.Rect(MARGIN, y + LABEL_H, PAGE_W - MARGIN, y + LABEL_H + h)
    page.insert_image(rect, filename=str(schematic))
    y += LABEL_H + h + 4

    f02 = FIG / "fig_02_variance_theory.pdf"
    left, right = split_rects(f02)
    y = add_pdf_row(page, y, [("B", f02, left), ("C", f02, right)])
    y += GAP
    y = add_pdf_row(page, y, [("D", p_vh, None), ("E", p_rev, None)])

    page.set_cropbox(fitz.Rect(0, 0, PAGE_W, y + 8))
    doc.save(OUT / "fig_main1.pdf")
    doc.close()


def fig2():
    f07 = FIG / "fig_07_nhsn_series.pdf"
    f08 = FIG / "fig_08_early_scale.pdf"
    f09 = FIG / "fig_09_denominator_noise.pdf"

    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=820)
    y = 0.0

    r = tight_clip(f07, src_rect(f07))
    w = PAGE_W - 2 * MARGIN
    h = w * r.height / r.width
    label(page, "A", 2.0, y)
    place_pdf(page, f07, (MARGIN, y + LABEL_H, MARGIN + w, y + LABEL_H + h), r)
    y += LABEL_H + h + GAP

    r8 = src_rect(f08)
    w8 = 300.0
    h8 = w8 * r8.height / r8.width
    x8 = (PAGE_W - w8) / 2
    label(page, "B", x8 + 1.0, y)
    place_pdf(page, f08, (x8, y + LABEL_H, x8 + w8, y + LABEL_H + h8))
    y += LABEL_H + h8 + GAP

    r9 = src_rect(f09)
    left9, right9 = split_rects(f09)
    y = add_pdf_row(page, y, [("C", f09, left9), ("D", f09, right9)])

    page.set_cropbox(fitz.Rect(0, 0, PAGE_W, y + 8))
    doc.save(OUT / "fig_main2.pdf")
    doc.close()


def fig3():
    f11 = FIG / "fig_11_reporting_adjustment.pdf"
    f12 = FIG / "fig_12_cross_pathogen.pdf"

    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=820)
    y = 0.0

    left11, right11 = split_rects(f11)
    y = add_pdf_row(page, y, [("A", f11, left11), ("B", f11, right11)])
    y += GAP

    # fig_12 carries one legend shared by its three panels, so it stays a
    # single full-width strip; cutting it into thirds would slice the legend.
    r12 = tight_clip(f12, src_rect(f12))
    w = PAGE_W - 2 * MARGIN
    h = w * r12.height / r12.width
    for letter, frac in (("C", 0.0), ("D", 0.448), ("E", 0.752)):
        label(page, letter, MARGIN + frac * w + 1.0, y)
    place_pdf(page, f12, (MARGIN, y + LABEL_H, MARGIN + w, y + LABEL_H + h), r12)
    y += LABEL_H + h

    page.set_cropbox(fitz.Rect(0, 0, PAGE_W, y + 8))
    doc.save(OUT / "fig_main3.pdf")
    doc.close()


def fig4():
    f04 = FIG / "fig_04_vR_precision.pdf"
    f05 = FIG / "fig_05_levers_budget.pdf"
    f06 = FIG / "fig_06_renewal_scale.pdf"

    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=860)
    y = 0.0
    for letters, path in (("AB", f04), ("CD", f05), ("EF", f06)):
        left, right = split_rects(path)
        y = add_pdf_row(page, y, [(letters[0], path, left),
                                  (letters[1], path, right)])
        y += GAP
    page.set_cropbox(fitz.Rect(0, 0, PAGE_W, y + 8))
    doc.save(OUT / "fig_main4.pdf")
    doc.close()


def fig5():
    f13 = FIG / "fig_13_scale_vs_seasons.pdf"
    f14 = FIG / "fig_14_peak_decomp.pdf"
    f15 = FIG / "fig_15_period_season_iqr.pdf"

    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=860)
    y = 0.0
    for letters, path in (("AB", f13), ("CD", f14), ("EF", f15)):
        left, right = split_rects(path)
        y = add_pdf_row(page, y, [(letters[0], path, left),
                                  (letters[1], path, right)])
        y += GAP
    page.set_cropbox(fitz.Rect(0, 0, PAGE_W, y + 8))
    doc.save(OUT / "fig_main5.pdf")
    doc.close()


def supplement_figure(src, dst, width=450.0):
    r = src_rect(src)
    h = width * r.height / r.width
    doc = fitz.open()
    page = doc.new_page(width=width, height=h + 0.6)
    place_pdf(page, src, (0, 0, width, h))
    doc.save(dst)
    doc.close()


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    supplement_figure(FIG / "fig_03_growth_test.pdf", FIG / "fig_s3_growth.pdf")
    supplement_figure(FIG / "fig_10_bootstrap_ratios.pdf", FIG / "fig_s1_bootstrap.pdf")
    supplement_figure(FIG / "fig_16_mx_forest.pdf", FIG / "fig_s2_forest.pdf")
    for p in OUT.glob("fig_main*.pdf"):
        r = src_rect(p)
        print(f"{p.name}: {r.width:.1f} x {r.height:.1f} pt")

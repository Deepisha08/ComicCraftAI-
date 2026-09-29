from pathlib import Path
from fpdf import FPDF


BASE_DIR = Path(__file__).resolve().parent.parent.parent
EXPORTS_DIR = BASE_DIR / "static" / "exports"


def safe_text(text):
    if text is None:
        return ""

    text = str(text)

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\n": " ",
        "\r": " ",
        "\t": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    words = text.split()
    fixed_words = []

    for word in words:
        if len(word) > 40:
            chunks = [
                word[i:i + 30]
                for i in range(0, len(word), 30)
            ]
            fixed_words.append(" ".join(chunks))
        else:
            fixed_words.append(word)

    return " ".join(fixed_words)


def write_text(pdf, label, text):
    text = safe_text(text)

    if not text:
        return

    pdf.multi_cell(
        0,
        7,
        f"{label}: {text}",
        new_x="LMARGIN",
        new_y="NEXT",
    )


def save_pdf(title, panels):

    EXPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = EXPORTS_DIR / "comic.pdf"

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    # Cover page
    pdf.add_page()

    pdf.set_font(
        "Arial",
        "B",
        20,
    )

    pdf.multi_cell(
        0,
        12,
        safe_text(title),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(8)

    # Every comic panel
    for panel in panels:

        pdf.add_page()

        # Panel title
        pdf.set_font(
            "Arial",
            "B",
            16,
        )

        panel_title = (
            f"Panel {panel.panel_number}: "
            f"{safe_text(panel.title)}"
        )

        pdf.multi_cell(
            0,
            9,
            panel_title,
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.ln(3)

        # Add clean panel image
        image_path = panel.image_path

        if image_path:

            if image_path.startswith("/static/"):
                relative_path = image_path.lstrip("/")
                local_image = BASE_DIR / relative_path
            else:
                local_image = Path(image_path)

            if local_image.exists():

                pdf.image(
                    str(local_image),
                    x=15,
                    y=35,
                    w=180,
                    h=100,
                )

                # Keep all text below the image
                pdf.set_y(140)

        pdf.ln(5)

        # Panel text below image
        pdf.set_font(
            "Arial",
            "",
            10,
        )

        write_text(
            pdf,
            "Scene",
            panel.scene_description,
        )

        write_text(
            pdf,
            "Caption",
            panel.caption,
        )

        write_text(
            pdf,
            "Narration",
            panel.narration,
        )

        write_text(
            pdf,
            "Dialogue",
            panel.dialogue,
        )

    # Save PDF
    pdf.output(
        str(output_path)
    )

    return "/static/exports/comic.pdf"
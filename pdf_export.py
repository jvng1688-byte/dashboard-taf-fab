"""
Exportacao PDF do resultado TAF - usa fpdf2 (>=2.7.0, pure Python)
"""
from fpdf import FPDF
from datetime import datetime
from taf_calculator import TAFResult


class TAFPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "RELATORIO DE DESEMPENHO - TAF FAB", align="C", ln=True)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} | Base: IN 002/2023-DGP/FAB", align="C", ln=True)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Dashboard TAF FAB - Portfolio Arthur Mota | github.com/jvng16688", align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0, 51, 102)
        self.cell(0, 8, title, ln=True)
        self.set_draw_color(0, 51, 102)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def kv_row(self, key: str, value: str, indent: int = 10):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 50)
        x = self.get_x() + indent
        self.set_x(x)
        self.cell(60, 6, f"{key}:")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, value, ln=True)


def generate_taf_pdf(result: TAFResult, filename: str = "taf_resultado.pdf"):
    pdf = TAFPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.section_title("1. DADOS DO CANDIDATO")
    pdf.kv_row("Sexo", "Masculino" if result.sexo == "M" else "Feminino")
    pdf.kv_row("Idade", f"{result.idade} anos")
    pdf.ln(3)

    pdf.section_title("2. PERFORMANCE BRUTA (Entradas)")
    pdf.kv_row("Corrida 12 min", f"{result.corrida_metros:.0f} metros")
    pdf.kv_row("Flexao de braco", f"{result.flexao_reps} repeticoes")
    pdf.kv_row("Abdominal 1 min", f"{result.abdominal_reps} repeticoes")
    pdf.kv_row("Barra fixa", f"{result.barra_valor:.0f} {'segundos' if result.sexo=='M' else 'repeticoes'}")
    pdf.kv_row("Natacao 50m livre", f"{result.natacao_segundos:.1f} segundos")
    pdf.ln(3)

    pdf.section_title("3. PONTUACAO OFICIAL (Tabela FAB)")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(80, 7, "Prova", border=1, fill=True)
    pdf.cell(30, 7, "Performance", border=1, fill=True, align="C")
    pdf.cell(30, 7, "Pontos", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)

    provas = [
        ("Corrida 12 min", f"{result.corrida_metros:.0f} m", result.pts_corrida),
        ("Flexao de braco", f"{result.flexao_reps} reps", result.pts_flexao),
        ("Abdominal 1 min", f"{result.abdominal_reps} reps", result.pts_abdominal),
        ("Barra fixa", f"{result.barra_valor:.0f} {'s' if result.sexo=='M' else 'reps'}", result.pts_barra),
        ("Natacao 50m livre", f"{result.natacao_segundos:.1f} s", result.pts_natacao),
    ]
    for nome, perf, pts in provas:
        pdf.cell(80, 7, nome, border=1)
        pdf.cell(30, 7, perf, border=1, align="C")
        color = (0, 150, 0) if pts >= 60 else (200, 0, 0) if pts < 40 else (200, 150, 0)
        pdf.set_text_color(*color)
        pdf.cell(30, 7, str(pts), border=1, align="C")
        pdf.set_text_color(0, 0, 0)
        pdf.ln()

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"TOTAL: {result.total} / 500  |  MEDIA: {result.media} / 100", align="C", ln=True)

    status_color = (0, 150, 0) if result.status == "APTO" else (200, 0, 0)
    pdf.set_text_color(*status_color)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, f"STATUS: {result.status}", align="C", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    from taf_calculator import get_next_milestone
    milestone = get_next_milestone(result)
    if "target_media" in milestone:
        pdf.section_title("4. PROXIMO MARCO")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, f"Meta: Media {milestone['target_media']} (APTO = 60)", ln=True)
        pdf.cell(0, 6, f"Pontos faltantes: {milestone['pontos_faltantes']:.0f}", ln=True)
        if "melhorias" in milestone and isinstance(milestone['melhorias'], dict):
            for prova, dados in milestone['melhorias'].items():
                if isinstance(dados, dict):
                    pdf.kv_row(f"  {prova}", f"{dados['atual_pts']} -> {dados['necessario_pts']} pts (+{dados['ganho_pts']})", indent=15)

    pdf.ln(5)
    pdf.section_title("5. OBSERVACOES")
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 5, "Calculos baseados na IN 002/2023-DGP/FAB e Portaria 805/GC3. APTO = Media >= 60 E todas as provas >= 40 pontos. Este relatorio e para fins de acompanhamento pessoal e portfolio. Resultado oficial somente na comissao de avaliacao da FAB.")

    pdf.output(filename)
    return filename
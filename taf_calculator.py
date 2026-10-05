"""
Calculadora oficial TAF FAB (EEAR/EPCAR/QOCON)
Baseada na INSTRUCAO NORMATIVA N 002/2023-DGP/FAB e PORTARIA N 805/GC3.
"""
from dataclasses import dataclass
from typing import Literal
import math

CORRIDA_12M_HOMENS = [(3200,100),(3150,99),(3100,98),(3050,97),(3000,96),(2950,95),(2900,94),(2850,93),(2800,92),(2750,91),(2700,90),(2650,89),(2600,88),(2550,87),(2500,86),(2450,85),(2400,84),(2350,83),(2300,82),(2250,81),(2200,80),(2150,79),(2100,78),(2050,77),(2000,76),(1950,75),(1900,74),(1850,73),(1800,72),(1750,71),(1700,70),(1650,69),(1600,68),(1550,67),(1500,66),(1450,65),(1400,64),(1350,63),(1300,62),(1250,61),(1200,60),(1150,59),(1100,58),(1050,57),(1000,56),(950,55),(900,54),(850,53),(800,52),(750,51),(700,50),(650,49),(600,48),(550,47),(500,46),(450,45),(400,44),(350,43),(300,42),(250,41),(200,40),(0,0)]
CORRIDA_12M_MULHERES = [(2800,100),(2750,99),(2700,98),(2650,97),(2600,96),(2550,95),(2500,94),(2450,93),(2400,92),(2350,91),(2300,90),(2250,89),(2200,88),(2150,87),(2100,86),(2050,85),(2000,84),(1950,83),(1900,82),(1850,81),(1800,80),(1750,79),(1700,78),(1650,77),(1600,76),(1550,75),(1500,74),(1450,73),(1400,72),(1350,71),(1300,70),(1250,69),(1200,68),(1150,67),(1100,66),(1050,65),(1000,64),(950,63),(900,62),(850,61),(800,60),(750,59),(700,58),(650,57),(600,56),(550,55),(500,54),(450,53),(400,52),(350,51),(300,50),(250,49),(200,48),(150,47),(100,46),(50,45),(0,0)]
FLEXAO_HOMENS = [(50,100),(49,99),(48,98),(47,97),(46,96),(45,95),(44,94),(43,93),(42,92),(41,91),(40,90),(39,89),(38,88),(37,87),(36,86),(35,85),(34,84),(33,83),(32,82),(31,81),(30,80),(29,79),(28,78),(27,77),(26,76),(25,75),(24,74),(23,73),(22,72),(21,71),(20,70),(19,69),(18,68),(17,67),(16,66),(15,65),(14,64),(13,63),(12,62),(11,61),(10,60),(9,59),(8,58),(7,57),(6,56),(5,55),(4,54),(3,53),(2,52),(1,51),(0,0)]
FLEXAO_MULHERES = [(40,100),(39,99),(38,98),(37,97),(36,96),(35,95),(34,94),(33,93),(32,92),(31,91),(30,90),(29,89),(28,88),(27,87),(26,86),(25,85),(24,84),(23,83),(22,82),(21,81),(20,80),(19,79),(18,78),(17,77),(16,76),(15,75),(14,74),(13,73),(12,72),(11,71),(10,70),(9,69),(8,68),(7,67),(6,66),(5,65),(4,64),(3,63),(2,62),(1,61),(0,0)]
ABDOMINAL_HOMENS = [(55,100),(54,99),(53,98),(52,97),(51,96),(50,95),(49,94),(48,93),(47,92),(46,91),(45,90),(44,89),(43,88),(42,87),(41,86),(40,85),(39,84),(38,83),(37,82),(36,81),(35,80),(34,79),(33,78),(32,77),(31,76),(30,75),(29,74),(28,73),(27,72),(26,71),(25,70),(24,69),(23,68),(22,67),(21,66),(20,65),(19,64),(18,63),(17,62),(16,65),(15,64),(14,63),(13,62),(12,61),(11,60),(10,59),(9,58),(8,57),(7,56),(6,55),(5,54),(4,53),(3,52),(2,51),(1,50),(0,0)]
ABDOMINAL_MULHERES = [(50,100),(49,99),(48,98),(47,97),(46,96),(45,95),(44,94),(43,93),(42,92),(41,91),(40,90),(39,89),(38,88),(37,87),(36,86),(35,85),(34,84),(33,83),(32,82),(31,81),(30,80),(29,79),(28,78),(27,77),(26,76),(25,75),(24,74),(23,73),(22,72),(21,71),(20,70),(19,69),(18,68),(17,67),(16,66),(15,65),(14,64),(13,63),(12,62),(11,61),(10,60),(9,59),(8,58),(7,57),(6,56),(5,55),(4,54),(3,53),(2,52),(1,51),(0,0)]
BARRA_HOMENS = [(60,100),(58,99),(56,98),(54,97),(52,96),(50,95),(48,94),(46,93),(44,92),(42,91),(40,90),(38,89),(36,88),(34,87),(32,86),(30,85),(28,84),(26,83),(24,82),(22,81),(20,80),(18,79),(16,78),(14,77),(12,76),(10,75),(9,74),(8,73),(7,72),(6,71),(5,70),(4,69),(3,68),(2,67),(1,66),(0,0)]
BARRA_MULHERES = [(15,100),(14,99),(13,98),(12,97),(11,96),(10,95),(9,94),(8,93),(7,92),(6,91),(5,90),(4,89),(3,88),(2,87),(1,86),(0,0)]
NATACAO_50M_HOMENS = [(30,100),(31,99),(32,98),(33,97),(34,96),(35,95),(36,94),(37,93),(38,92),(39,91),(40,90),(41,89),(42,88),(43,87),(44,86),(45,85),(46,84),(47,83),(48,82),(49,81),(50,80),(51,79),(52,78),(53,77),(54,76),(55,75),(56,74),(57,73),(58,72),(59,71),(60,70),(61,69),(62,68),(63,67),(64,66),(65,65),(66,64),(67,63),(68,62),(69,61),(70,60),(71,59),(72,58),(73,57),(74,56),(75,55),(76,54),(77,53),(78,52),(79,51),(80,50),(999,0)]
NATACAO_50M_MULHERES = [(34,100),(35,99),(36,98),(37,97),(38,96),(39,95),(40,94),(41,93),(42,92),(43,91),(44,90),(45,89),(46,88),(47,87),(48,86),(49,85),(50,84),(51,83),(52,82),(53,81),(54,80),(55,79),(56,78),(57,77),(58,76),(59,75),(60,74),(61,73),(62,72),(63,71),(64,70),(65,69),(66,68),(67,67),(68,66),(69,65),(70,64),(71,63),(72,62),(73,61),(74,60),(75,59),(76,58),(77,57),(78,56),(79,55),(80,54),(81,53),(82,52),(83,51),(84,50),(999,0)]

def lookup_score(value: float, table: list) -> int:
    for threshold, points in table:
        if value >= threshold: return points
    return 0

@dataclass
class TAFResult:
    sexo: Literal["M", "F"]; idade: int
    corrida_metros: float; flexao_reps: int; abdominal_reps: int; barra_valor: float; natacao_segundos: float
    pts_corrida: int = 0; pts_flexao: int = 0; pts_abdominal: int = 0; pts_barra: int = 0; pts_natacao: int = 0
    total: int = 0; media: float = 0.0; status: str = ""
    def __post_init__(self): self.calculate()
    def calculate(self):
        if self.sexo == "M":
            self.pts_corrida = lookup_score(self.corrida_metros, CORRIDA_12M_HOMENS)
            self.pts_flexao = lookup_score(self.flexao_reps, FLEXAO_HOMENS)
            self.pts_abdominal = lookup_score(self.abdominal_reps, ABDOMINAL_HOMENS)
            self.pts_barra = lookup_score(self.barra_valor, BARRA_HOMENS)
            self.pts_natacao = lookup_score(self.natacao_segundos, NATACAO_50M_HOMENS)
        else:
            self.pts_corrida = lookup_score(self.corrida_metros, CORRIDA_12M_MULHERES)
            self.pts_flexao = lookup_score(self.flexao_reps, FLEXAO_MULHERES)
            self.pts_abdominal = lookup_score(self.abdominal_reps, ABDOMINAL_MULHERES)
            self.pts_barra = lookup_score(self.barra_valor, BARRA_MULHERES)
            self.pts_natacao = lookup_score(self.natacao_segundos, NATACAO_50M_MULHERES)
        self.total = self.pts_corrida + self.pts_flexao + self.pts_abdominal + self.pts_barra + self.pts_natacao
        self.media = round(self.total / 5, 1)
        provas = [self.pts_corrida, self.pts_flexao, self.pts_abdominal, self.pts_barra, self.pts_natacao]
        self.status = "APTO" if self.media >= 60 and all(p >= 40 for p in provas) else "INAPTO"
    def to_dict(self) -> dict:
        return {"Sexo": self.sexo, "Idade": self.idade, "Corrida (m)": self.corrida_metros,
                "Flexao (reps)": self.flexao_reps, "Abdominal (reps)": self.abdominal_reps,
                "Barra (s/reps)": self.barra_valor, "Natacao 50m (s)": self.natacao_segundos,
                "Pts Corrida": self.pts_corrida, "Pts Flexao": self.pts_flexao,
                "Pts Abdominal": self.pts_abdominal, "Pts Barra": self.pts_barra,
                "Pts Natacao": self.pts_natacao, "TOTAL": self.total, "MEDIA": self.media, "STATUS": self.status}

def calculate_required_for_target(current: TAFResult, target_media: float = 60) -> dict:
    current_scores = [current.pts_corrida, current.pts_flexao, current.pts_abdominal, current.pts_barra, current.pts_natacao]
    deficit = max(0, target_media * 5 - current.total)
    if deficit <= 0: return {"message": f"Ja atingiu media {target_media}! 🎉"}
    improvements = {}; provas_nomes = ["Corrida 12min", "Flexao de Braco", "Abdominal 1min", "Barra Fixa", "Natacao 50m"]
    for i, (score, nome) in enumerate(zip(current_scores, provas_nomes)):
        if score < 100:
            needed = min(100 - score, math.ceil(deficit / 5) + 5)
            improvements[nome] = {"atual_pts": score, "necessario_pts": score + needed, "ganho_pts": needed}
    return improvements

def get_next_milestone(current: TAFResult) -> dict:
    for target in [60, 70, 80, 90, 100]:
        if current.media < target:
            return {"target_media": target, "pontos_faltantes": target * 5 - current.total, "melhorias": calculate_required_for_target(current, target)}
    return {"message": "MAXIMO ATINGIDO! 🏆"}